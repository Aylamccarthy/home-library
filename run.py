from colorama import Fore, Back, Style


def menu():
     print(Fore.LIGHTGREEN_EX + """
    1. Add book
    2. Edit book
    3. Remove book
    4. View all books
    5. Show book details
    6. Exit
    """ + Style.RESET_ALL)

menu()

def show_menu():
    while True:
        menu()
        user_choice = input(Fore.LIGHTYELLOW_EX
                            + "Please select a number from 1 to 6 "
                              "to continue: "
                            + Style.RESET_ALL)
        clear_terminal()
        # validates user input, only values from 1 to 6 are allowed
