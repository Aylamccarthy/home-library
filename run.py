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
print("Welcome to Home Library App.")
print("You can manage all your books here.")
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


def validate_user_option_input():
    """
    Checks if the user input is between 1-6.
    Code taken from https://stackoverflow.com/questions/
    and modified to suit the app.
    """
    while True:
        n = int(input("Please enter a number between 1 and 6: "))
        if 1 <= n <= 6:
            break


def add_book():
    """Allows user to add new entry to the library.
    """
    print("Now you can add a new book  to your library.")
    book_title = input("Please enter your book title here:\n ")
    book_author = input("Please enter the books author:\n")

add_book()


def view_all_books():
    print('Updating books...\n')
    data = books.get_all_values()
    print(data)


def get_book_titles():
    books = SHEET.worksheet('books')
    column = books.col_values(2)
    print(column)

   
    
# Taken and modified to suit the app, 
# from https://pypi.org/project/prettytable/

x = PrettyTable()
x.field_names = ["ID", "Title", "Author"]
x.add_row(["1", "Harry Potter", "J.K. Rowling"])


# def main():
show_menu()
validate_user_option_input()
add_book()
view_all_books()
get_book_titles()
print(x)
