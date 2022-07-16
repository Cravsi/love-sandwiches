"""
A Code along project for basic understanding of a python project.
"""

import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches_project')


def get_sales_data():
    """
    Get Sales figures input from the user
    """
    while True:
        print('Please enter sales data from the last market')
        print('Data should be six numbers, separated by commas')
        print('Example: 10, 20, 30, 40 ... etc. \n')

        data_str = input('Enter your data here: \n') # new line required due to heroku quirk.
        print(f'The data provided is {data_str}')

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print('Data is valid')
            break

    return sales_data


def validate_data(values):
    """
    Inside the try, str are converted to int.
    ValueError declared if strings cannot be converted
    or if there are not exactly six values.
    """
    try:
        values = [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values are required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again \n")
        return False

    return True


def calculate_surplus_data(sales_row):
    """
    Compares the sales with the stock to calculate surplus
    """
    print('Calculating surplus... \n')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - int(sales)
        surplus_data.append(surplus)

    return surplus_data


def update_worksheet(data, worksheet):
    """
    Receives a list of variable to be inserted into a worksheet
    Updates the relevant worksheet
    """
    print(f"Updating {worksheet}... \n")
    updated_worksheet = SHEET.worksheet(worksheet)
    updated_worksheet.append_row(data)
    print(f"{worksheet.capitalize()} successfully updated. \n")


def get_last_5_sales_entries():
    """
    Collects columns of data from the sales worksheet, returns
    the last 5 entries as a list of lists.
    """

    sales = SHEET.worksheet('sales')

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])

    return columns


def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print("Calculating stock data... \n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1  # extra 10% for extra profit
        new_stock_data.append(round(stock_num))

    return new_stock_data


def main():
    """
    Runs all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, 'sales')
    surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(surplus_data, 'surplus')
    sales_columns = get_last_5_sales_entries()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, 'stock')


print('Welcome to the one and only place for your automated python sandwich.')
main()
