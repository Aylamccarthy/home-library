# Manual testing of validation and functionalities

Testing of application functionalities and validations were done throughout the building process.

## Main menu

Function used for inputs validation - validate_num_range()

| What is being tested | Input  | Expected response | Result  |
|---|---|---|---|
|  Please select a number from 1 to 7 to continue | "0", "abc", "empty"   |Wrong input | Pass
|  Please select a number from 1 to 7 to continue | "1" | Valid input, call add_book fn | Pass
|  Please select a number from 1 to 7 to continue | "2" | Valid input, call edit_book fn | Pass
|  Please select a number from 1 to 7 to continue | "3" | Valid input, call remove_book fn | Pass
|  Please select a number from 1 to 7 to continue | "4" | Valid input, call show_all_books fn  | Pass
|  Please select a number from 1 to 7 to continue | "5" | Valid input, call change_sorting_method fn | Pass
|  Please select a number from 1 to 7 to continue | "6" | Valid input, call show_book_details fn | Pass
|  Please select a number from 1 to 7 to continue | "7" | Valid input, call quit fn | Pass
|  Please select a number from 1 to 7 to continue | "2" (database is empty)| Valid input, prompt user to add first book | Pass
Please select a number from 1 to 7 to continue | "3" (database is empty)| Valid input, prompt user to add first book | Pass
Please select a number from 1 to 7 to continue | "4" (database is empty)| Valid input, prompt user to add first book | Pass
Please select a number from 1 to 7 to continue | "5" (database is empty)| Valid input, prompt user to add first book | Pass
Please select a number from 1 to 7 to continue | "6" (database is empty)| Valid input, prompt user to add first book | Pass



## Add book function

Function used - validate_string() 
The same function is used to validate book's author, category and description.

|  What is being tested  | Input  | Expected response  | Result
|---|---|---|---|
|  Please enter book's title | "a"  | Input too short  | Pass
|  Please enter book's title | "ab"  | Input too short  | Pass
|  Please enter book's title | empty  | Input can't be empty  | Pass
|  Please enter book's title | "!title"  | Input can't start with special char.  | Pass
|  Please enter book's title | "Book title should have a maximum 24 characters "  | Input exceeded 24 characters  | pass
|  Please enter book's title | "Epic"  | Valid input  | Pass
|  Please select "1" if you read that book or "2 if you didn't | "3"  | Wrong input  | Pass
|  Please select "1" if you read that book or "2 if you didn't | empty  | Wrong input  | Pass
|  Please select "1" if you read that book or "2 if you didn't | "0"  | Wrong input  | Pass



## Yes/No question

Function used for inputs validation - validate_yes_no().

|  What is being tested  | Input  | Expected response  | Result
|---|---|---|---|
|  Confirm adding this book. Y/N | "0", "3", "f", empty  | Wrong input  | Pass
|  Confirm adding this book. Y/N |  "y", "Y" | Valid input, proceed | Pass
|  Confirm adding this book. Y/N |  "n", "N" | Valid input, abort  | Pass



# Update book function

|  What is being tested  | Input  | Expected response  | Result
|---|---|---|---|
|  Which book would you like to edit? | "6" (5 records exist)  | Wrong input, please select ID from 1 to 5  | Pass
|  Which book would you like to edit? | "g", empty (5 records exist)  | Wrong input, please select ID from 1 to 5  | Pass
|  Which book would you like to edit? | "5" (5 records exist )  | Input valid, show book #5  | Pass
|  What do you want to edit? Select 1-6 | "0", "a", "`", empty (6 possible choices )  | Wrong input | Pass
|  What do you want to edit? Select 1-6 | "7" (6 possible choices )  | Wrong input | Pass

The same validation method is used for input of author, title, category, status and description for both "add book" and "update book" features.


## Remove book function

|  What is being tested  | Input  | Expected response  | Result
|---|---|---|---|
|  Please select a book to remove (#ID) | "0", "a", empty (5 records exist) | Wrong input | Pass
|  Are you sure you want to delete this book? Y/N | "0", "b", empty | Wrong input | Pass
|  Are you sure you want to delete this book? Y/N | "n" | Valid input, return | Pass
|  Are you sure you want to delete this book? Y/N | "Y" | Valid input, remove book | Pass


## Show book details function

Function used for inputs validation - validate_num_range()

|  What is being tested  | Input  | Expected response  | Result
|---|---|---|---|
| Which book details would you like to see? | "9" (10 records exist)  | Wrong input  | Pass
| Which book details would you like to see? | "5"  | Valid input, show book details  | Pass
| Which book details would you like to see? | "abc", "!"  | Wrong input              | Pass
| Which book details would you like to see? | "2", | Valid input                     | Pass


## Search Book function

|  What is being tested  | Input  | Expected response  | Result
| If you wish to search by book title,press 1: | "0"  | Wrong input  | Pass
|If you wish to search by book author, press 2:| "2"  | Valid input  | Pass
|Please enter book's title:                    |"Matilda"| Valid input | Pass
|Please enter book's title:                    | "12"    | Wrong input | Pass
|Please enter author's name:                   | "12"    | Wrong input | Pass
|Please enter author's name:                   | "Dahl"    | Valid input | Pass


# Exit function

|  What is being tested  | Input  | Expected response                         | Result
|---|---|---|---|
| Are you sure you want to quit? | "n"  | Valid input, return  to main menu   | Pass
| Are you sure you want to quit? | "01", "!", empty | Wrong input             | Pass
| Are you sure you want to quit? | "y"  | Valid input, terminate program      | Pass


