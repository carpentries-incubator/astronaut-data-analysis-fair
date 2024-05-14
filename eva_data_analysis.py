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
import pandera as pa
import matplotlib.pyplot as plt
import sys
import re
import json

def read_json_to_dataframe(input_file_):
    """
    Read the data from a JSON file into a Pandas dataframe.

    Args:
        input_file_ (str): The path to the JSON file.

    Returns:
        pd.DataFrame: The loaded dataframe.
    """
    print(f'Reading JSON file {input_file_}')
    with open(input_file_, 'r') as f:
        json_data = json.load(f)

    eva_df = pd.json_normalize(json_data)

    return eva_df


def clean_data(df_):
    """
    Clean the input data

    Removing any incomplete rows;
    Set data types
    Sort by date (asc.)

    Args:
        df_ (pd.DataFrame): The input dataframe.

    Returns:
        pd.DataFrame: The cleaned dataframe.
    """
    print('Cleaning input data')
    df_['eva'] = df_['eva'].astype(float)
    df_['date'] = pd.to_datetime(df_['date'])
    df_.dropna(axis=0, inplace=True)
    df_.sort_values('date', inplace=True)
    return df_


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


def summarise_categorical(df_, varname_):
    """
    Tabulate the distribution of a categorical variable

    Args:
        df_ (pd.DataFrame): The input dataframe.
        varname_ (str): The name of the variable

    Returns:
        pd.DataFrame: dataframe containing the count and percentage of
        each unique value of varname_
    """
    print(f'Tabulating distribution of categorical variable {varname_}')

    # Prepare statistical summary
    count_variable = df_[[varname_]].copy()
    count_summary = count_variable.value_counts()
    percentage_summary = round(count_summary / count_variable.size, 2) * 100

    # Combine results into a summary data frame
    df_summary = pd.concat([count_summary, percentage_summary], axis=1)
    df_summary.columns = ['count', 'percentage']
    df_summary.sort_index(inplace=True)


    df_summary = df_summary.reset_index()
    return df_summary


def validate_input_data(df_):
    """
    Validate the input data against a schema.

    Args:
        df_ (pd.DataFrame): The input dataframe.

    Returns:
        bool: Whether the validation was successful.
    """
    print('Validating input data against schema')
    schema = pa.DataFrameSchema({
        'eva': pa.Column(str, nullable=True),
        'country': pa.Column(str, nullable=True),
        'crew': pa.Column(str, nullable=True, checks=pa.Check(
            lambda s: s.apply(lambda x: x == "" or ";" in x),
            error='Must be text using semicolon (;) as a separator')
        ),
        'vehicle': pa.Column(str, nullable=True),
        'date': pa.Column(str, nullable=True),
        'duration': pa.Column(str, nullable=True, checks=pa.Check(
            lambda x: (x == "") | x.str.match(r'^\d{1,2}:\d{2}$'),
            error='Must be in (H)H:MM format (without seconds)')
        ),
        'purpose': pa.Column(str, nullable=True)
    })

    try:
        schema.validate(df_, lazy=True)
        print('Data validation successful!')
        return True
    except pa.errors.SchemaError as e:
        print("Data validation failed!:", e)
        print("Skipping further analysis...")
        return False


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

    data_is_valid = validate_input_data(eva_data)

    if data_is_valid:

        eva_data_cleaned = clean_data(eva_data)

        eva_data_prepared = add_crew_size_variable(eva_data_cleaned)

        write_dataframe_to_csv(eva_data_prepared, output_file)

        table_crew_size = summarise_categorical(eva_data_prepared, "crew_size")

        write_dataframe_to_csv(table_crew_size, "./table_crew_size.csv")

        plot_cumulative_time_in_space(eva_data_prepared, graph_file)

    print("--END--")
