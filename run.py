import gspread
from google.oauth2.service_account import Credentials
from prettytable import PrettyTable
from colorama import Fore, Back, Style
from art import *


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
print("Welcome to Home Library App.\n")
print("You can manage all your books here.\n")
print("Please use menu below to continue.\n")

def menu():
    """
    Show all the options 1-6 the user can choose from to manage their books
    """
    print(Fore.BLUE + """
    1. Add book
    2. Edit book
    3. Remove book
    4. View all books
    5. Show book details
    6. Exit
    """+ Style.RESET_ALL)

def show_menu():
    """
    will print menu. User is given an option between 1-6.
    """
    menu()
    user_option = input(Fore.LIGHTGREEN_EX
                            + "Please select a number from 1 to 6 "
                              "to continue: "
                            + Style.RESET_ALL)

show_menu()


def validate_user_option_input():
    """
    Checks if the user input is between 1-6.
    Code taken from https://stackoverflow.csom/questions/
    and modified to suit the app.
    """
    
    while True:
        n = int(input("Please enter a number between 1 and 6: "))
        if 1 <= n <= 6:
            break

validate_user_option_input()

def add_book():
    """Allows user to add new entry to the library.
    """
    print("Now you can add a new book  to your library.")
    book_title = input("Please enter your book title here:\n ")
    book_author = input("Please enter the books author:\n")

add_book()

def print_all_database():
    """
    Gets all values from the database and prints them
    to the terminal in a form of table generated with
    PrettyTable library.
    Maximum width of whole table is set to 79 characters.
    Each column's maximum width is set individually.
    """
    books = SHEET.worksheet('books')
    x = PrettyTable()
    x.field_names = books.row_values(1)
    x.add_rows = books.get_all_values()
    print(x)

print_all_database()



def view_all_books():
    """
    Show all the book entries from the database.
    Code taken and modified to suit the app, 
    from https://pypi.org/project/prettytable/
    """
book_list = PrettyTable()
book_list.field_names = ["ID", "Title", "Author", "Category", "Status", "Description"]
book_list.add_rows = data

view_all_books()
    
def get_book_titles():
    books = SHEET.worksheet('books')
    column = books.col_values(2)
    print(column)


def main():
    menu()
    show_menu()
    validate_user_option_input()
    add_book()
    view_all_books()
    get_book_titles()
    print(book_list)

