import json

#Main Utils
#Average Likes per post
def get_average_like_from_file(file_path):
    with open(file_path,encoding='utf-8') as file:
            # Load JSON data from the file
            data = json.load(file)
            
            # Check if data is a list and has at least one item
            if isinstance(data, list) and len(data) > 0:
                # Extract the first item from the list
                post_info = data[0]['latestPosts']
            L=[]
            for i in range(len(post_info)):
                try:
                    if post_info[i]['isPinned']:
                        pass
                except:
                    L.append(post_info[i]['likesCount'])
    return(calculate_average(L))

#Engagement rate
def calculate_engagement_rate(average_likes, total_followers):
    """
    Calculate the engagement rate based on average likes and total followers.

    Parameters:
    average_likes (int): The average number of likes per post.
    total_followers (int): The total number of followers.

    Returns:
    float: The engagement rate as a percentage.
    """
    if total_followers == 0:
        raise ValueError("Total followers cannot be zero.")
    
    engagement_rate = (average_likes / total_followers) * 100
    return  f"{engagement_rate:.2f}%" 

#Total number of posts
def get_posts_count_from_file(file_path):
    """
    Reads JSON data from a file and extracts the followers count.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        int: The followers count if available, else returns None.
    """
    try:
        with open(file_path,encoding='utf-8') as file:
            # Load JSON data from the file
            data = json.load(file)
            
            # Check if data is a list and has at least one item
            if isinstance(data, list) and len(data) > 0:
                # Extract the first item from the list
                user_info = data[0]
                
                # Retrieve the followers count
                followers_count = user_info.get('postsCount', None)
                if followers_count is not None:
                    # Format the followers count with commas
                    formatted_followers_count = f"{followers_count:,}"
                    return formatted_followers_count
                else:
                    return "Followers count not found"
            else:
                return None
    except json.JSONDecodeError:
        print("Invalid JSON data")
        return None
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

#Average Comments
def get_average_comments_from_file(file_path):
    with open(file_path,encoding='utf-8') as file:
            # Load JSON data from the file
            data = json.load(file)
            
            # Check if data is a list and has at least one item
            if isinstance(data, list) and len(data) > 0:
                # Extract the first item from the list
                post_info = data[0]['latestPosts']
            L=[]
            for i in range(len(post_info)):
                try:
                    if post_info[i]['isPinned']:
                        pass
                except:
                    L.append(post_info[i]['commentsCount'])
    return(calculate_average(L))
#Viral Reach Rate
def calculate_viral_reach_rate(average_likes, average_comments, total_followers):
    """
    Calculate the approximate Viral Reach Rate.

    Parameters:
    average_likes (int): The average number of likes received.
    average_comments (int): The average number of comments received.
    total_followers (int): The total number of followers.

    Returns:
    float: The approximate Viral Reach Rate as a percentage.
    """
    if total_followers <= 0:
        raise ValueError("Total followers must be greater than zero.")
    
    total_engagement = average_likes + average_comments
    viral_reach_rate = (total_engagement / total_followers) * 100
    
    return f"{viral_reach_rate:.2f}%" 

#Total Likes
def get_total_like_from_file(file_path):
    with open(file_path,encoding='utf-8') as file:
            # Load JSON data from the file
            data = json.load(file)
            
            # Check if data is a list and has at least one item
            if isinstance(data, list) and len(data) > 0:
                # Extract the first item from the list
                post_info = data[0]['latestPosts']
            L=[]
            for i in range(len(post_info)):
                try:
                    if post_info[i]['isPinned']:
                        pass
                except:
                    L.append(post_info[i]['likesCount'])
    return(sum(L))
def top_three_posts(L):
    # Sort the list based on likesCount and commentsCount, descending order
    L_sorted = sorted(L, key=lambda x: (x[0] + x[2]), reverse=True)
    
    # Return the top three posts
    return L_sorted[:3]
#Secondary Utils
def calculate_average(numbers):
    return sum(numbers) / len(numbers)

#Extract all posts images, caption, likes and comments
def extract_posts(file_path):
    with open(file_path,encoding='utf-8') as file:
            # Load JSON data from the file
            data = json.load(file)
            
            # Check if data is a list and has at least one item
            if isinstance(data, list) and len(data) > 0:
                # Extract the first item from the list
                if data[0]['latestPosts']:
                    post_info = data[0]['latestPosts']
            L=[]
            for i in range(len(post_info)):
                try:
                    if post_info[i]['isPinned']:
                        pass
                except:
                    H=[]
                    H.append(post_info[i]['likesCount'])
                    H.append(post_info[i]['displayUrl'])
                    H.append(post_info[i]['commentsCount'])
                    H.append(post_info[i]['caption'])
                    L.append(H)
    return(L)


