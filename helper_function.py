import pandas as pd
import re
import datetime
import seaborn as sns
import matplotlib.pyplot as plt

def imp_shark(url):
    """
    The function reads the data from the given URL and returns a DataFrame.
    Parameters:
        url (str): The URL to read the data from.
    Returns:
        pd.DataFrame: The loaded DataFrame.
    """
    pd.set_option('display.max_columns', None)
    shark_df = pd.read_excel(url)
    return shark_df

def clean_data(shark_df):
    """
    Cleans the given DataFrame by dropping unnecessary columns, handling missing values,
    and standardizing certain values.
    Parameters:
        shark_df (pd.DataFrame): The DataFrame to clean.
    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    # Drop unnecessary columns
    shark_df = shark_df.drop(columns=['Name', 'pdf', 'Unnamed: 11', 'href formula', 'href', 'Case Number', 'Case Number.1', 'original order', 'Source', 'Unnamed: 21', 'Unnamed: 22'])

    # Drop rows with all NA values
    shark_df = shark_df.dropna(how='all')

    # Drop duplicates
    shark_df = shark_df.drop_duplicates()

    # Standardize gender values
    gender_mapping = {
        'F': 'F',
        'lli': 'F',
        'M': 'M',
        'N': 'M',
        ' M': 'M',
        'M x 2': 'M',
        '.': 'F',
        'M ': 'M'
    }
    shark_df['Sex'] = shark_df['Sex'].replace(gender_mapping)

    # Drop columns not needed for analysis
    shark_df = shark_df.drop(columns=["Species ", "Location", "Date"])

    # Handle missing values in 'Year' and convert to int
    shark_df = shark_df.dropna(subset=['Year'])
    shark_df['Year'] = shark_df['Year'].astype(int)

    # Map 'Type' values
    type_mapping = {
        'Unprovoked': 'Unprovoked',
        'Provoked': 'Provoked',
        'Invalid': 'Others',
        'Watercraft': 'Others',
        'Sea Disaster': 'Others',
        'Questionable': 'Others'
    }
    shark_df['Type'] = shark_df['Type'].map(type_mapping)

    # Convert 'Time' column to strings
    shark_df['Time'] = shark_df['Time'].astype(str)

    # Filter out invalid time formats
    shark_df = shark_df[shark_df['Time'].str.match(r'^\d{1,2}h\d{2}$')]

    # Categorize 'Time' values
    shark_df['Time'] = shark_df['Time'].apply(categorize_time)
    shark_df = shark_df.dropna(subset=['Time'])

    # Slice and handle 'Age' values
    df_shark_sliced_age = shark_df.iloc[:1000]
    df_shark_sliced_age['Age'] = pd.to_numeric(df_shark_sliced_age['Age'], errors='coerce')
    df_shark_sliced_age['Age'] = df_shark_sliced_age['Age'].fillna(df_shark_sliced_age['Age'].mean())
    df_shark_sliced_age = df_shark_sliced_age.drop(columns='Age')

    return df_shark_sliced_age

def check_str(main_string, search_string):
    """
    Checks if the main_string exists within search_string.
    Parameters:
        main_string (str): The string to search for.
        search_string (str): The string to search within.
    Returns:
        bool: True if main_string is found within search_string, False otherwise.
    """
    return bool(re.search(main_string.lower(), str(search_string).lower()))

def visualize_top5_countries(shark_df):
    """
    Visualizes the top 5 attacked countries as a pie chart.
    Parameters:
        shark_df (pd.DataFrame): The DataFrame to visualize.
    """
    top5_countries = ['USA', 'AUSTRALIA', 'SOUTH AFRICA', 'NEW ZEALAND', 'BAHAMAS']
    top5_countries_df = shark_df[shark_df['Country'].isin(top5_countries)]
    country_counts = top5_countries_df['Country'].value_counts()
    plt.figure(figsize=(8, 6))
    plt.pie(country_counts, labels=country_counts.index, autopct='%1.1f%%', colors=sns.color_palette("viridis", len(country_counts)))
    plt.title("Top 5 Attacked Countries")
    plt.show()

def visualize_attacks_last_24_years(shark_df):
    """
    Visualizes the number of attacks in the last 24 years.
    Parameters:
        shark_df (pd.DataFrame): The DataFrame to visualize.
    """
    filtered_years_df = shark_df[(shark_df['Year'] >= 2000) & (shark_df['Year'] <= 2024)]
    plt.figure(figsize=(10, 6))
    sns.histplot(filtered_years_df['Year'], bins=25, color='red').set_title("Attacks in the Last 24 Years")
    plt.show()

def visualize_attacks_by_sex(shark_df):
    """
    Visualizes the number of attacks by sex.
    Parameters:
        shark_df (pd.DataFrame): The DataFrame to visualize.
    """
    plt.figure(figsize=(8, 6))
    sns.countplot(x='Sex', data=shark_df, palette='pastel').set_title("Attacks by Sex")
    plt.show()

def visualize_attacks_by_time(shark_df):
    """
    Visualizes the number of attacks by time of day as a pie chart.
    Parameters:
        shark_df (pd.DataFrame): The DataFrame to visualize.
    """
    time_counts = shark_df['Time'].value_counts()
    plt.figure(figsize=(8, 6))
    plt.pie(time_counts, labels=time_counts.index, autopct='%1.1f%%', colors=sns.color_palette("muted", len(time_counts)))
    plt.title("Attacks by Time of Day")
    plt.show()

def categorize_time(time_str):
    """
    Categorizes the given time string into morning, afternoon, evening, or night.
    Parameters:
        time_str (str): The time string to categorize.
    Returns:
        str: The category of the time.
    """
    try:
        # Define the input format
        input_format = "%Hh%M"
        
        # Parse the time string into a datetime object
        time_obj = datetime.datetime.strptime(time_str, input_format)
        
        # Extract the hour from the datetime object
        hour = time_obj.hour
        
        # Categorize based on hour
        if 0 <= hour < 5:
            return "Night"
        elif 6 <= hour < 12:
            return "Morning"
        elif 12 <= hour < 18:
            return "Afternoon"
        elif 18 <= hour < 21:
            return "Evening"
        elif 21 <= hour <= 23:
            return "Night"
        else:
            return "Night"
    except ValueError:
        return "Night"
