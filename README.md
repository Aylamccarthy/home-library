<h1 align = "center">Home Library App- Python Project </h1>

### Student Developer: Ayla McCarthy

<b>[View live program here]() </b>  


![Program mockup]

The Home Library App was created as Portfolio Project #3 (Python Essentials) for Diploma in Full Stack Software Development at [Code Institute](https://www.codeinstitute.net). It allows users to manage their personal/family book libraries, view, add, update, and remove books.

Project purpose was to build a command-line python application that allows user to manage a common dataset about a particular domain.

# Table of Content

*   [Project](#project)
    *   [Strategy/Scope](#strategyscope)
    *   [Site owner goals](#site-owner-goals)
    *   [External user's goal](#external-users-goal)
*   [User Experience (UX/UI)](#user-experience-ux)
*   [Logic and features](#logic-and-features)
    *   [Python logic](#python-logic)
    *   [Database structure](#database-structure)
    *   [Features](#features)
        *   [Main menu](#main-menu)
        *   [Add book](#add-book)
        *   [Update book](#edit-book)
        *   [Remove book](#remove-book)
        *   [View all books](#view-all-books)
        *   [Search book](#)
        *   [Show book details](#show-book-details)
        *   [Exit](#exit)
*   [Technology](#technology)
    *   [Software used](#software-used)
    *   [Python libraries/modules](#python-librariesmodules)
*   [Testing](#testing)
    *   [Accessibility](#accessibility)
    *   [Validation](#validation)
    *   [Manual testing](#manual-testing)
    *   [Bugs/known issues](#bugsknown-issues)
*   [Deployment](#deployment)
    *   [Git and GitHub](#git-and-github)
    *   [Deployment to Heroku](#deployment-to-heroku)
*   [Possible future development](#possible-future-development)
*   [Credits](#credits)
    *   [Code](#code)
    *   [Media](#media)
    *   [Acknowledgements](#acknowledgements)


# Project
## Strategy/Scope

I chose to develop an application that can be used in real life. This idea came to mind when I was brainstorming on what app to develop to help my life as a parent taking care of a young family. Initially I thought about a weekly grocery shopping list app, but when I saw our books all over the house, that's when I decided, an app to manage these books would be perfect! Home Library App was designed to allows users to manage their personal/family book libraries. The application offers functionalities such as: viewing book database, adding, updating and removing books.

The application should have a clean and intuitive user interface and offer easy access and navigation to all functionalities.

To achieve the strategy goals, I implemented the following features:

- Customised terminal display page for better visual experience.
- Colours in terminal to give user feedback dependent on his actions.
- Reliable and quick connection with database provided by Google.
- Menu with easy access to all features and possibility to exit or restart the application.
- Clean user interface for easy navigation and readability.

## Site owner goals

As a program owner/developer I would like to:
- create application that has real life usage,
- create application that is easy to use and intuitive to navigate,
- provide user a feedback to every input and action,
- decide what kind of user input is allowed by implementing validations,
- try my best to build a bug free application.


##  External user's goal

As a user I would like to:
- be able to clearly understand application's purpose from the first contact,
- be able to use program in real life,
- be able to easily navigate the program and access all features,
- be able to receive feedback to actions taken,
- be able to decide what to do next, what features to use,
- be able to quit program,

# Logic and Features

## Python Logic

A flow diagram of the logic behind the application was created using [Lucid Chart](https://www.lucidchart.com/).
![Flow diagram]()

## Database Structure

Google Sheets is used to create the application database. There is only one worksheet named "library" used to store all the data.
![database](../home-library/views/images/database.png)



## Bugs
To print data base using prettytable. I found this bug so challenging but eventually managed to solve it after days of research.
The book IDs in the database would not generate automatically as expected.

Validation on edit_book function is not working as expected

backround image and favicon are not working as expected






### Resources
Code Institute "Love Sandwiches" and learning platform
Code Institute Slack Community for unparalled support and knowledge base.
My mentor Gareth McGirr for all the support, guidance and suggestions throughout the building of this project.
Python Library Management System Project - Full Tutorial#39 | Programming is Fun
12 Python Project for Beginners | freeCodeCamp.Org
Python Tutorial for Beginners- Kevin Stratvert | Full Python Course 
Learn Python in 2023 | TechWorld with Nana
Python Google Sheets API Tutorial - 2019 |Tech With Tim 
Colorama Tutorial | Tech with Tim
Python Full Course for free | Bro Code
How to create ASCII art text in Python | Coding Professor
StackOverflow
W3Schools

