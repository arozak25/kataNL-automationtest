# Kata NL Automation Test

This program is made for automate Kata NL Testing. You can test the NL by preparing a .txt file format that includes sentences and the label that the NL should recognize. The output of the test will be an excel file with an important information about the result.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

Things you need to install:
* [Pyhton version 3.6 or above](https://www.python.org/downloads/)

### Installing

A step by step series of examples that tell you how to get the program running

1. Clone this project (You know how to clone right?)

2. Once you already installed python, run: `pip install -r requirements.txt`

3. After all the packages required in the `requirements.txt` already installed. Open `predict.py`

## Running the tests

In `predict.py` , you'll find the following variables:
```# Input the parameter
TXT_INPUT_FILENAME = "datatraining"
EXCEL_OUTPUT_FILENAME = "Test Result After Training"
EXCEL_WORKSHEET_NAME = "Test Result"
BASE_DIR = 'F:\\Some\\Path'
NL_ID = "YOUR-NL-ID"
NL_TOKEN = "YOUR-NL-TOKEN"
THRESHOLD = 0.5
API_ENDPOINT = "https://geist.kata.ai/nlus/" + NL_ID + "/predict"
```
### Usage

You can utilize those variable based on their function:

`TXT_INPUT_FILENAME` : file name with .txt extension for input

`EXCEL_OUTPUT_FILENAME` : file name for the excel output

`EXCEL_WORKSHEET_NAME` : worksheet name for the excel output

`BASE_DIR` : the base directory for `TXT_INPUT_FILENAME`

`NL_ID` : kata NL ID

`NL_TOKEN` : kata NL Token

`THRESHOLD` : minimum threshold for a sentence to passed the test

`API_ENDPOINT` : kata prediction API Endpoint

If all looks good, you can run `predict.py` and wait for the test result.

## Contributing

Is something missing/incorrect? Please let me know by contacting arozak25@gmail.com. If you know how to fix it straight away, don’t hesitate to create a pull request on this GitHub repository.
