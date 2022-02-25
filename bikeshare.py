"""
@author: Marion JACQUET
github profile : m-jacquet
"""

import time
import pandas as pd


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }



def check_data_entry(prompt, valid_entries): 
    """
    Asks user to type some input and verify if the entry typed is valid.
    Since we have 3 inputs to ask the user in get_filters(), it is easier to write a function.
    Args:
        (str) prompt - message to display to the user
        (list) valid_entries - list of string that should be accepted 
    Returns:
        (str) user_input - the user's valid input
    """
    try:
        user_input = str(input(prompt)).lower()
    
        while user_input not in valid_entries : 
            print('Sorry... it seems like you\'re not typing a correct entry.')
            print('Let\'s try again!')
            user_input = str(input(prompt)).lower()
        
        print('Great! the chosen entry is: {}\n'.format(user_input))
        return user_input
    
    except:
        print('Seems like there is an issue with your input')



def get_filters(): 
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('Hi there! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    valid_cities = CITY_DATA.keys()
    prompt_cities = 'Please choose one of the 3 cities (chicago, new york city, washington): '
    city = check_data_entry(prompt_cities, valid_cities)
      
    
    # get user input for month (all, january, february, ... , june)
    valid_months = ['all','january','february','march','april','may','june']
    prompt_month = 'Please choose a month (all, january, february, ... , june): '
    month = check_data_entry(prompt_month, valid_months)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = ['all','monday','tuesday','wednesday','thursday','friday','saturday', 'sunday']
    prompt_day = 'Please choose a day (all, monday, tuesday, ... sunday): '
    day = check_data_entry(prompt_day, valid_days)


    print('-'*40)
    return city, month, day



def load_data(city, month, day): # DONE
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    # read the input file
    try:
        df = pd.read_csv(CITY_DATA[city])
    except:
        print('Erm, seems like the file cannot be read...')
        return 
    
     # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['week_day'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month']== month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['week_day'] == day.title()]

    return df



def time_stats(df, city, month, day): 
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel with the filters (city =', city,'; month =', month, '; day =', day, ') ...\n')

    start_time = time.time()
    
    
    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most common month: ', popular_month)

    # display the most common day of week
    popular_week_day = df['week_day'].mode()[0]
    print('Most common day of the week: ', popular_week_day)


    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour 
    popular_hour = df['hour'].mode()[0]
    print('Most common start hour: ', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df, city, month, day):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip with the filters (city =', city,'; month =', month, '; day =', day, ') ...\n')
    start_time = time.time()
    
    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most common start station: ', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most common end station: ', popular_end_station)


    # display most frequent combination of start station and end station trip
    df['Trip from - to'] = df['Start Station'] + ' - ' + df['End Station']
    popular_trip = df['Trip from - to'].mode()[0]
    print('Most common trip: ', popular_trip)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df, city, month, day):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration with the filters (city =', city,'; month =', month, '; day =', day, ') ...\n')
    start_time = time.time()
   

    # display total travel time
    print('Total travel time: ', df['Trip Duration'].sum())

    # display mean travel time
    print('Average travel time: ', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df, city, month, day):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats with the filters (city =', city,'; month =', month, '; day =', day, ') ...\n')
    start_time = time.time()
    
    
    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nTypes of users:')
    print(user_types)
    if df['User Type'].isnull().sum() != 0 :
        print('Please note there was ', df['User Type'].isnull().sum(), ' unknown values.')

    # Display counts of gender
    if city == 'washington':
        print('\nGenders: no gender data available for washington')
    else: 
        genders = df['Gender'].value_counts()
        print('\nGenders:')
        print(genders)
        if df['Gender'].isnull().sum() != 0 :
            print('Please note there was ', df['Gender'].isnull().sum(), ' unknown values.')
        
    # Display earliest, most recent, and most common year of birth
    if city == 'washington':
        print('\nYears of birth: no birth data available for washington')
    else: 
        print('\nYears of birth:')
        print('Earliest year of birth: ', int(df['Birth Year'].min()))
        print('Latest year of birth: ', int(df['Birth Year'].max()))
        print('Average year of birth: ', int(df['Birth Year'].mode()[0]))
        if df['Birth Year'].isnull().sum() != 0 :
            print('Please note there was ', df['Birth Year'].isnull().sum(), ' unknown values.')
            
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def display_details(df):
    """
    Displays details of the dataset, 5 lines at a time.
    When we reach the last lines of the table, we display the remaining ones (might be less than 5 lines)
    """
    raw_data_input = input('Would you like to see 5 lines of raw data (yes/no)? ')
    
    if raw_data_input.lower()  == 'yes' :
        print('\nDisplaying raw data...\n')
        print('Current data set has a total of ', len(df), ' rows.\n')
        more_details = 'yes'
        i = 0
        while more_details.lower() == 'yes' and i + 5 <= len(df):
            print(df.iloc[i:i +5])
            more_details = input('\nDo you wish to see more details (yes/no)? ')
            i += 5
            
        # Displaying the last rows if the length of the df is not a multiple of 5
        if len(df) % 5 != 0  and more_details.lower() == 'yes' :
            print('Ok, these are the last rows:\n')
            print(df.iloc[i:len(df)])
            
        print('-'*40)



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, city, month, day)
        station_stats(df, city, month, day)
        trip_duration_stats(df, city, month, day)
        user_stats(df, city, month, day)
        display_details(df)

        restart = input('\nWould you like to restart? (yes/no): ')
        if restart.lower() != 'yes':
            break



if __name__ == "__main__":
	main()
    
    
