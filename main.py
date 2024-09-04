import streamlit as st
import altair as alt
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
from PIL import Image
from io import BytesIO
import requests
import base64
import os
from scraper import *
from mapsData import *
from scraperPost import *
from AccountsFollowersMetrics import get_followers_count_from_file,get_followers_growth_from_file,percentage_to_number,string_to_number,calculate_followers_lost_and_turnover,to_percentage,calculate_ratio,get_following_count_from_file
from FollowerEngagementMetrics import *
from main2 import extract_user_data
from parse_scraper import read_csv_and_create_data_structure

def display_markdown(value):
    st.markdown(
        f"""
        <div style='padding: 10px; border-radius: 10px; background-color: #f0f2f6;'>
            <h1 style='color: #ff4b4b;'>{value}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

def download_image(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Check if the request was successful
        return BytesIO(response.content)
    except Exception as e:
        st.error(f"Error downloading image: {e}")
        return None

def image_to_base64(image_data):
    """Convert image bytes to base64 encoding."""
    image = Image.open(image_data)
    buffer = BytesIO()
    image.save(buffer, format='JPEG')
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

def truncate_string(s, max_length):
    if len(s) > max_length:
        return s[:max_length] + "..."  # Adding "..." to indicate truncation
    return s

def send_markdown(ranking, caption, image_url, likes, shares, post_url):
    # Attempt to download the image
    image_data = download_image(image_url)
    
    if image_data:
        # Convert image data to base64 string
        image_base64 = image_to_base64(image_data)
        image_src = f"data:image/jpeg;base64,{image_base64}"
    else:
        # Fallback to placeholder image URL
        image_src = "https://via.placeholder.com/600x400"
    
    # Format the markdown string with the provided parameters
    markdown_code = f"""
    <div style='padding: 15px; border-radius: 10px; background-color: #f0f2f6; margin-bottom: 10px;'>
        <!-- Clickable link as a heading -->
        <a href='{post_url}' style='display: block; font-size: 24px; color: #ff4b4b; text-decoration: none; font-weight: bold;'>#{ranking}</a>
        <!-- Image of the post -->
        <img src='{image_src}' alt='Post{ranking} Image' style='max-width: 600px; max-height: 400px; border-radius: 10px; margin: 0 auto; display: block; object-fit: cover;'>
        <!-- Post caption -->
        <p style='font-size: 16px; color: #333;'>{caption}</p>
        <!-- Likes and comments -->
        <div style='display: flex; justify-content: space-between; font-size: 14px; color: #555;'>
            <span><strong>Likes:</strong> {likes}</span>
            <span><strong>Comments:</strong> {shares}</span>
        </div>
    </div>
    """
    
    # Display the markdown code with HTML in Streamlit
    st.markdown(markdown_code, unsafe_allow_html=True)
    file_path = "temp_image.jpg"

    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"{file_path} has been deleted.")
        else:
            print(f"{file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
# Initialize session state if not already done
#Account Follower Metrics
if 'FollowerCount' not in st.session_state:
    st.session_state.FollowerCount = "-"
if 'FollowerGrowthRate' not in st.session_state:
    st.session_state.FollowerGrowthRate = "-"
if 'FollowerTurnoverRate' not in st.session_state:
    st.session_state.FollowerTurnoverRate = "-"
if 'FollowerFollowingRatio' not in st.session_state:
    st.session_state.FollowerFollowingRatio = "-"

#Follower Engagement Metrics
if 'AverageLikesPerPost' not in st.session_state:
    st.session_state.AverageLikesPerPost = "-"
if 'EngagementRate' not in st.session_state:
    st.session_state.EngagementRate = "-"
if 'TotalPosts' not in st.session_state:
    st.session_state.TotalPosts = "-"
if 'AvgComments' not in st.session_state:
    st.session_state.AvgComments = "-"
if 'ViralReachRate' not in st.session_state:
    st.session_state.ViralReachRate = "-"
if 'TotalLikes' not in st.session_state:
    st.session_state.TotalLikes = "-"
#Top performing posts
#1
if 'post1im' not in st.session_state:
    st.session_state.post1im = "-"
if 'post1cap' not in st.session_state:
    st.session_state.post1cap = "-"
if 'post1com' not in st.session_state:
    st.session_state.post1com = "-"
if 'post1like' not in st.session_state:
    st.session_state.post1like = "-"

#2
if 'post2im' not in st.session_state:
    st.session_state.post2im = "-"
if 'post2cap' not in st.session_state:
    st.session_state.post2cap = "-"
if 'post2com' not in st.session_state:
    st.session_state.post2com = "-"
if 'post2like' not in st.session_state:
    st.session_state.post2like = "-"

#3
if 'post3im' not in st.session_state:
    st.session_state.post3im = "-"
if 'post3cap' not in st.session_state:
    st.session_state.post3cap = "-"
if 'post3com' not in st.session_state:
    st.session_state.post3com = "-"
if 'post3like' not in st.session_state:
    st.session_state.post3like = "-"



def button_action():
    extract_user_data('data0.5.json')
    st.session_state.geoData=''
    st.session_state.geoData=read_csv_and_create_data_structure('user_data.csv')
    st.session_state.FollowerCount= get_followers_count_from_file('data.json')  # Change this to whatever new text you want
    st.session_state.FollowerGrowthRate = get_followers_growth_from_file('data.json') 

    #Load Needed data

    actual_growth_rate=percentage_to_number(get_followers_growth_from_file('data.json'))
    standard_growth_rate= 0.05
    initial_followers=string_to_number(get_followers_count_from_file('data.json'))
    st.session_state.FollowerTurnoverRate = to_percentage(calculate_followers_lost_and_turnover(actual_growth_rate,standard_growth_rate,initial_followers)[1])


    #Load Data to calculate the follower to following ration
    followers = string_to_number(get_followers_count_from_file('data.json'))
    following = string_to_number(get_following_count_from_file('data.json'))

    st.session_state.FollowerFollowingRatio = calculate_ratio(followers, following)


    st.session_state.AverageLikesPerPost=get_average_like_from_file('data.json')

    #col4
    average_likes = get_average_like_from_file('data.json')
    total_followers = string_to_number(get_followers_count_from_file('data.json'))
   
def button_scrape():
    if os.path.exists('data.json'):
        os.remove('data.json')
    # Call the function with the user input
    api_token = "apify_api_fp9UgFVmLHW5kXOM0i0Wlch8atIwFM2g3py6"  # Replace with your actual API token
    fetch_instagram_data(st.session_state.username, api_token)
    scrape_posts(st.session_state.username)
# Load the image from a local file
image = Image.open("logo.png")
# Page configuration
st.set_page_config(page_title="Follower Overview", layout="wide")



# Create a nice sidebar
with st.sidebar:
    st.image(image, use_column_width=True)  # Replace with your logo URL
    
    st.write("### Actions")

    # Add a button to the Streamlit app
    if st.button('Run Analysis'):
        button_action()
    if st.button('Scrape Data'):
        button_scrape()
    st.markdown("---")
    st.write("### Parameters")
    # Create a textbox with a placeholder
    user_input = st.text_input("URL:", placeholder="Instagram URL or Username")
    st.session_state.username=user_input
    # Create a drag-and-drop file uploader
    uploaded_file = st.file_uploader("Upload your follower CSV Followers (Optional)", type=["csv"])
    analysis_type = st.radio(
    "Select Analysis Type:",
    ("Light Analysis", "Deep Analysis")
)
    exclude_followers_quality = st.checkbox(
    "Exclude followers quality analysis"
)
    

     # Create a drag-and-drop file uploader
    proxy_file = st.file_uploader("Upload your Proxies list (required for deep analyis)", type=["csv"])

    

    st.markdown("---")
    st.write("### About")
    st.markdown(
    "<div style='background-color: #e0f7fa; padding: 10px; border-radius: 5px;'>"
    "<p style='color:red;'>This dashboard offers an overview of your followers and account metrics. Please note that the data may not always be 100% accurate. For the most precise information, refer to Instagram's official documentation.</p>"
    "</div>",
    unsafe_allow_html=True
)
# Add a button to the Streamlit app

with st.expander("Followers Overview", expanded=True):
    st.info("""
    In this section, you’ll gain valuable insights into your follower statistics and engagement metrics, which can help identify potential fake followers. 
    
    You'll see your total follower count, the growth trends, and how your followers compare to those you’re following. 
            
    This information is crucial for understanding the authenticity of your audience.

    Additionally, the Follower Engagement Metrics will show average likes and comments per post, along with the performance of your top posts. 
            
    By analyzing these metrics, you can detect inconsistencies or unusual patterns that may suggest the presence of fake followers. For example, if your engagement rates are low despite a high follower count, it could indicate that a significant portion of your followers may not be genuine. This overview helps you assess the quality of your follower base and take necessary actions to improve your account’s credibility and effectiveness.
    """)
    
    st.subheader("Account Follower Metrics")

    # Create columns for metrics
    col1, col2 = st.columns(2)

    # Display metrics in a structured layout
    with col1:
        st.markdown("### Follower Count")
        # Display the Markdown with dynamic text
        st.markdown(
            f"<div style='padding: 10px; border-radius: 10px; background-color: #f0f2f6;'>"
            f"<h1 style='color: #ff4b4b;'>{st.session_state.FollowerCount}</h1>"
            "</div>",
            unsafe_allow_html=True
        )

        #Define needed Data for calculating the Follower turnover rate
       
        st.markdown("### Follower Turnover Rate")
        st.markdown(
            f"<div style='padding: 10px; border-radius: 10px; background-color: #f0f2f6;'>"
            f"<h1 style='color: #ff4b4b;'>{st.session_state.FollowerTurnoverRate}</h1>"
            "</div>",
            unsafe_allow_html=True
        )

    with col2:
        st.markdown("### Follower Growth Rate")
        st.markdown(f"<div style='padding: 10px; border-radius: 10px; background-color: #f0f2f6;'>"
            f"<h1 style='color: #ff4b4b;'>{st.session_state.FollowerGrowthRate}</h1>"
            "</div>",
            unsafe_allow_html=True)
        
        st.markdown("### Follower to Following Ratio")
        st.markdown(f"<div style='padding: 10px; border-radius: 10px; background-color: #f0f2f6;'>"
            f"<h1 style='color: #ff4b4b;'>{st.session_state.FollowerFollowingRatio}</h1>"
            "</div>",
            unsafe_allow_html=True)

    # Use Markdown with HTML to draw a line
    # Add space between subheaders
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.subheader("Follower Engagement Metrics")

    col3, col4, col4bis = st.columns(3)

    with col4bis:
        st.markdown("### Total Number of Posts")
        display_markdown(get_posts_count_from_file('data.json'))
        st.markdown("### Total Likes")
        display_markdown(get_total_like_from_file('data.json'))
        st.markdown("###")
        L = extract_posts('data.json')
        send_markdown(
    ranking=3,
    caption=truncate_string(L[2][3],10),
    image_url=L[2][1],
    likes=L[2][0],
    shares=L[2][2],
    post_url=L[2][1]
)
        #st.markdown("<div style='padding: 15px; border-radius: 10px; background-color: #f0f2f6; margin-bottom: 10px;'> <!-- Clickable link as a heading --> <a href='https://example.com/post1' style='display: block; font-size: 24px; color: #ff4b4b; text-decoration: none; font-weight: bold;'>#1</a> <!-- Image of the post --> <img src='https://via.placeholder.com/600x400' alt='Post1 Image' style='width: 100%; border-radius: 10px; margin-bottom: 10px;'> <!-- Post caption --> <p style='font-size: 16px; color: #333;'>This is the caption for Post1. It provides a brief description or context about the post.</p> <!-- Likes and comments --> <div style='display: flex; justify-content: space-between; font-size: 14px; color: #555;'> <span><strong>Likes:</strong> 123</span> <span><strong>Comments:</strong> 45</span> </div> </div>", unsafe_allow_html=True)

    with col3:
        st.markdown("### Average Likes per Post")
        display_markdown(get_average_like_from_file('data.json'))
        st.markdown("### Average Comments per Post")
        display_markdown(get_average_comments_from_file('data.json'))
        st.markdown("### Top Three Top performing Posts")
        L = extract_posts('data.json')
        send_markdown(
    ranking=1,
    caption=truncate_string(L[0][3],10),
    image_url=L[0][1],
    likes=L[0][0],
    shares=L[0][2],
    post_url=L[0][1]
)
    with col4:
        

        st.markdown("### Engagement Rate")
        average_likes=get_average_like_from_file('data.json')
        total_followers=string_to_number(get_followers_count_from_file('data.json'))
        average_comments=get_average_comments_from_file('data.json')
        display_markdown(calculate_engagement_rate(average_likes,total_followers))
        
        st.markdown("### Viral Reach Rate")

        display_markdown(calculate_viral_reach_rate(average_likes, average_comments, total_followers))
        st.markdown("###")
        L = extract_posts('data.json')
        send_markdown(
    ranking=2,
    caption=truncate_string(L[1][3],10),
    image_url=L[1][1],
    likes=L[1][0],
    shares=L[1][2],
    post_url=L[1][1]
)
# Add a horizontal line to separate sections

with st.expander("Follower Demographics"):
    st.info("""
    In this section, you'll explore the demographic breakdown of your followers, offering key insights into their geographic distribution and language preferences.

    You'll be able to see the top countries where your followers are located and understand how diverse your audience is through the Geographic Diversity Index. This index is essential for gauging how well your content resonates across different regions.

    Additionally, the app provides a detailed analysis of demographic attributes, including the most common languages spoken by your followers. You'll also find a heatmap showing the gender ratio and geographic distribution, giving you a clearer picture of your audience's composition.

    By examining these demographics, you can tailor your content more effectively to engage with different segments of your audience, ensuring that your messaging aligns with their cultural and regional contexts.
    """)

    # Part 1
    st.markdown("<hr>", unsafe_allow_html=True)


    st.title("Follower Demographics")
    st.subheader("Geographic Distribution")

    col5, col6 = st.columns(2)

    with col5:
    # Sample data
        print(st.session_state.geoData)
        data =st.session_state.geoData

        df = pd.DataFrame(data)

        st.markdown("### Top Follower Countries")

        st.write("This app visualizes the 'Top Follower Countries Geographic Diversity Index'.")

        chart = alt.Chart(df).mark_bar().encode(
            x="country",
            y="index"
        ).properties(
            width=800,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)


    with col6:
        # Sample data
        data = DataMaps()

        map_data = pd.DataFrame(data)
        df = pd.DataFrame(data)
        st.markdown("### Geographic Diversity Index")

        st.write("This app visualizes the 'Top Follower Countries Geographic Diversity Index'.")
    
        # Create a pydeck Deck object for the choropleth map
        st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=30,  # Central latitude for the initial view
        longitude=100,  # Central longitude for the initial view
        zoom=1,
        pitch=0,
    ),
    layers=[
        pdk.Layer(
            'HeatmapLayer',
            data=map_data,
            get_position=['lon', 'lat'],
            get_weight='probability',
            radius_pixels=60,
            intensity=5,
            color_range=[
                [255, 255, 204],
                [255, 237, 160],
                [254, 217, 118],
                [254, 178, 76],
                [253, 141, 60],
                [252, 78, 42],
                [227, 26, 28],
                [177, 0, 38],
                [128, 0, 38]
            ],
            threshold=0.5,
            opacity=0.8
        )
    ]
))


    st.markdown("<br><br>", unsafe_allow_html=True)

    st.subheader("Demographic Attributes")



    col7, col8 = st.columns(2)

    with col7:
    # Sample data
        st.markdown("### Top Follower Languages")
        labels = ['English', 'Spanish', 'French', 'German']
        sizes = [100, 80, 50, 30]
        colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']  # Custom colors

        # Create a pie chart
        fig, ax = plt.subplots(figsize=(8, 6))  # Set figure size

        # Define the function to center the percentage labels
        def make_autopct(pct):
            return f'{pct:.1f}%'

        # Plot pie chart
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct=make_autopct, startangle=140,
                                        wedgeprops=dict(edgecolor='w', linewidth=1, width=0.4))  # Remove background and add style

        # Style the text for better readability
        for text in autotexts:
            text.set_color('white')
            text.set_fontsize(12)
            text.set_weight('bold')

        # Add a legend to the chart
        ax.legend(wedges, labels, title="Languages", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

        # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.axis('equal')

        # Remove axes and background
        fig.patch.set_visible(False)
        ax.axis('off')

        # Display in Streamlit
        st.pyplot(fig)


    with col8:
    # Example data
    # Example data
        st.markdown("### Gender Ratio and geo Distribution Heatmap")
        data = {
            'Age Group': ['20-29', '20-29', '30-39', '30-39', '40-49', '40-49'],
            'Gender': ['Male', 'Female', 'Male', 'Female', 'Male', 'Female'],
            'Count': [50, 45, 60, 55, 70, 65]
        }

        df = pd.DataFrame(data)

        # Use pivot_table to handle potential duplicates
        pivot_table = df.pivot_table(index='Age Group', columns='Gender', values='Count', aggfunc='sum')

        # Set Seaborn style for better aesthetics
        sns.set(style='ticks')  # Use 'white' to ensure a clean background for the plot

        # Customize font settings
        rcParams['font.family'] = 'Arial'  # Set font family
        rcParams['font.size'] = 12  # Set font size


        # Generate the heatmap
        fig, ax = plt.subplots(figsize=(8, 6))

        # Use a red-based color map and remove the background
        sns.heatmap(pivot_table, annot=True, cmap='Reds', ax=ax, cbar_kws={'shrink': .8},
                    linewidths=0.5, linecolor='black')  # Remove background and adjust gridlines

        # Customize the plot appearance
        ax.set_facecolor('white')  # Set the background color of the plot area
        fig.patch.set_facecolor('white')  # Set the background color of the figure
        ax.set_xlabel('Gender', fontsize=14)  # Customize axis labels with font size
        ax.set_ylabel('Age Group', fontsize=14)
        ax.set_title('Heatmap of Gender Ratio by Age Group', fontsize=16)

        # Display the heatmap in Streamlit
        st.pyplot(fig)

# Add a horizontal line to separate sections
with st.expander("Followers Quality Analysis"):
    import streamlit as st

    st.info("""
    In this section, you’ll explore detailed insights into your follower demographics and geographic distribution, which can help you understand the diversity and authenticity of your audience.

    You'll see the distribution of your top follower countries and how it contributes to the 'Top Follower Countries Geographic Diversity Index.'

    Additionally, the Followers Quality Analysis will provide a breakdown of fake followers, including the Fake Follower Ratio and the percentage of Suspicious Follower Accounts. You’ll also find a summary of accounts flagged as suspicious based on various metrics.

    For example, a higher-than-average Fake Follower Ratio or Suspicion Score Distribution may indicate that a portion of your followers are not genuine. Identifying inactive followers and suspicious accounts can help you maintain a more authentic and engaged audience.

    Click the button above to view more details and download the full list of flagged accounts.
    """)


    st.subheader("Fake followers Detection")


    st.markdown("### Fake Follower Ratio")
    st.markdown("<div style='padding: 10px; border-radius: 10px; background-color: #f0f2f6;'>"
                    "<h1 style='color: #ff4b4b;'>11%</h1>"
                    "</div>", unsafe_allow_html=True)



    st.markdown("### Suspicious Follower Accounts")
    st.markdown("<div style='padding: 10px; border-radius: 10px; background-color: #f0f2f6;'>"
                    "<h1 style='color: #ff4b4b;'>5.6%</h1>"
                    "</div>", unsafe_allow_html=True)

    # Sample Data
    data = {
        'Account': ['User1', 'User2', 'User3', 'User4', 'User5'],
        'Suspicion Score': [85, 90, 78, 88, 92],
        'Details': ['High activity', 'Suspicious IP', 'Frequent follows', 'Spammy content', 'Multiple reports']
    }
    df = pd.DataFrame(data)



    # Displaying a summary of suspicious accounts
    st.header('Summary of Suspicious Accounts')
    st.write("Below is the list of accounts flagged as suspicious based on various metrics.")

    # Display top 3 suspicious accounts
    st.subheader('Top 3 Suspicious Accounts')
    st.write(df.head(3))

    # Button to view more details
    if st.button('Load More Details'):
        st.write("Complete List of Suspicious Accounts:")
        st.write(df)

        # Download button for full list
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download Full List as CSV",
            data=csv,
            file_name='suspicious_followers.csv',
            mime='text/csv'
        )
    else:
        st.write("Click the button above to view more details and download the full list.")

    # Optional: Visualize data with charts
    st.subheader('Suspicion Score Distribution')
    st.bar_chart(df.set_index('Account')['Suspicion Score'])
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.subheader("Inactive Follower Identification")




     
