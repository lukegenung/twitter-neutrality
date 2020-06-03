# based on https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
# read that file for how to generate the creds and how to use gspread to read and write to the spreadsheet

import gspread, itertools
from oauth2client.service_account import ServiceAccountCredentials


def colnum_to_string(i):
	'''
	Convert a column index to corresponding sheet column letter(s).
	'''
	string = ''
	while i > 0:
		i, remainder = divmod(i - 1, 26)
		string = chr(65 + remainder) + string
	return string


def get_data(workbook_name, sheet_name):
	print('Gathering raw data from Google Sheets...')
	print('Workbook: ', workbook_name)
	print('Worksheet: ', sheet_name)

	# Use creds to create a client to interact with the Google Drive API
	scope = ['https://spreadsheets.google.com/feeds',
	         'https://www.googleapis.com/auth/drive']
	creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
	client = gspread.authorize(creds)

	# Find a workbook by name and open the worksheet by name
	sheet = client.open(workbook_name).worksheet(sheet_name)

	# Extract and print all of the values
	list_of_hashes = sheet.get_all_records()

	print('Gathering raw data complete!\n')

	return list_of_hashes


def post_data(workbook_name, sheet_name, data):
	'''
	Clear header and data from specified Google Sheet.
	Then write provided data to the sheet.
	'''
	print('Clearing previous processed data from Google Sheets...')
	print('Workbook: ', workbook_name)
	print('Worksheet: ', sheet_name)

	# use creds to create a client to interact with the Google Drive API
	scope = ['https://spreadsheets.google.com/feeds',
	         'https://www.googleapis.com/auth/drive']
	creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
	client = gspread.authorize(creds)

	# find a workbook by name and open the worksheet by name
	sheet = client.open(workbook_name).worksheet(sheet_name)

	# get last row and col of worksheet
	last_row = sheet.row_count
	last_col = sheet.col_count

	# clear all contents on the worksheet
	clear_range = sheet.range('A1:' + colnum_to_string(last_col) + str(last_row + 1))
	
	for cell in clear_range:
		cell.value = ''

	sheet.update_cells(clear_range)
	print('Clearing data complete!\n')

	print('Posting processed data to Google Sheets...')
	print('Workbook: ', workbook_name)
	print('Worksheet: ', sheet_name)

	# set worksheet ranges to write new header and data
	data_rows = len(data)
	data_cols = len(data[0])
	header_range = sheet.range('A1:' + colnum_to_string(data_cols) + '1')
	value_range = sheet.range('A2:' + colnum_to_string(data_cols) + str(data_rows + 1))

	# get header names
	header = data[0].keys()

	# write header to sheet
	for i, val in enumerate(header):
		header_range[i].value = val

	sheet.update_cells(header_range)

	# convert data from list of dicts to list of lists (values only)
	# then flatten data into single list of values
	values = [list(x.values()) for x in data]
	values = list(itertools.chain.from_iterable(values))

	# write new data to sheet
	for i, val in enumerate(values):
		value_range[i].value = val

	sheet.update_cells(value_range)

	print('Posting processed data complete!')