# SimpleDebt Project planning

This document will be used to plan the project. Consists in the logical part of making (a Splitwise type) a system to pay bills between friends. Everybody registers its payments and for whom, as well as a description and automatically the date. The system then calculates the debts and displays in a table who owes what to whom, as well as a table that shows the minimum amount of transactions to pay all debts. As a nice to have it might be possible to add a statistics page that shows the total amount of money spent by each person, the total amount for category, total amount for each person per category, the person that spent the most money, the person that spent the least money, with who the groups spent the most, with who the least, etc.

## Logical abstract steps

1. Register users and form groups
2. Register payments
3. Calculate individual debt for each payment
4. Calculate the balance of each user
5. Calculate the minimum amount of transactions to pay all debts
6. Display the results

## Logical detailed steps

1. Register users and form groups (Relational database)
    1. Create a user: name, ID of user, balance, ID of group (foreign key), (total contribution, total debt. *possible*)
    2. Create a group: name, ID of group
    3. Add users to a group: the user table has a column with the ID of the group as a foreign key
2. Register payments (Relational database)
    1. Create a payment: ID of payment, ID of user paying (foreign key), ID of users receiving (foreign key)(a new table), amount, amount per user, description, date, category
    // Category might be determined by the description using NLP
    // A little check box to include or not the user paying in the users receiving
    // Future possible: percentage of each user or amount per user for exact amount
3. Calculate individual debt for each payment (Python)
    1. Do a query to the database to get the amount of the payment and the amount of users receiving it
    2. Calculate the amount per user (amount / amount of users receiving)
    3. Update the database with the amount per user
4. Calculate the balance of each user (Python)
    1. Do a query to the database to get the amount per user for each payment
    2. Calculate the total debt for each user
    // Possible show the debt for each payment
    3. Calculate the total contribution for each user
    // Possible show the contribution for each payment
    4. Calculate the balance for each user (total contribution - total debt)
    5. Update the database with the balance for each user
5. Calculate the minimum amount of transactions to pay all debts (Python)
    1. Do a query to the database to get the balance for each user
    2. Calculate the minimum amount of transactions to pay all debts
6. Display the results (Python)
    1. Do a query to the database to get the balance for each user
    2. Display the results in a table

### Register users and form groups

Group table:
| IDGroup (Int autofield)(PK) | Name (Varchar)
|----|------|
| 1  | HEMT |
| 2  | Quimica |
| 3 | ... |

User table:
| IDUser (Int autofield)(PK) | Name (Varchar) | IDGroup (Int)(FK) | Balance (Int) | TotalContribution (Int) | TotalDebt (Int) |
|----|------|----|----|----|----|
| 1 | Carlos | 1 | 0 | 20 | 85 |
| 2 | Hector | 1 | 0 | 50 | 20 |
| 3 | Gi | 2 | 0 | 30 | 30 |
| 4 | ... | ... | ... | ... | ... |

### Register payments

Payment table:
| IDPayment (Int autofield)(PK) | IDUserPaying (Int)(FK) | IDUserReceiving (Int)(FK) | Amount (Int) | AmountPerUser (Int) | Description (Varchar) | Date (Date) | Category (Varchar) |
|----|------|----|----|----|----|----|----|
| 1 | 1 | 2 | 20 |  | Pizza | 2020-01-01 | Food |
| 2 | 3 | 5 | 30 |  | Beer | 2020-01-02 | Drinks |
| 3 | ... | ... |  | ... | ... | ... | ... |

UserReceiving table:
| IDUserReceiving (Int autofield)(PK) | IDUser (Int)(FK) | IDPayment (Int)(FK) |
|----|------|----|
| 2 | 2 | 1 |
| 5 | 5 | 2 |
| ... | ... | ... |

### Calculate individual debt for each payment

```python
def calculate_amount_per_user():
    """
    Does a query to the database to get the amount of the payment and the amount of users receiving it
    Calculates the amount per user (amount / amount of users receiving)
    Updates the database with the amount per user
    """
    pass
```

### Calculate the balance of each user

```python
def calculate_balance():
    """
    Does a query to the database to get the amount per user for each payment
    Calculates the total debt for each user by summing all the AmountPerUser it appears in the database
    Calculates the total contribution for each user by summing all the payments made by each user
    Calculates the balance for each user (total contribution - total debt)
    Updates the database with the balance for each user
    """
    pass
```

### Calculate the minimum amount of transactions to pay all debts

```python
def calculate_minimum_transactions():
    """
    Does a query to the database to get the balance for each user
    Calculates the minimum amount of transactions to pay all debts
    """
    pass
```

### Display the results

```python
def display_results():
    """
    Does a query to the database to get the balance for each user
    Displays the results in a table
    """
    pass
```

## First prototype (MVP)

The first prototype will be a python script that reads a csv file with the records of the payments and calculates the balance of each user.
The csv file will be the *input* and will have the following columns (in this order):
| UserPaying | UsersReceiving | Amount | Description | Date | Category |
|----|------|----|----|----|----|
| ... | ... | ... | ... | ... | ... |

The program will have two *outputs*
The script will calculate the balance of each user and display it in a table.
| User | TotalContribution | TotalDebt | Balance |
|----|------|----|----|
| ... | ... | ... | ... |

Then it will display the transactions needed to pay all debts.
| UserPaying | UserReceiving | Amount |
|----|------|----|
| ... | ... | ... |

For the first prototype instead of using a database, the program will use OOP to store the data in classes' attributes.

The program will have the following classes:
- User:
    - Name (str)
    - Balance (float)
    - TotalContribution (float)
    - TotalDebt (float)
- Group:
    - Name (str)
    - Users (list of User objects)
    - Payments (list of Payment objects)
- Payment:
    - UserPaying (User object)
    - UsersReceiving (list of User objects)
    - Amount (float)
    - Description (str)
    - Date (date)
    - Category (str)

The Group class will have the following methods:
- calculate_amount_per_user
- calculate_balance
- calculate_minimum_transactions
- display_results

Note: the user appending will be done when the csv file is read and the user is created, as well as the payment appending that will be done at the same time the payment is created.

## Second prototype

The second prototype will be a Django web app that will have the same functionalities as the first prototype but with a database instead of OOP. For this second prototype the front end will not be extremely important, just enough to be able to use the app. 

The database will be SQLite, Django ORM will be used to interact with the database and the front end will be done with Django templates. 

The input still will be a csv file. And the output will be the same as the first prototype, a table with the balance of each user and a table with the transactions needed to pay all debts, but this time the tables will be displayed in the web app.

The web app will have the following pages:
- Home page (with a button to upload the csv file that fills the database)
- Dashboard (with the tables with the results)

## Third prototype

The third prototype will be a Django web app that will have the same functionalities as the second prototype but with a front end that is more user friendly.

Probably the database will be changed to one hosted in the cloud (probably PostgreSQL) and the front end will be done in Django templates.

The input will be a form that will be filled with the data of one payment. And the output will be the same as the second prototype, a table with the balance of each user and a table with the transactions needed to pay all debts, now with a more user friendly front end.

The web app will have the following pages:
- Home page
- Register (with a form to register a payment that fills the database)
- Dashboard (with the tables with the results)