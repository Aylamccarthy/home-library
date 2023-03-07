from colorama import Fore, Back, Style


def menu():
     print(Fore.LIGHTGREEN_EX + """
    1. Add book
    2. Edit book
    3. Remove book
    4. View all books
    5. Change sorting method
    6. Show book details
    7. Quit
    """ + Style.RESET_ALL)

menu()