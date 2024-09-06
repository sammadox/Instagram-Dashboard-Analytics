import json

#Main utils
def get_followers_count_from_file(file_path):
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
                followers_count = user_info.get('followersCount', None)
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

def get_followers_growth_from_file(file_path):
    with open(file_path,encoding='utf-8') as file:
            # Load JSON data from the file
            data = json.load(file)
            
            # Check if data is a list and has at least one item
            if isinstance(data, list) and len(data) > 0:
                # Extract the first item from the list
                try:
                    if data[0]['latestPosts']:
                        post_info = data[0]['latestPosts']
                except:
                    pass

            L=[]
            for i in range(len(post_info)):
                try:
                    if post_info[i]['isPinned']:
                        pass
                except:
                    L.append(post_info[i]['likesCount'])
    if len(L)==0:
        return(0)
    else:
        return(average_growth_rate(L))

def calculate_followers_lost_and_turnover(actual_growth_rate, standard_growth_rate, initial_followers):
    # Calculate expected new followers based on the standard growth rate
    expected_new_followers = standard_growth_rate * initial_followers
    
    # Calculate actual new followers based on the actual growth rate
    actual_new_followers = actual_growth_rate * initial_followers
    
    # Calculate the difference between expected and actual new followers
    followers_lost = max(expected_new_followers - actual_new_followers, 0)
    
    # Calculate total turnover (gained and lost followers)
    total_gained_followers = max(actual_new_followers, 0)
    total_lost_followers = max(followers_lost, 0)
    
    # Calculate turnover rate based on total gained and lost followers
    turnover_rate = ((total_gained_followers + total_lost_followers) / initial_followers) * 100
    
    return followers_lost, turnover_rate

def calculate_ratio(followers, following):
    if following == 0:
        return "N/A"  # To avoid division by zero
    ratio = (followers / following) * 100
    formatted_ratio = f"{ratio:,.2f}%"
    return formatted_ratio
#Optional utils
def average_growth_rate(metrics):
    growth_rates = []
    
    for i in range(1, len(metrics)):
        growth_rate = (metrics[i] - metrics[i-1]) / metrics[i-1]
        growth_rates.append(growth_rate)
    
    average_growth = sum(growth_rates) / len(growth_rates)
    
    # Format the average growth rate as "xx,xx%"
    formatted_growth = f"{average_growth * 100:.2f}".replace('.', ',') + "%"
    
    return formatted_growth

def get_following_count_from_file(file_path):
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
                follows_count = user_info.get('followsCount', None)
                if follows_count is not None:
                    # Format the followers count with commas
                    formatted_followers_count = f"{follows_count:,}"
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


def calculate_average(numbers):
    return sum(numbers) / len(numbers)

def percentage_to_number(percentage_str):
    # Replace the comma with a dot and remove the percentage symbol
    number_str = percentage_str.replace(',', '.').replace('%', '')
    
    # Convert the string to a float and divide by 100 to get the number
    number = float(number_str) / 100
    
    return number

def string_to_number(number_str):
    # Remove the comma and convert the string to an integer
    number = int(number_str.replace(',', ''))
    return number

def to_percentage(value):
    # Convert the number to a percentage with 2 decimal places
    percentage = f"{value:.2f}%"
    return percentage

