""" This Application supply statistical information about BikeShare"""
""" Developed By Ramatan,  MZ,  www.Ramatan.com  """

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new_york_city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

#############
# function: start application
def main():
    while True:
         print("Welcome! you can use my application to get statistical information about BikeShare Activities.\n")
         print("Please Read and select carefully to get the required information.\n")
         # user selection part : first choose city , month , day
         # selected_city_data = select_city()
         # df = load_city_data(selected_city_data)
         city, month, day = get_filters()
         print('The data filtered with the following, city: {}, month: {}, day: {}'.format(city, month, day))
         df = load_data(city, month, day)
         ##print(df.head())
         # call first function to show time stats
         # time stats
         try:
             time_stats(df)
         except:
            print('Data Not valid for time stats calcs.')
            #break
         # station state
         try:
            station_stats(df)
         except:
            print('Data Not valid for station stats calcs.')
            #break
         try:
            trip_duration_stats(df)
         except:
            print('Data Not valid for trip duration stats calcs.')
            #break
         try:
            user_stats(df)
         except:
            print('Data Not valid for user stats calcs.')
            #break

         restart = input('\nWould you like to restart? Enter yes or no.\n')
         if restart.lower() == 'no':
             break
         elif restart.lower() == 'yes':
             print('\nWelcome again, start your selections.\n')
         else:
             print('\n yes or no please.\n')


###########
# function: to select city
def select_city():
    """Asks the user for a city and returns selected city to filter function.
    Args: none.
    Returns: (string) selected city,
    and give user the chance to confirm selection before move to next one.
    """
    city = input('\nBikeshare data available for the following cities, \n'
                 '\nPlease select city you want: Chicago (CH), New York (NY), or Washington (WA)?\n')

    city = city.lower()

    while True:
        if city == "ny" or city == "new york":
            print('\nYou chose New York City! We\'re going to explore its bikeshare data\n')
            if input("are you sure about your selection? (y/n)") == "y":
               return 'new_york_city'
        if city == "ch" or city == "chicago":
            print('\nYou chose Chicago! We\'re going to explore its bikeshare data\n')
            if input("are you sure about your selection? (y/n)") == "y":
              return 'chicago'
        elif city == "wa" or city == "washington":
            print('\nYou chose Washington! We\'re going to explore its bikeshare data\n')
            if input("are you sure about your selection? (y/n)") == "y":
               return 'washington'
        city = input("Please choose between Chicago (CH), New York (NY), or Washington (WA)")
        city = city.lower()

######################################
###########
# function: to select month
def select_month():
    """Asks the user for a month and returns to filter function with selected month.
    Args: none.
    Returns: (string) selected month,
    and give user the chance to confirm selection before move to next one.
    """
    month = input('\nBikeshare data available for the following months, \n'
                 '\n 0:all, 1:january, 2:february, 3:march, 4:april, 5:may, 6:june, 7:july, 8:august, 9:september, 10:october, 11:november, 12:december \n')

    month = month.lower()

    while True:
        if month == "all" or month in MONTHS:
            print("\nYou chose {} We\'re going to next selection\n".format(month) )
            if input("are you sure about your selection? (y/n)") == "y":
               return month
            else:
                month = input("Please choose Valid Input")
        month = month.lower()

######################################
###########
# function: to select week day
def select_week_day():
    """Asks the user for a week day and returns to filter function with selected day.
    Args: none.
    Returns: (string) selected day,
    and give user the chance to confirm selection before move to next one.
    """
    day = input('\n You can select week day or select all, \n'
                  '\n 0:all, 1:sunday, 2:monday, 3:tuesday, 4:wednesday, 5:thursday, 6:friday, 7:saturday \n')

    day = day.lower()

    while True:
        if day == "all" or day in DAYS:
            print("\nYou chose {} We\'re going to show statistics for your selection.\n".format(day) )
            if input("are you sure about your selection? (y/n)") == "y":
               return day
            else:
                day = input("Please choose Valid Input")
        day = day.lower()
################################################
def load_data(city, month, day):
    """
    Reads the city file name and loads it to a dataframe
    Args:
    city - path to the file as a string
    Returns:
    df - dataframe to hold data for later processing
    """
    print('\nLoading the data...\n')
    #df = pd.read_csv(city)
    df = pd.read_csv(CITY_DATA[city])

    #add datetime format to permit easy filtering
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['month'] = df['Start Time'].dt.month
    df["day_of_month"] = df["Start Time"].dt.day
    # print(df.head(5))
    # extract month and day of week and hour from Start Time to create new columns
    #df['month'] = df['Start Time'].dt.month
    #df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        month =  MONTHS.index(month) + 1
        df = df[ df['month'] == month ]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[ df['day_of_week'] == day.title()]

    return df
#######################
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Args: none
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = select_city()

    # get user input for month (all, january, february, ... , june)

    month = select_month()
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day =select_week_day()

    #print('-'*40)
    return city, month, day
##############################################
## function
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].value_counts().idxmax()
    print("The most common month is :", most_common_month)

    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].value_counts().idxmax()
    print("The most common day of week is :", most_common_day_of_week)

    # display the most common start hour
    most_common_start_hour = df['hour'].value_counts().idxmax()
    print("The most common start hour is :", most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
############
## function
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].value_counts().idxmax()
    print("The most commonly used start station :", most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].value_counts().idxmax()
    print("The most commonly used end station :", most_common_end_station)

    # display most frequent combination of start station and end station trip
    most_common_start_end_station = df[['Start Station', 'End Station']].mode().loc[0]
    print("The most commonly used start station and end station : {}, {}"\
            .format(most_common_start_end_station[0], most_common_start_end_station[1]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#########################################
# function
##################
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print("Total travels time: ", total_travel)


    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print("Mean travel time: ", mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
#####################################
# function
#####################
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of user types:\n")
    user_counts = df['User Type'].value_counts()
    for index, user_count in enumerate(user_counts):
        print("  {}: {}".format(user_counts.index[index], user_count))

    print()

    # Display counts of gender
    if 'Gender' in df.columns:
       print("Counts of gender:\n")
       gender_counts = df['gender'].value_counts()
       for index,gender_count   in enumerate(gender_counts):
            print("  {}: {}".format(gender_counts.index[index], gender_count))
    print()


    # Display earliest, most recent, and most common year of birth
    birth_year = df['Birth Year']
    # the most common birth year
    most_common_year = birth_year.value_counts().idxmax()
    print("The most common birth year:", most_common_year)
    # the most recent birth year
    most_recent = birth_year.max()
    print("The most recent birth year:", most_recent)
    # the most earliest birth year
    earliest_year = birth_year.min()
    print("The most earliest birth year:", earliest_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
###############################################
######### App Start
if __name__ == "__main__":
	main()
