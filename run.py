import gspread
from google.oauth2.service_account import Credentials
from prettytable import PrettyTable
from colorama import Fore, Back, Style
from art import *
import os


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
# Open the Google Sheet by its name
SHEET = GSPREAD_CLIENT.open('home_library').sheet1
# Get the data from the sheet as a list of lists
data = SHEET.get_all_values()


# PrettyTable columns width
MAX_LEN = {"ID": 2, "Title": 24, "Author": 18, "Category": 12, "Status": 8}
# PrettyTable table width
TABLE_MAX_LEN = 79
# Book details max length for validation of inputs
ID_MAX_LEN = MAX_LEN["ID"]
TITLE_MAX_LEN = MAX_LEN["Title"]
AUTHOR_MAX_LEN = MAX_LEN["Author"]
CAT_MAX_LEN = MAX_LEN["Category"]
# description below assigned individually, it is displayed
# outside the PrettyTable tab.
DESC_MAX_LEN = 200
# Separator line
LINE = Fore.YELLOW + "#"*TABLE_MAX_LEN + Style.RESET_ALL  # 79 characters long
# Reading status
READ_YES = "Read"
READ_NO = "Not read"
APP = "Home Library App"

# Description of the 6 main functions of the app.
ADD_BOOK = Fore.LIGHTYELLOW_EX + """
Now you can add a new book to your library. \n
You will be asked to enter book title, author, category and status.
Choose if you have read the book or not. Book ID is generated automatically.
""" + Style.RESET_ALL

EDIT_BOOK = Fore.LIGHTYELLOW_EX \
            + "You can update all book details below." \
            + Style.RESET_ALL

REMOVE_BOOK = Fore.LIGHTYELLOW_EX \
              + "Here you can remove selected book from the database." \
              + Style.RESET_ALL

VIEW_ALL_BOOKS = Fore.LIGHTYELLOW_EX \
                 + f"This is the list of all your books." \
                 + Style.RESET_ALL

SHOW_BOOK_DETAILS = Fore.LIGHTYELLOW_EX \
                    + "This is detailed view of the book entry." \
                    + Style.RESET_ALL
END_SCREEN = Fore.LIGHTYELLOW_EX + """
This App was developed by Ayla McCarthy as Project Portfolio 3
for Diploma in Full Stack Software Development
at Code Institute.

Visit my profiles: 
https://github.com/aylamccarthy
https://www.linkedin.com/in/aylamccarthy/
""" + Style.RESET_ALL


def logo():
    """
    https://patorjk.com/software/taag/#p=display&f=Standard&t=Home%20Library
    """
    print(Fore.LIGHTCYAN_EX + """
     _   _                        _     _ _                          
    | | | | ___  _ __ ___   ___  | |   (_) |__  _ __ __ _ _ __ _   _ 
    | |_| |/ _ \| '_ ` _ \ / _ \ | |   | | '_ \| '__/ _` | '__| | | |
    |  _  | (_) | | | | | |  __/ | |___| | |_) | | | (_| | |  | |_| |
    |_| |_|\___/|_| |_| |_|\___| |_____|_|_.__/|_|  \__,_|_|   \__, |
                                                                |___/ 
    """ + Style.RESET_ALL)
    print(Fore.LIGHTGREEN_EX
          + f"Welcome to {APP}, you can manage all your books here."
            f"\nPlease use Menu below to continue." + Style.RESET_ALL)


logo()


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
    """ + Style.RESET_ALL)


def clear_terminal():
    """
    Clears terminal for better screen readability.
    Method found on StackOverflow:
    https://stackoverflow.com/questions/2084508/clear-terminal-in-python
    """
    os.system("cls" if os.name == "nt" else "clear")


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


def database_check():
    """
    Checks if database is not empty.
    If it's empty, user is asked to add his first book.
    Majority of app functionalities are disabled if DB is empty.
    """
    while True:
        # checks if there is a record below DB headers
        is_empty = len(SHEET.row_values(2))
        if is_empty == 0:
            clear_terminal()
            print(Fore.LIGHTRED_EX + "Database is empty, add at least "
                                     "one book to continue." + Style.RESET_ALL)
            return True

        break


def validate_string(user_text, max_length, element):
    """
    Validates user input, checks if input is too short or too long,
    if it's empty, or starts with special character.
    :param element: is variable assigned to user input, e.g. title, author
    :param user_text contains prompt to enter text
    :param max_length - max characters allowed in input
    """

    while True:
        user_input = input(user_text)
        # checks if input is empty
        if len(user_input) == 0:
            clear_terminal()
            print(Fore.LIGHTRED_EX + f"{element.capitalize()} can't be empty!"
                                   + Style.RESET_ALL)
        # checks if first character of the string is not special character
        elif not user_input[0].isalnum():
            print(Fore.LIGHTRED_EX
                  + f"{element.capitalize()} has to start with letter "
                    f"or digit!"
                  + Style.RESET_ALL)
        # checks if input is shorter than required 3 characters
        elif len(user_input) <= 2:
            clear_terminal()
            print(Fore.LIGHTRED_EX + "Please enter at least 3 characters..."
                                   + Style.RESET_ALL)
        # checks if input is longer than maximum allowed
        elif len(user_input) > int(max_length):
            clear_terminal()
            print(
                Fore.LIGHTRED_EX
                + f"Entered {element} exceeds maximum "
                  f"allowed length of {max_length} characters!"
                + Style.RESET_ALL)
        else:
            element = user_input.title()
            return element


def validate_num_range(user_input, first_val, last_val):
    """
    Checks if user input is within the range of possible options.
    Any input out of desired range will give user a hint showing
    a message containing exact range of possible options.
    :param user_input: this is user input
    :param first_val: this is first option from the range of options
    :param last_val:  this is the last option from the range of options
    :returns True if user's input is valid
    :returns False if user's input is invalid
    """
    try:
        options = list(range(first_val, last_val + 1))
        allowed_options = [str(i) for i in options]

        if user_input in allowed_options:
            return True
        else:
            raise ValueError
    except ValueError:
        clear_terminal()
        print(Fore.LIGHTRED_EX +
              f"\nWrong input, please select option from "
              f"{first_val} to {last_val} "
              f"to continue..." + Style.RESET_ALL)


def add_book():
    """
    Allows user to add new book to database using user input with following
    data: author, title, category, read status and description.
    The ID of the book is generated and added automatically for each new entry.
    Function looks up the database for first empty row and inserts new entry
    there. After adding new book the database is re-sorted and all ID values
    are renumbered to keep ascending order in the database.
    """
    print(ADD_BOOK)
    print(LINE)
    
    # initialize variable to store all book details from user input
    book_to_be_added = []

    while True:
        # user inputs title, then it's being validated, max 24 char allowed
        title = validate_string(Fore.LIGHTCYAN_EX
                                + "Please enter book's title: "
                                + Style.RESET_ALL, TITLE_MAX_LEN,
                                "title")
        # user inputs author then it's being validated, max 16 char allowed
        author = validate_string(Fore.LIGHTCYAN_EX
                                 + "Please enter book's author: "
                                 + Style.RESET_ALL, AUTHOR_MAX_LEN,
                                 "author")
        # user inputs category then it's being validated, max 12 char allowed
        category = validate_string(Fore.LIGHTCYAN_EX
                                   + "Please enter book's category: "
                                   + Style.RESET_ALL, CAT_MAX_LEN,
                                   "category")
        # user choose book reading status, allowed input is 1 or 2
        while True:
            status = input(Fore.LIGHTCYAN_EX
                           + "Please select \"1\" if you read that book "
                             "or \"2\" if you didn't: "
                           + Style.RESET_ALL)
            # checks if user input is digit in range 1-2
            if validate_num_range(status, 1, 2):
                if status == "1":
                    status = READ_YES
                    break
                elif status == "2":
                    status = READ_NO
                    break

        description = validate_string(
            Fore.LIGHTCYAN_EX + "Please enter book's description: "
                              + Style.RESET_ALL, DESC_MAX_LEN,
                                "description")

        break
   
    clear_terminal()
    print(LINE)
    row = ["", title, author, category, status, description]
    book_to_be_added.insert(0, row)
    SHEET.append_row(row)   # Append the row to the sheet
    print("Your new book is added successfully!") 
    print(LINE)


def edit_book():
    """
    This function allows the user to edit a book, update the sheet with the 
    edited data, and then print the updated data to the console.
    """
    
    data = SHEET.get_all_values()
     #  Create a PrettyTable with the data from the sheet
    table = PrettyTable(["Title", "Author", "Category", "Status"])
    table.field_names = data[0]
    row = [title, author, category, status,]
    for row in data[1:]:
        table.add_row(row)

    # Print the table to the console
    print(table)

    # Prompt the user to edit the data
    while True:
        row_index = input("Enter the index of the row you want to edit, or type 'q' to quit: ")
        if row_index.lower() == 'q':
            break
        try:
            row_index = int(row_index)
            if row_index < 1 or row_index > len(data) - 1:
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 6 or 'q' to quit.".format(len(data) - 1))

    if row_index:
         #  Prompt the user for the updated data
        title = input("Enter the updated title: ")
        author = input("Enter the updated author: ")
        category = input("Enter the updated category: ")
        status = input("Enter the updated status: ")
        
        # Update the row in the sheet with the new data
        SHEET.update_cell(row_index + 1, 1, title)
        SHEET.update_cell(row_index + 1, 2, author)
        SHEET.update_cell(row_index + 1, 3, category)
        SHEET.update_cell(row_index + 1, 4, status)
        
        # Print the updated table to the console
        data = SHEET.get_all_values()
        table = PrettyTable(["Title", "Author", "Category", "Status"])
        table.field_names = data[0]
        for row in data[1:]:
            table.add_row(row)
        print(table)


def print_all_database():
    """
     Gets all values from the database and prints them
     to the terminal in a form of table generated with
     PrettyTable library.
    """
    table = PrettyTable()  # Create a new table instance
    # Define the columns of the table based on the first row of the data
    table.field_names = data[0]

    # Insert the data into the table
    for row in data[1:]:
        table.add_row(row)

    # Print the table
    print(table)


def show_all_books():
    """
     Prints to the terminal a list of all books stored in the database.
     If database is empty database_check() prompts user to add first book.
    """
    if database_check():
        pass
    else:
        print(LINE)
        print_all_database()
        print(LINE)


def validate_yes_no(user_input):
    """
    Validates Y/N inputs.
    Prints user feedback if input is invalid.
    :param user_input - contains user choice
    :return True if valid input is given
    """
    try:
        valid_options = ["y", "Y", "n", "N"]
        if user_input in valid_options:
            return True
        else:
            raise ValueError
    except ValueError:
        clear_terminal()
        print(Fore.LIGHTRED_EX
              + "\nWrong input, please select \"Y\" or \"N\".\n"
              + Style.RESET_ALL)


user_input = input()


def exit_app():
    """
     This function prints goodbye message to the user.
     User is asked to confirm exit.
    """
    while True:
        are_you_sure = input(Fore.LIGHTYELLOW_EX
                             + "\nAre you sure you want to quit? Y/N: "
                             + Style.RESET_ALL)
        if validate_yes_no(are_you_sure):

            if "y" in are_you_sure or "Y" in are_you_sure:
                clear_terminal()
                print(Fore.LIGHTYELLOW_EX
                      + f"Thank you for using {APP} app!"
                      + Style.RESET_ALL)
                print(END_SCREEN)
                print(Fore.LIGHTYELLOW_EX + "\nTerminating..."
                                          + Style.RESET_ALL)
                break
            else:
                clear_terminal()
                show_menu()

        else:
            exit_app()

        break


def show_menu():
    """
    Will print menu. User is given an option between 1-6.
    """
    while True:
        menu()  # prints menu
        user_option = input(Fore.LIGHTGREEN_EX
                            + "Please select a number from 1 to 6 "
                              "to continue:\n "
                            + Style.RESET_ALL)

        clear_terminal()
        # validates user input only values from 1 to 6 are allowed
        validate_user_option_input()
        if user_option == "1":
            add_book()
        elif user_option == "2":
            edit_book()
        elif user_option == "3":
            print(VIEW_ALL_BOOKS)
            print_all_database()
        elif user_option == "4":
            show_all_books()
        elif user_option == "5":
            show_book_details()
        elif user_option == "6":
            exit_app()
            break


show_menu()


def main():
    """
    Main function of the program. 
    Shows App menu, where user can start and further use 
    all the app functionalities.
    """
    logo()
    menu()
    show_menu()
    add_book()
    # edit_book()
    view_all_books()
    get_book_titles()
    clear_terminal()
    exit_app()
    validate_yes_no(user_input)
    validate_user_option_input()
    print_all_database()


main()
