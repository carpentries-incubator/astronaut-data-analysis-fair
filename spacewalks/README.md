# Overview
Spacewalks is a python-based analysis tool for researchers to generate visualisations
and statistical summaries of NASA's extravehicular activity datasets.

## Features
Key features of Spacewalks:
- Generates a CSV table of summary statistics of extravehicular activity crew sizes
- Generates a line plot to show the cumulative duration of space walks over time

## Pre-requisites
Spacewalks was developed using Python version 3.12

To install and run Spacewalks you will to need have Python >=3.12 
installed. You will also need the following libraries (minimum versions in brackets)

- [NumPy](https://www.numpy.org/) >=2.0.0 - Spacewalk's test suite uses NumPy's statistical functions
- [Matplotlib](https://matplotlib.org/stable/index.html) >=3.0.0  - Spacewalks uses Matplotlib to make plots
- [pytest](https://docs.pytest.org/en/8.2.x/#) >=8.2.0  - Spacewalks uses pytest for testing
- [pandas](https://pandas.pydata.org/) >= 2.2.0 - Spacewalks uses pandas for data frame manipulation 

## Installation Instructions

Clone the Spacewalks repository to your local machine using Git.
If you don't have Git installed, you can download it from the official Git website.

```bash
git clone https://github.com/your-repository-url/spacewalks.git
cd spacewalks
```

Install the necessary dependencies:

```bash
python -m pip install pandas==2.2.2 matplotlib==3.8.4 numpy==2.0.0 pytest==7.4.2
```

To ensure everything is working correctly, run the tests using pytest.

```bash
python -m pytest
```


## Usage Example

To run an analysis using the eva_data_analysis.py script from the command line terminal,
launch the script using Python as follows:

```bash
python eva_data_analysis.py eva-data.json eva-data.csv
```

where: 
- the first argument is path to the Json data file.
- the second argument is the path the CSV output file.
