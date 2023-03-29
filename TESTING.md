# Manual testing of validation and functionalities

Testing of application functionalities and validations were done throughout the building process.

## Main menu
Function used for inputs validation - validate_num_range in utils/utils.py

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
