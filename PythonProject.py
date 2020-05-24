import time
import pandas as pd
import numpy as np
import sys

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    cities = ['Chicago','New York City','Washington']
    months = ['January','February','March','April','May','June','All']
    days_of_week = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','All']

    # Get user input for city (chicago, new york city, washington)   
    while True:
        city = input('Which city would you like to see data from: Chicago, Washington or New York City? ').title()
        if city.title() in cities: 
            break
        else:
            print('Try writing a city exactly as above')    
   
                                                                     
    # Get user input for month (all, january, february, ... , june)  
    while True:
        month = input('Which month? January, February, March, April, May, June or All?: ').title()
        if month.title() in months:
            break
        else:
            print('Sorry, that appears to be an invalid month, check for spelling!')

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Choose a day of the week (i.e Monday, Tuesday, All...): ').title()
        if day.title() in days_of_week:
            break
        else:
            print('Sorry, it appears that\'s not a valid day, please try again')


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])

    # Convert the dates from strings to types
     
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    if month != 'All':
        months = ['January','February','March','April','May','June']
        month = months.index(month) + 1
        df = df[df['month'] == int(month)]
    if day != 'All':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Display the most common month
    df['Month'] = df['Start Time'].dt.month
    popular_month = df['Month'].mode().iloc[0]
    print('Most popular month: ', popular_month)

    # Display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.day_name()
    popular_day = df['day_of_week'].mode().iloc[0]
    print('Most popular day of the week: ', popular_day)

    # Display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    popular_hour = df['Hour'].mode().iloc[0]
    print('Most popular hour: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    df['PopularStart'] = df['Start Station']
    popular_start = df['PopularStart'].mode().iloc[0]
    print('The most popular starting station is: ', popular_start)

    # Display most commonly used end station
    df['PopularEnd'] = df['End Station']
    popular_end = df['PopularEnd'].mode().iloc[0]
    print('The most popular end station is: ', popular_end) 

    # Display most frequent combination of start station and end station trip
    popular_trip = df['PopularStart'] + ' to ' + df['PopularEnd']
    print('The most popular trip is: ', popular_trip.mode()[0])
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    trip_startingtime = pd.to_datetime(df['Start Time'])
    trip_endtime = pd.to_datetime(df['End Time'])
    df['travel_time'] = trip_endtime - trip_startingtime

    total_travel_time = df['travel_time'].sum()
    print('The total amount of travel time is: ', total_travel_time)
    

    # Display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print('The average amount of time per trip is: ', avg_travel_time, 'seconds')



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    # As Washington doesn't have information on the gender and birth year of it's users, some if-else statements are in order
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_counted = df['User Type'].value_counts()
    print('User type count: ', user_types_counted)

    # Display counts of gender
    if 'Gender' in df.columns:
        genders_counted = df['Gender'].value_counts()
        print('\nCount by user\'s gender: ', genders_counted)
    else:
        print('\nWashington doesn\'t have information on the user\'s gender')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year_birth = df['Birth Year'].min()
        most_recent_year_birth = df['Birth Year'].max()
        common_year_birth = df['Birth Year'].mode()[0]

        print('\nThe earliest year of birth of a user was: ', earliest_year_birth)
        print('The most recent year of birth for a user was: ', most_recent_year_birth)
        print('The most common year of birth was: ', common_year_birth)
    else:
        print('\nWashington doesn\'t have information on the user\'s year of birth')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_additional_data(df):
    """
    Displays 5 rows of raw data at a time through pagination
    """
    prev = 0
    while True:
        data_display = input('Do you wish to see five rows of raw data? (Yes or No): ')
        if data_display == 'Yes' or data_display == 'yes':
            print(df.iloc[prev: prev + 5])
            prev += 5
            print('-'*40)
        elif data_display == 'No' or data_display == 'no':
            break
        else:
            print('Please type yes or no')

def main():
    restart = 'yes'
    while True:
        if restart == 'yes':
            city, month, day = get_filters()
            df = load_data(city, month, day)

            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_additional_data(df)

            while True:
                restart = input('\nWould you like to restart? Enter yes or no.\n')
                if restart.lower() != 'yes' and restart.lower() != 'no':
                    print('Please type yes or no')
                elif restart.lower() == 'yes':
                    break
                else:
                    restart = 'no'
                    break
        else:
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\nProgram interrupted, now closing')
        sys.exit(0)

    