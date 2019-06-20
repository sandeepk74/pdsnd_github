import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'nyc': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_LIST = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']

DAY_LIST = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city_question = input('\nWould you like to see data for Chicago, NYC or Washington?\n')
        if city_question.lower() != 'chicago' and city_question.lower() != 'nyc' and city_question.lower() != 'washington':
            print("Invalid input, please try again.")
        else:
            city = city_question.lower()
            break

    month = 0
    day = 0
    
    # get user input for month (all, january, february, ... , june)
    while True:
        month_question = input('\nWould you like to filter data by month? Enter y or n\n')
        if month_question.lower() != 'y' and month_question.lower() != 'n':
            print("Invalid input, please try again.")
        else:
            if month_question.lower() == 'y':
                while True:
                    which_month = input('\nWhich month? Enter Jan, Feb, Mar, Apr, May or Jun\n')
                    if which_month.lower() not in MONTH_LIST:
                        print("Invalid month, please try again.")
                    else:
                        month = MONTH_LIST.index(which_month.lower()) + 1
                        break                    
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day_question = input('\nWould you like to filter data by day of the week? Enter y or n\n')
        if day_question.lower() != 'y' and day_question.lower() != 'n':
            print("Invalid input, please try again.")
        else:
            if day_question.lower() == 'y':
                while True:
                    which_day = input('\nWhich day? Enter Mon, Tue, Wed, Thu, Fri, Sat or Sun\n')
                    if which_day.lower() not in DAY_LIST:
                        print("Invalid day, please try again.")
                    else:
                        day = DAY_LIST.index(which_day.lower()) + 1
                        break                    
            break

    print("Filters selected are %s, %d, %d" %(city, month, day))

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

    filename = CITY_DATA[city]
    # print(filename)
    df = pd.read_csv(filename)

    # Filtering data based on user inputs
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # print(df['month'].head())
    # print(df['day_of_week'].head())

    if month != 0:
        df = df.loc[df['month'] == month]

    if day != 0:
        df = df.loc[df['day_of_week'] == day]

    # print(df.shape)

    # Gives user an option to go through filtered raw data, 5 lines at a time. 
    raw_count = 0
    while True:
        if raw_count == 0:
            raw_data_question = input('\nWould you like to see raw data? Enter y or n.\n')
        else:
            raw_data_question = input('\nWould you like to see more raw data? Enter y or n.\n')

        if raw_data_question.lower() == 'n':
            break
        elif raw_data_question.lower() == 'y':
            if raw_count*5 + 5 <= df.shape[0]:
                print(df.iloc[raw_count*5 : raw_count*5 + 5])
                raw_count = raw_count + 1
            elif raw_count*5 < df.shape[0]:
                print(df.iloc[raw_count*5 : df.shape[0]])
                print("Done printing all data, breaking...")
                break
            else:
                print("Done printing all data, breaking...")
                break
        else:
            print("Invalid input, please try again.")

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    unique_months = df['month'].unique()
    if unique_months.shape[0] == 1:
        print("You have filtered data by month. So the most common month is %s" %(MONTH_LIST[unique_months[0] - 1].upper()))
    else:
        month_count_list = df['month'].value_counts()
        most_common_month = MONTH_LIST[month_count_list.keys().tolist()[0] - 1].upper()
        month_count = month_count_list.tolist()[0]
        print("%s is the best month for biking! %d rides were taken in %s." %(most_common_month, month_count, most_common_month))

    # display the most common day of week
    unique_days = df['day_of_week'].unique()
    if unique_days.shape[0] == 1:
        print("You have filtered data by day of the week. So the most common day of week is %s" %(DAY_LIST[unique_days[0] - 1].upper()))
    else:
        day_count_list = df['day_of_week'].value_counts()
        most_common_day = DAY_LIST[day_count_list.keys().tolist()[0] - 1].upper()
        day_count = day_count_list.tolist()[0]
        print("%s is the best day for biking! %d rides were taken on %s." %(most_common_day, day_count, most_common_day))

    # display the most common start hour
    start_hour_series = df['Start Time'].dt.hour
    start_hour_count_list = start_hour_series.value_counts()
    most_common_start_hour = start_hour_count_list.keys().tolist()[0]
    start_hour_count = start_hour_count_list.tolist()[0]
    print("%d is the most common hour to start biking! %d rides started at %d" %(most_common_start_hour, start_hour_count, most_common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station_value_counts = df['Start Station'].value_counts()
    most_common_start_station = start_station_value_counts.keys().tolist()[0]
    start_station_count = start_station_value_counts.tolist()[0]
    print("%s is the most common STARTING station for the bikers! %d rides started at this station." %(most_common_start_station, start_station_count))


    # display most commonly used end station
    end_station_value_counts = df['End Station'].value_counts()
    most_common_end_station = end_station_value_counts.keys().tolist()[0]
    end_station_count = end_station_value_counts.tolist()[0]
    # print(start_station_value_counts.head())
    print("%s is the most common ENDING station for the bikers! %d rides ended at this station." %(most_common_end_station, end_station_count))


    # display most frequent combination of start station and end station trip
    frequent_combo_df = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).reset_index(name='count')
    start_station = frequent_combo_df.iloc[0]["Start Station"]
    end_station = frequent_combo_df.iloc[0]["End Station"]
    frequency = frequent_combo_df.iloc[0]["count"]
    print("Trips from %s to %s occurred frequently. The count was %d." %(start_station, end_station, frequency))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    total_minutes = total_duration // 60
    total_hours = total_minutes // 60
    remainder_minutes = total_minutes % 60
    remainder_seconds = total_duration % 60

    print("Total duration is %d seconds, i.e." %(total_duration))
    print("Total duration is %d hours, %d minutes and %d seconds." %(total_hours, remainder_minutes, remainder_seconds))

    # display mean travel time
    mean_travel_time = round(total_duration / df.shape[0], 2)

    print("Average travel time is %f seconds." %(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = df['User Type'].value_counts()
    print("\nThe types of users that we have and their respective counts are:")
    print(user_type_counts)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("\nThe counts of users according to gender are:")
        print(gender_counts)
    else:
        print("\nYou have selected Washington city and counts of gender information is not available for Washington city")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        # Most common year of birth
        year_counts = df['Birth Year'].value_counts()
        most_common_birth_year = year_counts.keys().tolist()[0]
        birth_year_count = year_counts.tolist()[0]
        print("\n%d is the most common birth year for the bikers! No. of users are %d" %(most_common_birth_year, birth_year_count))

        # Earliest year of birth
        oldest = df['Birth Year'].min()
        print("The oldest people riding the bikes were born in %d" %(oldest))

        # Most recent
        youngest = df['Birth Year'].max()
        print("The youngest people riding the bikes were born in %d" %(youngest))
    else:
        print("\nYou have selected Washington city and year of birth information is not available for Washington city")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main() 