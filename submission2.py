import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv'}

def get_filters():
    """
    To ask user to input a city, month and day to show their data

    returns:
    (str) city - name of the city
    (str) month - selecting a month or 'all'
    (str) day - selecting a day or 'all'
    """
    print('Hello! let\'s explore some US bikeshare data!')

    # getting user input for city

    city = input('Please select a city from: Chicago, New York City, Washington: ').lower()
    while city not in (CITY_DATA.keys()):
        print('Provided city is not available, please to choose from the given')
        city = input('Please select a city from: Chicago, New York City, Washington: ').lower()

    # getting user input for month

    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input('Please provide a month between January and June or type all to select all: ').lower()
        if month not in months:
            print('Please provide a month from the given')
            continue
        else:
            break

    # getting user input for days
    days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']
    day = input("Please to provide a day of the week or all: ").lower()
    while day not in days:
        print('Please to provide a valid day!')
        day = input("Please to provide a day of the week or all: ").lower()
    else:
        day = 'all'


    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """"
    Loading the data for a specific city and filtering by month and day if applicable.

    Arguments Taken:
        (str) city
        (str) month
        (str) day

    return:
    df - a pandas DataFrame
    """

    #loading data to DataFrame
    df = pd.read_csv(CITY_DATA[city])

    #converting Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])


    # exctracting month and day of week from Start Time and create new month and day columns
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day_name()

    # month filter -if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month] #added in submission 2 after reviewer comment.. this to create a new df for the selected month

    # days filter -if applicable
    # changed the day filteration code in submission 2 to be matching the same logic of months filteration
    if day != 'all':
        days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        day = days.index(day) + 1

        df = df[df['day'] == day]

    return df

def time_stats(df):
    """Displaying Statistics on the most frequents."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # the most common month

    #months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = df['month'].mode()[0]
    print('The Most common month for travel is:', month)


    # the most common day of the week
    day = df['day'].mode()[0]
    print('The Most common day for travel is:', day)

    # the most common hour

    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('The Most common hour is:', common_hour)


    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """"Displaying statistics about stations"""
    print('\nCalculating The Most visitid stations and Trips stats ...\n')
    start_time = time.time()

    # common start point
    com_sp = df['Start Station'].value_counts()
    print('The most common start station is:', com_sp.index.max())

    # common end point
    com_ep = df['End Station'].value_counts()
    print('The most common end station is:', com_ep.index.max())

    #common combination of start and end points
    df['com start-end stations'] = df['Start Station'] + " & " + df['End Station'] # a new column to combine start & end stations
    com_comb = df['com start-end stations'].mode()[0] # generating the most repeating combination across all
    print('The most common combination of start and end stations is:\n',com_comb)

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):


    """Displaying statistics about trips durations"""

    print('\nCalculating The Trip Duration Statistics...\n')
    start_time = time.time()


    #total travel time

    tt_time = sum(df['Trip Duration'])
    print('The Total Time Traveled is : ', (tt_time//86400)/30, 'Days') #converting to days

    #longest trip
    lt_time = df['Trip Duration'].max()

    #longest_trip = df['ttime'].max()
    print('Longest trip took: ', lt_time//(60*60), 'Hour(s)' ) #converting to hours

    #shortest trip

    st_time = df['Trip Duration'].min()
    print('Shortest trip took:', (st_time % 1440)/60 , 'Minute(s)') # converting to minutes

    # avg trip duration
    avg_time = df['Trip Duration'].mean() # extracting average
    print('The Average Trip Duration were: ', avg_time/60, 'Hour(s)') #average converted to hours


    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displaying Statistics about Bike Share users"""
    print('\nCalculation Users Statistics...\n')
    start_time = time.time()

    #df['Birth Year'] = pd.to_datetime(df['Birth Year'])
    # counts of user types
    print(df['User Type'].value_counts())

    # Gender Counting
    if 'Gender' in (df.columns):
        print(df['Gender'].value_counts())
    else:
        print('Sorry! No Gender data')

    # earliest, most recent and most common users bearth years
    if 'Birth Year' in (df.columns):
        year = df['Birth Year']
        print('Earliest User(s) were born in: ', int(year.min()), '\nMost recent is: ', int(year.max()), '\nAnd Most Common birth year is:', int(year.mode()[0]))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def show_data(df):

    """ Asking user for the desire to view the used raw data """
    sample = 0
    Q_for_User = input('Would you like to view sample of the raw data? (y/n) ').lower()

    if Q_for_User.lower() == 'y':
        print(df[sample : sample +5])
        sample += 5
    else:
        return


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
