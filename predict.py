import os
import requests
import xlsxwriter
import re

# Input the parameter
TXT_INPUT_FILENAME = "datatraining"
EXCEL_OUTPUT_FILENAME = "Test Result After Training"
EXCEL_WORKSHEET_NAME = "Test Result"
BASE_DIR = 'F:\\Nawatech\\Bodyshop\\test data'
NL_ID = "tbs-chatbot:NL-Yara-Main"
NL_TOKEN = "665e8d07-edc2-4633-af9b-fec1792dc5b8"
THRESHOLD = 0.5
API_ENDPOINT = "https://geist.kata.ai/nlus/" + NL_ID + "/predict"

filepath = os.path.join(BASE_DIR, TXT_INPUT_FILENAME + ".txt")
f = open(filepath, "r")

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook(EXCEL_OUTPUT_FILENAME + '.xlsx')
worksheet = workbook.add_worksheet(EXCEL_WORKSHEET_NAME)

bold = workbook.add_format({'bold': 1, 'border': 1})
below_threshold = workbook.add_format({'bg_color': '#e17055', 'border': 1})
no_dict_key = workbook.add_format({'bg_color': '#fdcb6e', 'border': 1})
wrong_intent = workbook.add_format({'bg_color': '#d63031', 'border': 1})
undetected_intent = workbook.add_format({'bg_color': '#9B59B6', 'border': 1})
border = workbook.add_format({'border': 1})

# Write some data headers.
worksheet.write('A1', 'Input', bold)
worksheet.write('B1', 'Type', bold)
worksheet.write('C1', 'Confidence', bold)
worksheet.write('D1', 'Value', bold)
worksheet.write('E1', 'Resolved Key', bold)
worksheet.write('F1', 'Notes', bold)

row = 2
for x in f:
    # data to be sent to api
    y = re.sub(r'#(\w+)', '', x)
    r = re.search(r"#(\w+)", x)
    expected_label = ""
    if r is not None:
        test = r.group().replace("#", "")
        expected_label = str(test)
    body = {'text': y}
    headers = {'Authorization': 'Bearer ' + NL_TOKEN}
    # sending post request and saving response as response object
    r = requests.post(url=API_ENDPOINT, data=body, headers=headers)

    for entities in r.json()["result"]:
        if len(r.json()["result"][entities]) != 0:
            entities_type = r.json()["result"][entities][0]["type"]
            score = r.json()["result"][entities][0]["score"]
            value = r.json()["result"][entities][0]["value"]
            if entities_type == "trait":
                if expected_label != value:
                    worksheet.write('A' + str(row), x, wrong_intent)
                    worksheet.write('B' + str(row), entities_type, wrong_intent)
                    worksheet.write('C' + str(row), score, wrong_intent)
                    worksheet.write('D' + str(row), value, wrong_intent)
                    worksheet.write('E' + str(row), "-", wrong_intent)
                    worksheet.write('F' + str(row), "This input isn't detected as " + str(expected_label), wrong_intent)
                    row += 1
                elif score < THRESHOLD and expected_label == value:
                    worksheet.write('A' + str(row), x, below_threshold)
                    worksheet.write('B' + str(row), entities_type, below_threshold)
                    worksheet.write('C' + str(row), score, below_threshold)
                    worksheet.write('D' + str(row), value, below_threshold)
                    worksheet.write('E' + str(row), "-", below_threshold)
                    worksheet.write('F' + str(row), "This input is below the expected threshold", below_threshold)
                    row += 1
                elif score >= THRESHOLD and expected_label == value:
                    worksheet.write('A' + str(row), x, border)
                    worksheet.write('B' + str(row), entities_type, border)
                    worksheet.write('C' + str(row), score, border)
                    worksheet.write('D' + str(row), value, border)
                    worksheet.write('E' + str(row), "-", border)
                    worksheet.write('F' + str(row), "-", border)
                    row += 1
                else:
                    worksheet.write('A' + str(row), x, undetected_intent)
                    worksheet.write('B' + str(row), "-", undetected_intent)
                    worksheet.write('C' + str(row), "-", undetected_intent)
                    worksheet.write('D' + str(row), "-", undetected_intent)
                    worksheet.write('E' + str(row), "-", undetected_intent)
                    worksheet.write('F' + str(row), "This input isn't detected on any intent", undetected_intent)
            elif entities_type == "dict":
                if r.json()["result"][entities][0]["resolved"] == "null" or r.json()["result"][entities][0]["resolved"] == "":
                    dict_key = r.json()["result"][entities][0]["resolved"]["dictKey"]
                    if dict_key == "null" or dict_key == "":
                        worksheet.write('A' + str(row), x, no_dict_key)
                        worksheet.write('B' + str(row), entities_type, no_dict_key)
                        worksheet.write('C' + str(row), score, no_dict_key)
                        worksheet.write('D' + str(row), value, no_dict_key)
                        worksheet.write('E' + str(row), "-", no_dict_key)
                        worksheet.write('F' + str(row), "This input doesn't have a dictionary key", no_dict_key)
                        row += 1
                    elif score < THRESHOLD and (dict_key != "null" or dict_key != ""):
                        worksheet.write('A' + str(row), x, below_threshold)
                        worksheet.write('B' + str(row), entities_type, below_threshold)
                        worksheet.write('C' + str(row), score, below_threshold)
                        worksheet.write('D' + str(row), value, below_threshold)
                        worksheet.write('E' + str(row), dict_key, below_threshold)
                        worksheet.write('F' + str(row), "This input is below the expected threshold", below_threshold)
                        row += 1
                    elif score >= THRESHOLD and (dict_key != "null" or dict_key != ""):
                        worksheet.write('A' + str(row), x, border)
                        worksheet.write('B' + str(row), entities_type, border)
                        worksheet.write('C' + str(row), score, border)
                        worksheet.write('D' + str(row), value, border)
                        worksheet.write('E' + str(row), dict_key, border)
                        worksheet.write('F' + str(row), "-", border)
                        row += 1
                    else:
                        worksheet.write('A' + str(row), x, undetected_intent)
                        worksheet.write('B' + str(row), "-", undetected_intent)
                        worksheet.write('C' + str(row), "-", undetected_intent)
                        worksheet.write('D' + str(row), "-", undetected_intent)
                        worksheet.write('E' + str(row), "-", undetected_intent)
                        worksheet.write('F' + str(row), "This input isn't detected on any intent", undetected_intent)
                else:
                    worksheet.write('A' + str(row), x, undetected_intent)
                    worksheet.write('B' + str(row), "-", undetected_intent)
                    worksheet.write('C' + str(row), "-", undetected_intent)
                    worksheet.write('D' + str(row), "-", undetected_intent)
                    worksheet.write('E' + str(row), "-", undetected_intent)
                    worksheet.write('F' + str(row), "This input isn't detected on any intent", undetected_intent)
        else:
            worksheet.write('A' + str(row), x, undetected_intent)
            worksheet.write('B' + str(row), "-", undetected_intent)
            worksheet.write('C' + str(row), "-", undetected_intent)
            worksheet.write('D' + str(row), "-", undetected_intent)
            worksheet.write('E' + str(row), "-", undetected_intent)
            worksheet.write('F' + str(row), "This input isn't detected on any intent", undetected_intent)
    row += 1
print("success")
workbook.close()



