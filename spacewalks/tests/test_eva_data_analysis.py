import os
import pandas as pd
import numpy as np
import pandas.testing as pdt
import pytest
from eva_data_analysis import (
    write_dataframe_to_csv,
    read_json_to_dataframe,
    text_to_duration,
    add_duration_hours_variable,
    calculate_crew_size,
    add_crew_size_variable,
    summarise_categorical
)


def test_read_json_to_dataframe():
    """
    Test that read_json_to_dataframe loads json to dataframe and
    implements the following data cleaning steps
    drop_na, set types, convert string date (date) to date_time, sort by date
    """
    input_file = "tests/data/test_data.json"

    df_actual = read_json_to_dataframe(input_file)

    df_expected = pd.DataFrame({
        'eva': ['1', '3'],
        'country': ['USA', 'USA'],
        'crew': ['Ed White;', 'Eugene Cernan;'],
        'vehicle': ['Gemini IV', 'Gemini IX-A'],
        'date': ['1965-06-03T00:00:00.000', '1966-06-05T00:00:00.000'],
        'duration': ['0:36', '2:07'],
        'purpose': ['First U.S. EVA. ...', 'Inadequate restraints ...']
    }, index=[2, 0])
    
    df_expected['eva'] = df_expected['eva'].astype(float)
    df_expected['date'] = pd.to_datetime(df_expected['date'])

    # Open the file and verify its contents
    pdt.assert_frame_equal(df_actual, df_expected)


def test_write_data_to_file(tmp_path):
    """
    Test that write_data_to_file creates a CSV file with expected content
    at target location
    """
    data = pd.DataFrame({
        'eva': ['3', '2', '1'],
        'country': ['USA', 'USA', 'USA'],
        'crew': ['Eugene Cernan;', 'David Scott;', 'Ed White;'],
        'vehicle': ['Gemini IX-A', 'Gemini VIII', 'Gemini IV'],
        'date': ['1966-06-05T00:00:00.000', np.nan, '1965-06-03T00:00:00.000'],
        'duration': ['2:07', '0:00', '0:36'],
        'purpose': ['Inadequate restraints ...', 'HHMU EVA cancelled ...', 'First U.S. EVA. ...']
    })

    file_path = tmp_path / "test-eva-data.csv"

    write_dataframe_to_csv(data, file_path)

    # Assert that the file was created
    assert os.path.exists(file_path)

    # Open the file and verify its contents
    contents = pd.read_csv(file_path, dtype=str)
    pdt.assert_frame_equal(contents, data)

def test_text_to_duration_integer():
    """
    Test that text_to_duration returns expected ground truth values
    for typical whole hour durations
    """
    actual_result =  text_to_duration("10:00")
    expected_result = 10
    assert actual_result == expected_result

def test_text_to_duration_float():
    """
    Test that text_to_duration returns expected ground truth values
    for typical durations with a non-zero minute component
    """
    actual_result = text_to_duration("10:20")
    expected_result = 10.33333333
    assert actual_result == pytest.approx(expected_result)

def test_text_to_duration_edge():
    """
    Test that text_to_duration returns expected values
    for a set of edge-case examples
    """
    test_input = "0:00"
    expected_result = 0
    actual_result = text_to_duration(test_input)
    assert actual_result == pytest.approx(expected_result)

def test_add_duration_hours_variable():
    """
    Test that add_duration_hours_variable adds expected duration_hours
    column for simple ground truth example
    """

    test_input = pd.DataFrame({
        'duration': ['2:07', '0:00', '0:36'],
    }, index=[0, 1, 2])

    expected_result = pd.DataFrame({
        'duration': ['2:07', '0:00', '0:36'],
        'duration_hours': [2.116667, 0, 0.60],
    }, index=[0, 1, 2])

    actual_result = add_duration_hours_variable(test_input)

    pdt.assert_frame_equal(actual_result, expected_result)

def test_calculate_crew_size():
    """
    Test that calculate_crew_size returns expected ground truth values
    for typical crew values
    """
    actual_result = calculate_crew_size("Valentina Tereshkova;")
    expected_result = 1
    assert actual_result == expected_result

    actual_result = calculate_crew_size("Judith Resnik; Sally Ride;")
    expected_result = 2
    assert actual_result == expected_result

    test_input = "Richard Gordon;Buzz Aldrin;John Glenn;"
    expected_result = 3
    actual_result = calculate_crew_size(test_input)
    assert actual_result == expected_result

def test_calculate_crew_size_edge_cases():
    """
    Test that calculate_crew_size returns expected ground truth values
    for edge case where crew is an empty string
    """
    actual_result = calculate_crew_size("")
    assert actual_result is None


def test_add_crew_size_variable():
    """
    Test that add_crew_size_variable adds expected crew_count
    column for simple ground truth example
    """

    test_input = pd.DataFrame({
        'crew': [
            "",
            "Richard Gordon;",
            "Richard Gordon;Buzz Aldrin;",
            "Richard Gordon;Buzz Aldrin;John Glenn;"
        ]
    }, index=[0, 1, 2, 3])

    expected_result = pd.DataFrame({
        'crew': [
            "",
            "Richard Gordon;",
            "Richard Gordon;Buzz Aldrin;",
            "Richard Gordon;Buzz Aldrin;John Glenn;"
        ],
        'crew_size': [None, 1, 2, 3]
    }, index=[0, 1, 2, 3])

    actual_result = add_crew_size_variable(test_input)

    pdt.assert_frame_equal(actual_result, expected_result)


def test_summarise_categorical():
    """
    Test that summarise_categorical correctly tabulates
    distribution of values (counts, percentages) for a simple ground truth
    example
    """
    test_input = pd.DataFrame({
        'country': ['USA', 'USA', 'USA', "Russia", "Russia"],
    }, index=[0, 1, 2, 3, 4])

    expected_result = pd.DataFrame({
        'country': ["Russia", "USA"],
        'count': [2, 3],
        'percentage': [40.0, 60.0],
    }, index=[0, 1])

    actual_result = summarise_categorical(test_input, "country")

    pdt.assert_frame_equal(actual_result, expected_result)


def test_summarise_categorical_missvals():
    """
    Test that summarise_categorical correctly tabulates
    distribution of values (counts, percentages) for a ground truth
    example (edge case where column contains missing values)
    """
    test_input = pd.DataFrame({
        'country': ['USA', 'USA', 'USA', "Russia", pd.NA],
    }, index=[0, 1, 2, 3, 4])

    expected_result = pd.DataFrame({
        'country': ["Russia", "USA", np.nan],
        'count': [1, 3, 1],
        'percentage': [20.0, 60.0, 20.0],
    }, index=[0, 1, 2])
    actual_result = summarise_categorical(test_input, "country")

    pdt.assert_frame_equal(actual_result, expected_result)
    


def test_summarise_categorical_invalid():
    """
    Test that summarise_categorical raises an
    error when a non-existent column is input
    """
    test_input = pd.DataFrame({
        'country': ['USA', 'USA', 'USA', "Russia", "Russia"],
    }, index=[0, 1, 2, 3, 4])

    with pytest.raises(KeyError):
        summarise_categorical(test_input, "country-2")