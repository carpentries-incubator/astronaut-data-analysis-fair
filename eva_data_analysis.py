"""
Analyse the time spent in spacewalks (EVAs) by US and Russian astronauts
from 1965 to 2013.

Data source*: https://data.nasa.gov/Raw-Data/Extra-vehicular-Activity-EVA-US-and-Russia/9kcy-zwvn/about_data
Download in JSON format with:
    `curl https://data.nasa.gov/resource/eva.json --output eva-data.json`
* With post-download modifications (see README for further details)

Authors:
    Sarah Jaffa
"""

import pandas as pd
import matplotlib.pyplot as plt
import sys


def read_json_to_dataframe(input_file_):
    """
    Read the data from a JSON file into a Pandas dataframe
    Clean the data by removing any incomplete rows and sort by date
    """
    print(f'Reading JSON file {input_file_}')
    # Complains here
    eva_df = pd.read_json(input_file_,
                          convert_dates=['date'])
    eva_df.dropna(axis=0, inplace=True)
    eva_df.sort_values('date', inplace=True)
    return eva_df


def write_dataframe_to_csv(df_, output_file_):
    """
    Save dataframe to CSV file for later analysis
    """
    print(f'Saving to CSV file {output_file_}')
    df_.to_csv(output_file_)


def plot_cumulative_time_in_space(df_, graph_file_):
    """
    Convert the duration column from strings to number of hours
    Calculate cumulative sum of durations
    Plot cumulative time spent in space over years
    """
    print(f'Plotting cumulative spacewalk duration and saving to {graph_file_}')
    df_['duration_hours'] = df_['duration'].str.split(":").apply(lambda x: int(x[0]) + int(x[1])/60)
    df_['cumulative_time'] = df_['duration_hours'].cumsum()
    plt.plot(df_.date, df_.cumulative_time, 'ko-')
    plt.xlabel('Year')
    plt.ylabel('Total time spent in space to date (hours)')
    plt.tight_layout()
    plt.savefig(graph_file)
    plt.show()


if __name__ == '__main__':

    if len(sys.argv) < 3:
        input_file = './eva-data.json'
        output_file = './eva-data.csv'
        print(f'Using default input and output filenames')
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        print('Using custom input and output filenames')

    graph_file = './cumulative_eva_graph.png'

    eva_data = read_json_to_dataframe(input_file)

    write_dataframe_to_csv(eva_data, output_file)

    plot_cumulative_time_in_space(eva_data, graph_file)
