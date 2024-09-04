import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def replace_long_items(input_list, max_length=10, replacement='Others'):
    """
    Replace items in the list that are longer than `max_length` with `replacement`.

    Parameters:
    - input_list (list): The list to be processed.
    - max_length (int): The maximum length for items to be retained.
    - replacement (str): The value to replace items longer than `max_length`.

    Returns:
    - list: The processed list with long items replaced.
    """
    # Process each item in the list
    processed_list = [replacement if (item is not None and len(item) > max_length) else item for item in input_list]

    return processed_list
# Load the CSV data
df = pd.read_csv('user_data.csv')

# Debugging: Print the first few rows of the DataFrame to check its content
print("Initial DataFrame:")
print(df.head())

# Clean the 'language' column by removing invalid entries
df = df[df['language'].notna()]  # Remove rows where 'language' is NaN
df = df[df['language'] != 'Language not found']  # Remove rows with 'Language not found'

# Debugging: Print the cleaned DataFrame
print("\nCleaned DataFrame:")
print(df.head())

# Extract the 'language' column and count occurrences
language_counts = df['language'].value_counts()

# Debugging: Print the language counts
print("\nLanguage Counts:")
print(language_counts)

# Generate the lists
labels = replace_long_items(language_counts.index.tolist())
sizes = language_counts.values.tolist()

# Debugging: Print the labels and sizes
print("\nLabels and Sizes:")
print("Labels:", labels)
print("Sizes:", sizes)

# Generate a list of colors with the same length as the number of languages
num_languages = len(labels)
colors = plt.get_cmap('tab10').colors  # Using a colormap with distinct colors

# Ensure colors list is the same length as labels
if len(colors) < num_languages:
    colors = colors * (num_languages // len(colors) + 1)
colors = colors[:num_languages]

# Convert colors to hex format
colors_hex = [mcolors.to_hex(c) for c in colors]

# Print the results
print("\nColors:")
print(colors_hex)
