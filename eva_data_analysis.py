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
import re


def read_json_to_dataframe(input_file_):
    """
    Read the data from a JSON file into a Pandas dataframe.
    Clean the data by removing any incomplete rows and sort by date

    Args:
        input_file_ (str): The path to the JSON file.

    Returns:
        pd.DataFrame: The loaded dataframe.
    """
    print(f'Reading JSON file {input_file_}')
    eva_df = pd.read_json(input_file_, convert_dates=['date'])
    eva_df['eva'] = eva_df['eva'].astype(float)
    eva_df.dropna(axis=0, inplace=True)
    eva_df.sort_values('date', inplace=True)
    return eva_df


def write_dataframe_to_csv(df_, output_file_):
    """
    Write the dataframe to a CSV file.

    Args:
        df_ (pd.DataFrame): The input dataframe.
        output_file_ (str): The path to the output CSV file.

    Returns:
        None
    """
    print(f'Saving to CSV file {output_file_}')
    df_.to_csv(output_file_, index=False)

def text_to_duration(duration):
    """
    Convert a text format duration "HH:MM" to duration in hours

    Args:
        duration (str): The text format duration

    Returns:
        float: The duration in hours
    """
    hours, minutes = duration.split(":")
    duration_hours = int(hours) + int(minutes)/60
    return duration_hours


def add_duration_hours_variable(df_):
    """
    Add duration in hours (duration_hours) variable to the dataset

    Args:
        df_ (pd.DataFrame): The input dataframe.

    Returns:
        pd.DataFrame: A copy of df_ with the new duration_hours variable added
    """
    df_copy = df_.copy()
    df_copy["duration_hours"] = df_copy["duration"].apply(
        text_to_duration
    )
    return df_copy


def plot_cumulative_time_in_space(df_, graph_file_):
    """
    Plot the cumulative time spent in space over years

    Convert the duration column from strings to number of hours
    Calculate cumulative sum of durations
    Generate a plot of cumulative time spent in space over years and
    save it to the specified location

    Args:
        df_ (pd.DataFrame): The input dataframe.
        graph_file_ (str): The path to the output graph file.

    Returns:
        None
    """
    print(f'Plotting cumulative spacewalk duration and saving to {graph_file_}')
    df_ = add_duration_hours_variable(df_)
    df_['cumulative_time'] = df_['duration_hours'].cumsum()
    plt.plot(df_.date, df_.cumulative_time, 'ko-')
    plt.xlabel('Year')
    plt.ylabel('Total time spent in space to date (hours)')
    plt.tight_layout()
    plt.savefig(graph_file_)
    plt.show()


def calculate_crew_size(crew):
    """
    Calculate crew_size for a single crew entry

    Args:
        crew (str): The text entry in the crew column

    Returns:
        int: The crew size
    """
    if crew.split() == []:
        return None
    else:
        return len(re.split(r';', crew))-1


def add_crew_size_variable(df_):
    """
    Add crew size (crew_size) variable to the dataset

    Args:
        df_ (pd.DataFrame): The input dataframe.

    Returns:
        pd.DataFrame: A copy of df_ with the new crew_size variable added
    """
    print('Adding crew size variable (crew_size) to dataset')
    df_copy = df_.copy()
    df_copy["crew_size"] = df_copy["crew"].apply(
        calculate_crew_size
    )
    return df_copy



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

    eva_data_prepared = add_crew_size_variable(eva_data)

    write_dataframe_to_csv(eva_data_prepared, output_file)

    plot_cumulative_time_in_space(eva_data_prepared, graph_file)

    print("--END--")
