"""
Building an analytics page for HubOptimize
"""

####################################################################################
# IMPORTING LIBRARIES AND LOADING DATA
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Set page configurations for streamlit
st.set_page_config(
    page_title="Analytics",
    page_icon="📊",
    layout="wide",
)

# Loading data
datafile = 'hotel_booking.csv'

# Store/Cache data once
@st.cache_data
def get_data() -> pd.DataFrame:
    return pd.read_csv(datafile)

df = get_data()


####################################################################################
# PRE-PROCESSING AND DATA CLEANING
# Drop columns not required
df.drop(columns={'hotel', 'lead_time', 'adults', 'babies', 'children', 
                 'meal', 'distribution_channel', 'country', 'reserved_room_type', 
                 'agent', 'company', 'days_in_waiting_list', 'required_car_parking_spaces', 
                 'stays_in_weekend_nights', 'stays_in_week_nights', 'is_repeated_guest'}, 
                 inplace=True)

# Rename columns
renamed_columns = {
    'assigned_room_type': 'space_type',
    'customer_type': 'customer_booking_type',
    'adr' : 'average_daily_rate',
    'deposit_type' : 'payment_type',
    'arrival_date_year': 'year',
    'arrival_date_month': 'month',
    'arrival_date_week_number': 'week_number',
    'arrival_date_day_of_month': 'day_of_month'
}

df.rename(columns=renamed_columns, inplace=True)

# Modify Data
# 1. Data in space type
new_space_type = {
    'A': 'Open Workspace, Flexible Hours',
    'B': 'Private Workspace, Medium',
    'C': 'Open Workspace, Collaborative Environment',
    'D': 'Meeting Room, Coffee/Tea',
    'E': 'Open Workspace, Regular Hours',
    'F': 'Private Workspace, Small',
    'G': 'Meeting Room',
    'H': 'Private Office, Phone Booth',
    'I': 'Virtual Office',
    'K': 'Conference Room, Coffee/Tea',
    'L': 'Private Workspace, Large',
    'P': 'Conference Room'
}
df.space_type = df['space_type'].replace(new_space_type)

# 2. Dropping rows that have market_segment as 'Aviation'
df.drop(df[df.market_segment == 'Aviation'].index, axis=0, inplace=True)

# 3. Substitute data in 'customer_booking_type' to specify 
# whether users are booking daily, monthly, or yearly.
new_booking_type = {
    'Transient': 'Monthly',
    'Transient-Party': 'Daily per hour',
    'Contract': 'Weekly',
    'Group': 'Yearly'
}
df.customer_booking_type = df['customer_booking_type'].replace(new_booking_type)

# 4. Substitute data in 'payment_type' to specify what mediums 
# co-working space users use to pay.
new_payment_type = {
    'No Deposit': 'Online',
    'Non Refund': 'In Person Card',
    'Refundable': 'In Person Cash'
}
df.payment_type = df['payment_type'].replace(new_payment_type)

# Creating and populating dataframe with new data
# Setting a seed to ensure reproduceability whenever code is run
np.random.seed(123)

# Define the length of the DataFrame
df_length = len(df)

# 1. Create new column 'age' and populate with random 
# ages between 18 and 60
# Generate random values for the age column
random_values = np.random.randint(18, 60, df_length)

# Create new column and populate with the random values
df['age'] = random_values

# 2. Create new column 'gender' and populate with 
# male and female genders.
# Define the list of values 'gender' column
values_list = ['Male', 'Female']

random_values = np.random.choice(values_list, df_length)
df['gender'] = random_values

# 3. Create new column 'user_work_preferences' and 
# populate with random selections from list.
values_list = ['Quiet environment', 'Flexible Hours', 'Collaborative Environment', 
               'Regular Hours', 'Private Workspace', 'Open Workspace']
random_values = np.random.choice(values_list, df_length)
df['user_work_preferences'] = random_values

# 4. Create new column 'user_top_amenity' and populate 
# with random selections from list.
values_list = ['High-speed Internet', 'Coffee/Tea', 'Meeting Rooms', 
               'Printing/Scanning', 'Lounge Areas', 'Outdoor Space']
random_values = np.random.choice(values_list, df_length)
df['user_top_amenity'] = random_values

# 5. Create new column 'membership_status' and populate 
# with random selections from list.
values_list = ['Member', 'Non Member']
random_values = np.random.choice(values_list, df_length)
df['membership_status'] = random_values

# 6. Create new column 'booking_duration_hours' and 
# populate with random hours.
random_values = np.random.randint(1, 15, df_length)
df['booking_duration_hours'] = random_values

# 7. Create new column 'booking_price' and populate with 
# prices for each booking type.
# Define a dictionary mapping booking types to their prices
booking_prices = {
    'Daily per hour': 2000,
    'Weekly': 15000,
    'Monthly': 25000,
    'Yearly': 70000
}

# Create a new column in the DataFrame by mapping the membership plans to their prices
df['space_booking_price'] = df['customer_booking_type'].map(booking_prices)

# 8. Create new column 'user_rating' and populate with 
# ratings for spaces.
random_rating = np.round(np.random.uniform(1, 5, df_length), 1)
df['user_rating'] = random_rating

# 9. Create new column 'weekday_booking' and populate with 
# boolean values showing if the booking was for a weekday or a weekend.
values_list = [0, 1]
random_values = np.random.choice(values_list, df_length)
df['weekday_booking'] = random_values

# 10. Create new column 'occupation' and populate with 
# randomly assigned occupations.
values_list = ['Freelancer', 'Software Developer', 'Graphic Designer', 
               'Marketing Professional', 'Entrepreneur', 'Writer', 
               'Researcher', 'Remote Worker', 'Data Scientist', 
               'Financial Analyst', 'Digital Nomad']
random_values = np.random.choice(values_list, df_length)
df['occupation'] = random_values

####################################################################################
# EXPLORATORY DATA ANALYSIS
# Dashboard title
st.title("Insights")

# Filters
# Year filter
year_filter = st.selectbox("Select the Year", pd.unique(df["year"]))

# Month Filter
month_filter = st.selectbox("Select the Month", pd.unique(df["month"]))

# Filter dataframe according to filters
df = df[df["year"] == year_filter]
df = df[df["month"] == month_filter]

st.markdown("<hr/>",unsafe_allow_html=True)

# Count things for summary cards
no_members = len(df)
weekday_bookings = len(df[df['weekday_booking'] == 1])
weekend_bookings = len(df[df['weekday_booking'] == 0])

# Create summary cards
# create four columns
sc_1, sc_2, sc_3 = st.columns(3)

with sc_1:
    st.markdown("**Total Members**")
    number1 = no_members 
    st.markdown(f"<h1 style='color: #017A40;'>{number1}</h1>", unsafe_allow_html=True)

with sc_2:
    st.markdown("**Weekday Bookings**")
    number2 = weekday_bookings 
    st.markdown(f"<h1 style='color: #017A40;'>{number2}</h1>", unsafe_allow_html=True)

with sc_3:
    st.markdown("**Weekend Bookings**")
    number3 = weekend_bookings
    st.markdown(f"<h1 style='color: #017A40;'>{number3}</h1>", unsafe_allow_html=True)

st.markdown("<hr/>",unsafe_allow_html=True)


# Charts
# Most popular space types
if len(df) != 0:
    st.markdown(f"<h3 style='text-align: center; color: #003873;'>Most Popular \
Space Types</h3>", unsafe_allow_html=True)
    fig1, ax1 = plt.subplots(figsize=(14,8))
    ax1 = sns.countplot(y='space_type', data=df, palette='Blues_d', hue= 'space_type', legend=False)
    plt.ylabel('Coworking Space Type')
    plt.xlabel('Count')
    sns.despine(bottom = True, left = True)
    st.pyplot(fig1)
    
    st.markdown("<hr/>",unsafe_allow_html=True)

# Heatmap showing Average daily rate per month for each space
if len(df) != 0:
    st.markdown(f"<h3 style='text-align: center; color: #003873;'>Average Daily Rate \
of Space Types Per Month</h3>", unsafe_allow_html=True)
    # create pivot table, months will be columns, 
    # space_type will be rows, average_daily_rate 
    # will be the values
    fig2, ax2 = plt.subplots(figsize=(14,8))
    piv = pd.pivot_table(df, values="average_daily_rate",
                            index=["space_type"], columns=["month"], fill_value=0)
    ax1 = sns.heatmap(piv, annot=True, fmt='.2f', cmap='YlGnBu', linewidths=.5)
    plt.xlabel('Month')
    plt.ylabel('Coworking Space Type')
    plt.tight_layout()
    st.pyplot(fig2)

    st.markdown("<hr/>",unsafe_allow_html=True)

# Distribution of canceled space types
if len(df) != 0:
    fig_col1, fig_col2 = st.columns(2)
    # Bar Chart of Highest canceled space types
    with fig_col1:
        st.markdown(f"<h4 style='text-align: center; color: #003873;'>Space Types With \
the Highest Cancelations</h4>", unsafe_allow_html=True)
        fig3, ax3 = plt.subplots(figsize=(16,15))
        ax3 = sns.countplot(data=df, y='space_type', hue='is_canceled', palette='Blues_d')
        plt.ylabel('Coworking Space Type')
        plt.xlabel('Count')
        sns.despine(bottom = True, left = True)
        plt.legend(loc='lower right', labels=['Not Canceled', 'Canceled'])
        st.pyplot(fig3)

    # Pie chart of canceled space types
    with fig_col2:
        st.markdown(f"<h4 style='text-align: center; color: #003873;'>Distribution of Canceled \
    Bookings by Space Type</h4>", unsafe_allow_html=True)
        def calculate_distribution(df):
            canceled_counts = df[df['is_canceled'] == 1]['space_type'].value_counts()
            # Set a threshold for percentages
            threshold = 1.5

            # Calculate the total count of canceled bookings
            total_canceled_count = canceled_counts.sum()

            # Filter out counts below the threshold
            canceled_counts_above_threshold = canceled_counts[canceled_counts / total_canceled_count * 100 >= threshold]

            # Calculate the percentage of canceled bookings for each room type
            percentages = canceled_counts_above_threshold / total_canceled_count * 100

            # Combine counts below the threshold and label as 'Other'
            other_count = canceled_counts[canceled_counts / total_canceled_count * 100 < threshold].sum()
            percentages['Others'] = other_count / total_canceled_count * 100

            return percentages

        pie_chart_percentages = calculate_distribution(df)

        fig5, ax5 = plt.subplots(figsize=(8,8))
        plt.pie(pie_chart_percentages, labels=pie_chart_percentages.index, autopct='%1.1f%%', startangle=140)
        st.pyplot(fig5)

    st.markdown("<hr/>",unsafe_allow_html=True)

# Distribution of Customer Booking Type Among The Top 5 Most Popular Spaces
if len(df) != 0:
    st.markdown(f"<h3 style='text-align: center; color: #003873;'>Distribution of Customer \
Booking Type Among The Top 5 Most Popular Spaces</h3>", unsafe_allow_html=True)
    top_spaces = df['space_type'].value_counts().index[:4]

    # filter dataframe
    df_top_spaces = df[df['space_type'].isin(top_spaces)]

    fig6, ax6 = plt.subplots(figsize=(14,8))
    ax6 = sns.countplot(x='space_type', data=df_top_spaces, 
                        palette='Blues_d', hue= 'customer_booking_type')
    plt.xlabel('Coworking Space Type')
    plt.xticks(fontsize=9)
    plt.ylabel('Count')
    plt.legend(title='Customer Booking Type')
    sns.despine(bottom = True, left = True)
    st.pyplot(fig6)

    st.markdown("<hr/>",unsafe_allow_html=True)

# Space types aligned with user preferences
if len(df) != 0:
    st.markdown(f"<h3 style='text-align: center; color: #003873;'>Space Types \
Aligned with User Preferences</h3>", unsafe_allow_html=True)
    
    room_preferences_counts = df.groupby(['space_type', 'user_work_preferences'])\
        .size().unstack(fill_value=0)
    fig7, ax7 = plt.subplots(figsize=(14,8))
    ax7 = sns.heatmap(room_preferences_counts, annot=True, fmt="d", cmap='YlGnBu', linewidths=.5)
    plt.xlabel('User Preferences')
    plt.ylabel('Room')
    sns.despine(bottom = True, left = True)
    plt.xticks(fontsize=9.5)
    st.pyplot(fig7)
    
    st.markdown("<hr/>",unsafe_allow_html=True)

# Occupations of Frequent Users
if len(df) != 0:
    st.markdown(f"<h3 style='text-align: center; color: #003873;'>Occupations \
of Frequent Users</h3>", unsafe_allow_html=True)
    
    fig8, ax8 = plt.subplots(figsize=(14,8))
    ax8 = sns.countplot(y='occupation', data=df, palette='Blues_d', hue= 'occupation', legend=False)
    plt.ylabel('Occupation')
    plt.xlabel('Count')
    sns.despine(bottom = True, left = True)
    st.pyplot(fig8)

    st.markdown("<hr/>",unsafe_allow_html=True)

# Which occupations frequently use the rooms that have the highest daily rate?
if len(df) != 0:
    st.markdown(f"<h3 style='text-align: center; color: #003873;'>Occupations \
Frequently Using Spaces With Highest Daily Rates</h3>", unsafe_allow_html=True)
    
    highest_daily_rate = df['average_daily_rate'].max()
    rooms_with_highest_rate = df[df['average_daily_rate']\
                                == highest_daily_rate]['space_type'].unique()
    high_rate_data = df[df['space_type'].isin(rooms_with_highest_rate)]
    occupation_counts = high_rate_data['occupation'].value_counts().reset_index()
    occupation_counts.columns = ['Occupation', 'Count']

    fig9, ax9 = plt.subplots(figsize=(14,8))
    ax9 = sns.barplot(x='Occupation', y='Count', data=occupation_counts, palette='Blues_d')
    plt.xlabel('Occupation')
    plt.ylabel('Frequency of Room Use')
    plt.xticks(fontsize=7)
    sns.despine(bottom = True, left = True)
    st.pyplot(fig9)

    st.markdown("<hr/>",unsafe_allow_html=True)

# Which gender uses the most popular rooms the most?
if len(df) != 0:
    st.markdown(f"<h3 style='text-align: center; color: #003873;'>Space \
Use by Gender</h3>", unsafe_allow_html=True)
    
    fig10, ax10 = plt.subplots(figsize=(14,8))
    ax10 = sns.countplot(data=df, y='space_type', hue='gender', palette='Blues_d')
    plt.ylabel('Coworking Space Type')
    plt.xlabel('Count')
    plt.legend(labels=['Male', 'Female'], loc='lower right')
    sns.despine(bottom = True, left = True)
    st.pyplot(fig10)

    st.markdown("<hr/>",unsafe_allow_html=True)

# Rooms with Highest Booking Duration Counts
if len(df) != 0:
    st.markdown(f"<h3 style='text-align: center; color: #003873;'>Space \
Types with Highest Booking Duration Counts</h3>", unsafe_allow_html=True)
    
    # Group data by room and booking hours, then count occurrences
    room_hour_counts = df.groupby(['space_type', 'booking_duration_hours']).size().reset_index(name='count')

    # Find the booking duration hour with the highest count for each room
    idx = room_hour_counts.groupby(['space_type'])['count'].transform(max) == room_hour_counts['count']
    room_highest_counts = room_hour_counts[idx]

    # If multiple hours have the same highest count for a room, this could show multiple rows per room.
    # To simplify, we can take the first occurrence (or handle duplicates as needed)
    room_highest_counts = room_highest_counts.drop_duplicates(subset=['space_type'])
    
    fig11, ax11 = plt.subplots(figsize=(14,8))
    ax11 = sns.barplot(data=room_highest_counts, y='space_type', x='count', \
                       hue='booking_duration_hours', palette='Blues_d')
    plt.ylabel('Co-Working Space Type')
    plt.xlabel('Count')
    plt.legend(title='Booking Duration (Hours)')
    sns.despine(bottom = True, left = True)
    st.pyplot(fig11)

    st.markdown("<hr/>",unsafe_allow_html=True)