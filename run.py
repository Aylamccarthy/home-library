import gspread
from google.oauth2.service_account import Credentials
from prettytable import PrettyTable
from colorama import Fore, Back, Style
from art import *
import os
import textwrap


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

# App constants
HEADERS = SHEET.row_values(1)
HEADERS_NO_DESC = HEADERS[:-1]
HEADERS_NO_DESC_NO_ID = HEADERS[:-1]
DESCRIPTION = SHEET.row_values(1).pop()
ALL_VALUES = SHEET.get_all_values()
ALL_VALUES_NO_HEADER = ALL_VALUES[1:]
APP = "Home Library App"
# Reading status
READ_YES = "Read"
READ_NO = "Not read"

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

# Initialize two values to store id's of first and last book.
# They are used later to determine valid input range and DB length.
first_book_id = ""
last_book_id = ""

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
        validate_num_range(user_option, 1, 6)
        if user_option == "1":
            add_book()
        elif user_option == "2":
            edit_book()
        elif user_option == "3":
            remove_book()
        elif user_option == "4":
            show_all_books()
        elif user_option == "5":
            show_book_details()
        elif user_option == "6":
            exit_app()
            break


def clear_terminal():
    """
    Clears terminal for better screen readability.
    Method found on StackOverflow:
    https://stackoverflow.com/questions/2084508/clear-terminal-in-python
    """
    os.system("cls" if os.name == "nt" else "clear")


def wrap_text(text):
    """
    The function uses textwrap library to wrap long strings
    over 79 characters to the new line. It's used to correctly display
    books description.
    :param text - any string
    """
    wrapper = textwrap.TextWrapper(width=79)
    wrapped_text = wrapper.fill(text=text)
    print(wrapped_text)


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


def renumber_id_column():
    """
    Suggestion from my mentor.
    This function will also be used to generate book ID.
    Renumber values in column 1 in the worksheet
    This will be used later to keep values in order
    when book is added or removed.
    """
    col = SHEET.col_values(1)  # assigns values from column 1
    new_col = col[1:]  # slices out the headers
    id_val = 1  # allows to start ID values from 1
    row_val = 2  # allows to start iteration from row 2

    # underline used to avoid using variable without later need
    for _ in new_col:
        # renumbering ID value to keep order
        SHEET.update_acell("A" + str(row_val), id_val)
        id_val += 1
        row_val += 1
    print(Fore.LIGHTYELLOW_EX + "Updating database..." + Style.RESET_ALL)


def how_many_books():
    """
    Checks if there is one more books in the database.
    This will be used later in edit_book, remove_book,
    and show_book_detais functions to conditionally give
    user hint on possible input selection, e.g. "Choose the
    ony book you have" or "Choose book from 1 to 10".
    """
    all_books = SHEET.col_values(1)[1:]  # list of IDs of all books
    global first_book_id
    global last_book_id

    if len(all_books) == 1:
        return True
    elif len(all_books) > 1:
        first_book_id = all_books[0]
        last_book_id = all_books[-1]
        return False

    return first_book_id, last_book_id


def database_check():
    """
    Checks if database is not empty.
    If it's empty, user is asked to add his first book.
    Majority of app functionalities are disabled if DB is empty.
    Checks if the user input is between 1-6.
    Code taken from https://stackoverflow.csom/questions/
    and modified to suit the app.
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

    # insert all collected inputs into the list
    book_to_be_added.extend([title, author, category, status,
                             description])
   
    clear_terminal()
    print("Here's the details of your new book:")
    first_empty_row = len(SHEET.get_all_values())
    book_to_be_added.insert(0, first_empty_row)
    print(LINE)
    
    # The code below iterates through two lists using the zip method
    # as shown in "Love Sandwiches" project.
    # First list with database headers and second list with book details.
    # Then it prints output for each pair. e.g. AUTHOR: "J.K. Rowling"
    for header, item in zip(range(len(HEADERS_NO_DESC)),
                            range(len(book_to_be_added))):
        print(f"{HEADERS_NO_DESC[header]}: " + Fore.LIGHTGREEN_EX
              + f"{book_to_be_added[item]}" + Style.RESET_ALL)

    print(f"\n{DESCRIPTION}: ")
    wrap_text(Fore.LIGHTGREEN_EX + book_to_be_added[-1].capitalize()
                                 + Style.RESET_ALL)

    print(LINE)

    # The code below prompts the user to confirm if they want to add
    # book to the database. If the answer is yes, it adds the book to the
    # database. If no, the process is aborted and the book
    # will not be added to the database.

    while True:
        are_you_sure = input(Fore.LIGHTYELLOW_EX
                             + " \nConfirm adding this book. Y/N: "
                             + Style.RESET_ALL)
        if validate_yes_no(are_you_sure):

            if "y" in are_you_sure or "Y" in are_you_sure:
                clear_terminal()
                SHEET.append_row(book_to_be_added)
                print(Fore.LIGHTYELLOW_EX + "\nAdding book to the database..."
                                          + "\nUpdating database. Please wait..."
                                          + "\nBook added successfully."
                                          + Style.RESET_ALL)
                break
            # negative answer breaks the loop and takes user back
            elif "n" in are_you_sure or "N" in are_you_sure:
                clear_terminal()
                print(Fore.LIGHTRED_EX + "Aborting... Book has not been added."
                      + Style.RESET_ALL)
                break
    

def edit_book():
    """
    The function first checks if the database exists and is populated.
    If it does not, the function exits.If the database exists and is populated, 
    the function displays all books in the database, and prompts the user to 
    select a book to edit. The user is then presented with the details of
    the selected book in the form of a table, and is prompted to select
    which detail they would like to edit.The function then validates the user's
    input. If the user enters a valid input, the function updates the database
    and displays a success message. The user is then prompted to either
    keep editing the book or return to the main menu.
    """
    if database_check():
        pass
    else:
        allowed_input = SHEET.col_values(1)[1:]

        while True:
            print(EDIT_BOOK)
            show_all_books()
            user_choice = input(Fore.LIGHTYELLOW_EX
                                + "\nWhich book would you like to edit?: "
                                + Style.RESET_ALL)
            clear_terminal()

            if user_choice in allowed_input:
                # finds book in the database, counting in list's zero-notation
                db_row = int(user_choice) + 1
                # assigns exact row to variable
                book_id =SHEET.row_values(db_row)
                book_description = str(book_id[-1])
                book_no_desc = book_id[:-1]

            def print_edited_book():
                print(EDIT_BOOK)
                print(LINE)
                x = PrettyTable()
                # assigns table's headers from first row in database
                x.field_names = HEADERS_NO_DESC
                x._max_table_width = TABLE_MAX_LEN
                x._max_width = MAX_LEN
                x._align["Title"] = "l"  # aligns column to the left
                # inserts a list with book details to the table
                x.add_rows([book_no_desc])
                print(x)  # prints table to the terminal
                print(f"\n{DESCRIPTION}: ")
                # book description can be longer text that will
                # be wrapped to the new line over 79 characters.
                wrap_text(book_description)
                print(LINE)
            
            # The code below will allow the user to choose what data
            # he wants to edit, i.e, Title, Author, etc.
            while True:
                print_edited_book()
                print(Fore.LIGHTGREEN_EX + """
                1. Title 
                2. Author
                3. Category
                4. Status
                5. Description
                6. Return 
                """ + Style.RESET_ALL)
                user_choice = input(Fore.LIGHTYELLOW_EX
                                        + "What do you want to edit? "
                                          "Select 1-6: "
                                        + Style.RESET_ALL)
                validate_num_range(user_choice, 1, 6)

                if user_choice == "1":
                    title = validate_string(Fore.LIGHTCYAN_EX
                    + "Please update book's title: "
                    + Style.RESET_ALL, TITLE_MAX_LEN,"Title"
                    )
                    book_no_desc[1] = title.title()
                    SHEET.update_cell(db_row, 2, title.title())
                    print(Fore.LIGHTYELLOW_EX + "Updating database..."
                              + Style.RESET_ALL)
                    clear_terminal()
                    print(Fore.LIGHTGREEN_EX
                              + f'Book title updated successfully to '
                                f'"{title.title()}".\n'
                              + Style.RESET_ALL)
                    print(Fore.LIGHTYELLOW_EX
                              + "Keep editing this book or return to "
                                "main menu."
                              + Style.RESET_ALL)

                elif user_choice == "2":
                    author = validate_string(Fore.LIGHTCYAN_EX
                    + "Please update book's author"
                    + Style.RESET_ALL, TITLE_MAX_LEN,"author")
                    book_no_desc[2] = author.title()
                    SHEET.update_cell(db_row, 3, author.title())
                    clear_terminal()
                    print(
                        Fore.LIGHTGREEN_EX
                        + f'Book author updated successfully'
                          f'to "{author.title()}".\n'
                        + Style.RESET_ALL)
                    print(Fore.LIGHTYELLOW_EX 
                        + "Keep editing this book "
                          "or return to main menu."
                        + Style.RESET_ALL)

                elif user_choice == "3":
                    category = validate_string(
                        Fore.LIGHTCYAN_EX 
                        + "Please update books category:"
                        + Style.RESET_ALL, CAT_MAX_LEN, "category")
                    book_no_desc[3] = category.capitalize()
                    SHEET.update_cell(db_row, 4, category.capitalize())
                    clear_terminal()
                    print(
                            Fore.LIGHTGREEN_EX
                            + f'Book category updated successfully '
                              f'to "{category.capitalize()}".\n'
                            + Style.RESET_ALL)
                    print(Fore.LIGHTYELLOW_EX
                         + "Keep editing this  book or"
                            "return to main menu."
                         + Style.RESET_ALL)

                elif user_choice == "4":
                    while True:
                        select_status = input(
                                Fore.LIGHTCYAN_EX
                                + "Please select \"1\" if you read that book "
                                  "or \"2\" if you didn't: "
                                + Style.RESET_ALL)
                    if validate_num_range(select_status, 1, 2):
                        if select_status == "1":
                            status = READ_YES
                            book_no_desc[4] = status
                            SHEET.update_cell(db_row, 5, status)
                            clear_terminal()
                            print(
                                Fore.LIGHTGREEN_EX
                                + f'Book status updated successfully '
                                  f'to "{status.lower()}".\n'
                                + Style.RESET_ALL)
                            print(Fore.LIGHTYELLOW_EX
                                + "Keep editing this book or return "
                                  "to main menu."
                                + Style.RESET_ALL)
                            break
                        elif select_status == "2":
                            status = READ_NO
                            book_no_desc[4] = status
                            SHEET.update_cell(db_row, 5, status)
                            clear_terminal()
                            print(Fore.LIGHTGREEN_EX
                                 + f'Book status updated successfully'
                                   f'to "{status.lower()}".\n'
                                 + Style.RESET_ALL)
                            print(Fore.LIGHTYELLOW_EX
                                 + "Keep editing this book or return "
                                   "to main menu."
                                 + Style.RESET_ALL)
                            break

                elif user_choice == "5":
                    description = \
                            validate_string(Fore.LIGHTCYAN_EX 
                        + "Please update book's description:"
                        + Style.RESET_ALL, DESC_MAX_LEN,
                                            "description")
                    SHEET.update_cell(db_row, 6,
                                    description.capitalize())
                    book_description = description.capitalize()
                    clear_terminal()
                    print(Fore.LIGHTGREEN_EX
                              + f"Book description updated successfully.\n"
                              + Style.RESET_ALL)
                    print(Fore.LIGHTYELLOW_EX
                              + "Keep editing this book or return."
                              + Style.RESET_ALL)
                    
                
                elif user_choice == "6":  # returns to previous menu
                    clear_terminal()
                    show_all_books()
                    break

                
                


                   

                





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


def remove_book():
    """
    Function allows user to remove whole database entry for selected book.
    Loop is used to ask user to select book to be removed.
    The input is then validated. In case of wrong input,
    user is asked to select book, e.g. 1-20.
    User is asked to confirm choice before deletion. 
    The input is then validated. Book is removed if
    positive answer is given.
    """
    if database_check():  # checks if database is not empty
        pass
    else:
        print(REMOVE_BOOK)
        show_all_books()  # prints a list of all books in the database
        # creates a list with all input to check agains
        allowed_input = SHEET.col_values(1)[1:]

        # The loop below is used to ask user to select book to be removed.
        while True:
            user_choice = input(
                Fore.LIGHTYELLOW_EX
                                + "\nPlease select a book to remove (#ID): "
                                + Style.RESET_ALL
            )

            if user_choice in allowed_input:
                # finds database row counting in list zero notation
                db_row = int(user_choice) + 1
                row_str = str(db_row)
                delete_title = SHEET.acell("B" + row_str).value
                delete_author = SHEET.acell("C" + row_str).value
                delete_status = SHEET.acell("E" + row_str).value
                clear_terminal()

                # the condition below is used to print different message
                # depending on book's read status
                if delete_status == READ_YES:
                    confirm = f"The book \"{delete_title.title()}\" by " \
                              f"{delete_author.title()} will be removed."
                    read_status = \
                        Fore.LIGHTGREEN_EX \
                        + f"The book is {delete_status.lower()}." \
                        + Style.RESET_ALL
                    wrap_text(Fore.LIGHTYELLOW_EX + confirm + Style.RESET_ALL)
                    print(read_status)

                elif delete_status == READ_NO:
                    confirm = f"The book \"{delete_title.title()}\" " \
                              f"by {delete_author.title()} will be removed."
                    read_status = \
                        Fore.LIGHTRED_EX \
                        + f"The book is {delete_status.lower()}." \
                        + Style.RESET_ALL
                    wrap_text(Fore.LIGHTYELLOW_EX + confirm + Style.RESET_ALL)
                    print(read_status)

                while True:
                    are_you_sure = \
                        input(Fore.LIGHTRED_EX
                              + "\nAre you sure you want to delete "
                                "this book? Y/N: "
                              + Style.RESET_ALL)
                    if validate_yes_no(are_you_sure):

                        if "y" in are_you_sure or "Y" in are_you_sure:
                            SHEET.delete_rows(db_row)
                            clear_terminal()
                            print(Fore.LIGHTYELLOW_EX
                                  + "Removing book, please wait..."
                                  + Style.RESET_ALL)
                            renumber_id_column()
                            print(Fore.LIGHTGREEN_EX
                                  + "Book removed. Database updated "
                                    "successfully."
                                  + Style.RESET_ALL)
                            break

                        elif "n" in are_you_sure or "N" in are_you_sure:
                            clear_terminal()
                            print(Fore.LIGHTRED_EX
                                  + "Aborting... Database hasn't been changed."
                                  + Style.RESET_ALL)
                            break
                            
                    else:
                        clear_terminal()
                        print(Fore.LIGHTRED_EX
                              + "Wrong input, please select \"Y\" or \"N\"..."
                              + Style.RESET_ALL)

            else:
                clear_terminal()
                # checks how many books are in the database, if there's only
                # one,the user is asked to select the only possible option.
                if how_many_books():
                    print(Fore.LIGHTRED_EX +
                          "Wrong input!\nNot much of a choice, "
                          "you have only one book, please select it...\n"
                          + Style.RESET_ALL)
                # if there is more than one book in the database,
                # the user is given range of options, e.g. 1-10
                elif how_many_books() is False:
                    print(Fore.LIGHTRED_EX +
                          f"Wrong input!\nPlease select #ID from 1 "
                          f"to {last_book_id}.\n"
                          + Style.RESET_ALL)
                remove_book()

            break


def show_all_books():
    """
     Prints to the terminal a list of all books stored in the database.
     If database is empty database_check() prompts user to add first book.
    """
    if database_check():
        pass
    else:
        print(VIEW_ALL_BOOKS)
        print(LINE)
        print_all_database()
        print(LINE)


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


def main():
    """
    Main function of the program. 
    Shows App menu, where user can start and further use
    all the app functionalities.
    """
    logo()
    show_menu()


main()
