import time
import pandas as pd
import numpy as np
from colorama import init, Fore

init()

CITY_DATA = {
    'chicago': 'C:/Users/A.Seery/Documents/chicago.csv',
    'new york city': 'C:/Users/A.Seery/Documents/new_york_city.csv',
    'washington': 'C:/Users/A.Seery/Documents/washington.csv'}

months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print(Fore.GREEN + 'Hello! Let\'s explore some US bikeshare data!' + Fore.RESET)
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    while True:
        city = input(Fore.GREEN +'Enter city name (chicago, new york city, or washington ): ' + Fore.RESET).lower()
        if city in CITY_DATA:
            break
        else:
            print(Fore.GREEN +'Invalid city name. Please try again.'+ Fore.RESET)

    # get user input for month (all, january, february, ... , june)
    
    while True:
        month = input(Fore.GREEN +'Enter month (all, january, february, ... , june): '+ Fore.RESET).lower()
        if month in months:
            break
        else:
            print(Fore.GREEN +'Invalid month. Please try again.'+ Fore.RESET)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    
    while True:
        day = input(Fore.GREEN +'Enter day of week (all, monday, tuesday, ... , sunday): '+ Fore.RESET).lower()
        if day in days:
            break
        else:
            print(Fore.GREEN +'Invalid day. Please try again.'+ Fore.RESET)

    print('-'*40)
    return city, month, day


    
def load_data(city, month, day):
    """ Reference: The content in the CVS files needs converting as its imported as a string found this on how to and why 
    https://www.geeksforgeeks.org/python-pandas-to_datetime/
    
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load data for the selected city
    df = pd.read_csv(CITY_DATA[city])

    # Convert the 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day_of_week from 'Start Time' and create new columns
    df['month'] = df['Start Time'].dt.month 
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()

    # Filter by month if applicable
    if month != 'all':
        month_number = months.index(month)
        df = df[df['month'] == month_number]

    # Filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df

    
def time_stats(df):
    """Displays statistics on the most frequent times of travel. 
    Referenced pandas.Series.mode
    found here https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.mode.html
    This does not consider null entries."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('Most common month:', months[common_month].title())

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most common day of week:', common_day.title())

    # display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    common_start_hour = df['start_hour'].mode()[0]
    print('Most common start hour:', common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
  
    commonly_used_station = df['Start Station'].mode()[0]
    print('Most common start station:', commonly_used_station)

    
    # display most commonly used end station
    commonly_used_station = df['End Station'].mode()[0]
    print('Most common end station:', commonly_used_station)

    # display most frequent combination of start station and end station trip
    df['start_end_combined'] = df['Start Station'] + ' to ' + df['End Station']
    common_combination = df['start_end_combined'].mode()[0]
    print('Most frequent combination of start station and end station trip:', common_combination)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


   
def trip_duration_stats(df):
    """ Displays statistics on the total and average trip duration.
    Refernce: how divmod works https://www.geeksforgeeks.org/divmod-python-application/ """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_hours, remainder = divmod(total_travel_time, 3600)
    total_minutes, total_seconds = divmod(remainder, 60)
    rounded_seconds = round(total_seconds)  # Added for readability Round the seconds to the nearest whole number
    print('Total travel time: {} hours, {} minutes, and {} seconds'.format(total_hours, total_minutes, rounded_seconds))
    

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_hours, remainder = divmod(mean_travel_time, 3600)
    mean_minutes, mean_seconds = divmod(remainder, 60)
    rounded_seconds = round(mean_seconds) 
    print('Average travel time: {} hours, {} minutes, and {} seconds'.format(mean_hours, mean_minutes, rounded_seconds))

   
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts().to_string()
    print('User types:\n', user_types)
    
    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts().to_string()
        print('\nCounts of gender:\n', gender_counts)
    else:
        print('\nGender data not available for this city.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])

        print('\nEarliest year of birth:', earliest_birth_year)
        print('Most recent year of birth:', most_recent_birth_year)
        print('Most common year of birth:', most_common_birth_year)
    else:
        print('\nBirth year data not available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)




def display_raw_data(df):
    """
    Function below displays 5 rows of raw data from the DataFrame upon user request. 
    It will keep displaying the next 5 rows as long as the user keeps entering 'yes' or mistypes.
    Displays 5 rows of raw data upon user request."""
    
    index = 0
    display_data = input('\nWould you like to view the first 5 rows of raw data? Enter yes or no.\n').lower()

    while display_data == 'yes':
        print(df.iloc[index:index + 5])
        index += 5

        display_data = input('\nWould you like to view the next 5 rows of raw data? Enter yes or no.\n').lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

"""
Block below ensures that the main() function is 
only called when the script is run directly and not when it is imported as a module
 """

if __name__ == "__main__":
	main()
