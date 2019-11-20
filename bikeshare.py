"""This program provides bikeshare statistics for 3 US cities."""

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    invalid = True
    while invalid:
        city = input('Enter the city for which you would like bikeshare info (Chicago, New York City, or Washington): ')
        city = city.lower()
        if city!='chicago' and city!='new york city' and city!='washington':
            print('\nYou\'ve entered an invalid city. Please enter one of Chicago, New York City, or Washington.')
        else:
            invalid = False

    # TO DO: get user input for month (all, january, february, ... , june)
    invalid = True
    while invalid:
        month = input('Enter the month (January through June) for which you would like the bikeshare info, or \'all\' for all months: ')
        month = month.lower()
        if month!='january' and month!='february' and month!='march' \
        and month!='april' and month!='may' and month!='june' and month!='all':
            print('\nYou\'ve entered an invalid month. Try again.')
        else:
            invalid = False

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    invalid = True
    while invalid:
        day = input('Enter the day of the week (full word) for which you would like the bikeshare info, or \'all\' for all days: ')
        day = day.lower()
        if day!='monday' and day!='tuesday' and day!='wednesday' and day!='thursday' \
        and day!='friday' and day!='saturday' and day!='sunday' and day!='all':
            print('\nYou\'ve entered an invalid day of the week. Try again.')
        else:
            invalid = False

    print('-'*40)
    return city, month, day # These are now all lowercase in the rest of the code


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
    # load data file into a dataframe
    filename = CITY_DATA[city.lower()]
    df = pd.read_csv(filename)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month #gives month number
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    df['start_hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
    
        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]

    return df

def print_raw_data(df):
    num_rows = df.shape[0]
    #print('Number of rows is {}'.format(num_rows))
    see_raw_data = input('\nWould you like to see 5 lines of the raw data? Enter yes or no: ')
    see_raw_data = see_raw_data.lower()
    while see_raw_data!='no':
        if see_raw_data=='yes':
            print(df.iloc[:5])
            s=5
            while see_raw_data!='no':
                see_raw_data = input('\nWould you like to see 5 more lines of the raw data? Enter yes or no: ')
                see_raw_data = see_raw_data.lower()
                if see_raw_data!='yes' and see_raw_data!='no':
                    print('\nInvalid response. Please enter yes to see 5 more lines, or no to continue. ')
                elif see_raw_data=='yes':
                    if s+5>num_rows: #if user tries to go past available rows
                        print('This is the end of the file. Displaying rest of data.')
                        print(df.iloc[s:])
                        see_raw_data = 'no' # quit
                    else:
                        print(df.iloc[s:s+5])
                        s += 5
    print('-'*40)
                        
def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if month == 'all': # doesn't make sense to display the most popular month if we've filtered to only one month
        popular_month = df['month'].mode()[0] # this returns a number now
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        print('The most popular month for bike rentals in this city on the requested day(s) is {}.'.format(months[popular_month-1].title()))

    # TO DO: display the most common day of week
    if day == 'all': # doesn't make sense to display the most popular day of week if we've filtered to only one day
        popular_day = df['day_of_week'].mode()[0] # this returns a capitalized string
        print('The most popular day of the week for bike rentals in this city in the requested month(s) is {}.'.format(popular_day))

    # TO DO: display the most common start hour
    popular_time = df['start_hour'].mode()[0] # this returns a capitalized string
    print('The most popular starting hour for bike rentals in this city during the requested month(s)/day(s) is {}.'.format(popular_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most popular origin for bike rentals in this city during the requested month(s)/day(s) is {}.'.format(popular_start_station))    

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most popular destination for bike rentals in this city during the requested month(s)/day(s) is {}.'.format(popular_end_station))  

    # TO DO: display most frequent combination of start station and end station trip
    #print(df[['Start Station','End Station']].mode()[0]) #*******************************************************
    #sub = df[['Start Station','End Station']]
    df['Route'] = df['Start Station'] + ' to ' + df['End Station']
    #print(df.iloc[:20])
    popular_combo_station = df['Route'].mode()[0]
    print('The most popular trip taken for bike rentals in this city during the requested month(s)/day(s) is {}.'.format(popular_combo_station))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('The total travel time (rounded to nearest hour) for the requested month(s)/day(s) for bike rentals in this city is {} hours.'
          .format(int(round(df['Trip Duration'].sum()/60/60))))

    # TO DO: display mean travel time
    print('The average travel time (rounded to nearest minute) for the requested month(s)/day(s) for bike rentals in this city is {} minutes.'
          .format(int(round(df['Trip Duration'].mean()/60))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('The following is the count of the different user types renting bikes in this city during the requested month(s)/day(s):\n{}\n'
          .format(df['User Type'].value_counts()))

    if city=='chicago' or city=='new york city':
        # TO DO: Display counts of gender
        print('The following is the count of the genders renting bikes in this city during the requested month(s)/day(s):\n{}\n'
              .format(df['Gender'].value_counts()))

        # TO DO: Display earliest, most recent, and most common year of birth
        print('The oldest person who rented bikes in this city during the requested month(s)/day(s) was born in {}.'
              .format(int(df['Birth Year'].min())))
        print('The youngest person who rented bikes in this city during the requested month(s)/day(s) was born in {}.'
              .format(int(df['Birth Year'].max())))
        print('The most common birth year for people who rented bikes in this city during the requested month(s)/day(s) is {}.'
              .format(int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        print_raw_data(df)
        
        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes to restart: ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
