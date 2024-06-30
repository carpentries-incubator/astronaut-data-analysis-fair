import pandas as pd
import matplotlib.pyplot as plt
import sys


def read_json_to_dataframe(input_file_):
    print(f'Reading JSON file {input_file_}')
    # Read the data from a JSON file into a Pandas dataframe
    eva_df = pd.read_json(input_file_, convert_dates=['date'])
    # Clean the data by removing any incomplete rows and sort by date
    eva_df['eva'] = eva_df['eva'].astype(float)
    eva_df.dropna(axis=0, inplace=True)
    eva_df.sort_values('date', inplace=True)
    return eva_df


def write_dataframe_to_csv(df_, output_file_):
    print(f'Saving to CSV file {output_file_}')
    # Save dataframe to CSV file for later analysis
    df_.to_csv(output_file_, index=False)

def text_to_duration(duration):
    # Convert a string duration to number of hours
    hours, minutes = duration.split(":")
    duration_hours = int(hours) + int(minutes)/60
    return duration_hours


def add_duration_hours_variable(df_):
    # Convert the duration column from strings to number of hours
    df_copy = df_.copy()
    df_copy["duration_hours"] = df_copy["duration"].apply(
        text_to_duration
    )
    return df_copy


def plot_cumulative_time_in_space(df_, graph_file_):
    print(f'Plotting cumulative spacewalk duration and saving to {graph_file_}')
    # Plot cumulative time spent in space over years
    df_ = add_duration_hours_variable(df_)
    df_['cumulative_time'] = df_['duration_hours'].cumsum()
    plt.plot(df_.date, df_.cumulative_time, 'ko-')
    plt.xlabel('Year')
    plt.ylabel('Total time spent in space to date (hours)')
    plt.tight_layout()
    plt.savefig(graph_file_)
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

    print("--END--")
