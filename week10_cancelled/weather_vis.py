import requests
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os

plt.rcParams.update({'font.size': 12})

# What we want to do:
# 1. Adapt functions from week 7 workshop to return Pandas dataframe
# 2. Simplify a little
# 3. Manipulate the resulting dataframe to make it work well with Seaborn
#    (convert to long format (melt), joining/merging dataframes)


def get_weather_data(city_name, frequency, variables):
    # Look for existing CSV (to avoid repeating API requests unnecessarily)
    filename = f'{city_name}_{frequency}'
    for v in variables:
        filename += f'_{v}'
    filename += '.csv'

    if not os.path.exists(filename):
        # Get city information
        params_dict = {'name': city_name, 'count': 1}
        city_info = requests.get('https://geocoding-api.open-meteo.com/v1/search', params=params_dict).json()

        # Extract the first result in the list
        city_info = city_info['results'][0]

        # Get latitude, longitude, and time zone
        latitude, longitude = city_info['latitude'], city_info['longitude']
        time_zone = city_info['timezone']

        # Create a dictionary for the parameters I need
        params_dict = {'timezone': time_zone,
                       'latitude': latitude,
                       'longitude': longitude,
                       frequency: variables}

        # Request data from the API
        r = requests.get('https://api.open-meteo.com/v1/forecast', params=params_dict)

        # Parse the JSON data to a pandas dataframe (much easier than dealing with dicts!)
        data = pd.DataFrame(r.json()['hourly'])
        data.to_csv(filename, index=False)
    else:
        data = pd.read_csv(filename)

    # Make sure the time column values are proper datetime objects
    data['time'] = pd.to_datetime(data['time'])

    return data


if __name__ == '__main__':
    city_name = 'Edinburgh'
    frequency = 'hourly'
    variables = ['temperature_2m', 'cloud_cover']
    edinburgh_data = get_weather_data(city_name, frequency, variables)
    # print(edinburgh_data.head(20))

    # # Plot just the temperature data over time
    # sns.relplot(data=edinburgh_data, x='time', y='temperature_2m', kind='line')
    # plt.show()

    sns.relplot(data=edinburgh_data, x='time', y='temperature_2m', hue='cloud_cover', size='cloud_cover')
    plt.show()

    # Plot temperature and cloud cover in 2 separate subplots

    # First: convert to long format
    print('Before converting to long format:\n', edinburgh_data)
    edinburgh_data_long = pd.melt(edinburgh_data, id_vars=['time'], value_vars=['temperature_2m', 'cloud_cover'])
    print('After converting to long format:\n', edinburgh_data_long)

    sns.relplot(data=edinburgh_data_long, x='time', y='value', col='variable')
    plt.show()

    # Try this: this now plots temperature and cloud cover in 1 figure,
    # with different colours for the 2 different variables in 'variable'.
    # Make sure you understand the difference with the first plot before
    # we used pd.melt()!
    # sns.relplot(data=edinburgh_data_long, x='time', y='value', hue='variable')

    # Exercises:
    # - Add more weather variables
    # - Incorporate the units in the labels/titles
    # - Get data for another city, merge it with first city, plot
    #     data for the 2 cities in the same figure


    ## Joining data for multiple cities

    # Get the same data for Glasgow
    city_name = 'Glasgow'
    glasgow_data = get_weather_data(city_name, frequency, variables)

    # Remove one data point each day, at a different time in Edinburgh and Glasgow,
    # just to demonstrate joining dataframes with different missing values
    edinburgh_data_gaps = edinburgh_data.loc[edinburgh_data['time'].dt.hour != 2]
    glasgow_data_gaps = glasgow_data.loc[glasgow_data['time'].dt.hour != 5]
    # print(edinburgh_data_gaps.head(10))
    # print(glasgow_data_gaps.head(10))

    # Join the two dataframes 
    edinburgh_data_gaps['city'] = 'Edinburgh'
    glasgow_data_gaps['city'] = 'Glasgow'
    edi_gla_data = pd.concat([edinburgh_data_gaps, glasgow_data_gaps])
    print(edi_gla_data.head())

    # Create 2 subplots, one for each city
    sns.relplot(data=edi_gla_data, x='time', y='temperature_2m', hue='cloud_cover', size='cloud_cover', col='city')
    plt.show()

    # We could also merge the 2 dataframes like this (try the different ways and spot which times are missing!)
    # How you choose to join dataframes depends on what you need to do with the data after.
    # edi_gla_data = edinburgh_data_gaps.merge(glasgow_data_gaps, on='time', suffixes=['_edi', '_gla'])
    # edi_gla_data = edinburgh_data_gaps.merge(glasgow_data_gaps, on='time', suffixes=['_edi', '_gla'], how='right')
    edi_gla_data = edinburgh_data_gaps.merge(glasgow_data_gaps, on=['time', 'city'], suffixes=['_edi', '_gla'], how='outer')
    print(edi_gla_data.head())
