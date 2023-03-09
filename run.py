import gspread
from google.oauth2.service_account import Credentials
from prettytable import PrettyTable

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('home_library')

books = SHEET.worksheet('books')
data = books.get_all_values()

def view_all_books():
    print('Updating books...\n')
    data = books.get_all_values()
    print(data)

view_all_books()

def get_book_titles():
    books = SHEET.worksheet('books')
    column = books.col_values(2)
    print(column)
get_book_titles()


def add_book():
    book_title = input("Please enter your book title here: ")

add_book()
    
# Taken and modified to suit the app, 
# from https://pypi.org/project/prettytable/

x = PrettyTable()
x.field_names = ["ID", "Title", "Author"]
x.add_row(["1", "Harry Potter", "J.K. Rowling"])

print(x)