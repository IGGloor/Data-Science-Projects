# Import module
import sqlite3
# Create a db file if doesn't exist
db = sqlite3.connect("ebookstore.db")
# Create cursor object to be used in different methods
cursor = db.cursor()

# Create book table if it doesn't exist
def create_book_db():
    # Execute SQL command to create table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS book (
        id INTEGER PRIMARY KEY,
        title TEXT,
        authorID INTEGER,
        qty INTEGER
    )
    ''')
    # Commit changes to db
    db.commit()

# Populate book table if empty
def populate_book_db():
    # Check if table is empty
    cursor.execute('''SELECT COUNT(*) FROM book''')
    count = cursor.fetchone()[0]
    if count == 0:
        try:
            # Insert data into the table
            books = [(3001, "A Tale of Two Cities", 1290, 30), 
                (3002, "Harry Potter and the Philosopher's Stone", 8937, 40), 
                (3003, "The Lion, the Witch and the Wardrobe", 2356, 25),
                (3004, "The Lord of the Rings", 6380, 37),
                (3005, "Alice's Adventures in Wonderland", 5620, 12)]
            cursor.executemany(
            '''INSERT INTO book(id, title, authorID, qty) VALUES(?, ?, ?, ?)''', books
            )
            db.commit()
        except ValueError:
            print("Database is already populated with books.")

# Create author table if it doesn't exist
def create_author_db():
    #Execute SQL command to create table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS author (
        id INTEGER PRIMARY KEY,
        name TEXT,
        country TEXT
    )
    ''')
    # Commit changes to db
    db.commit()

# Populate author table if empty
def populate_author_db():
    # Check if table is empty
    cursor.execute('''SELECT COUNT(*) FROM author''')
    count = cursor.fetchone()[0]
    if count == 0:
        try:
            # Insert data into the table
            authors = [(1290, "Charles Dickens", "England"), 
                (8937, "J.K. Rowling", "England"), 
                (2356, "C.S. Lewis", "Ireland"),
                (6380, "J.R.R. Tolkien", "South Africa"),
                (5620, "Lewis Carroll", "England")]
            cursor.executemany(
            '''INSERT INTO author(id, name, country) VALUES(?, ?, ?)''', authors
            )
            db.commit()
        except ValueError:
            print("Database is already populated with authors.")

# Get all valid book ids
def get_bookIds():
    cursor.execute('''SELECT id FROM book''')
    return [str(row[0]) for row in cursor.fetchall()]

# Get all valid author names
def get_authors():
    cursor.execute('''SELECT name FROM author''')
    authors = cursor.fetchall()
    return authors

# Update book quantity
def update_qty(bookID):
    while True:
        try:
            new_qty = int(input("What would you like to update the new quantity to? "))
            try:
                cursor.execute(f'''UPDATE book SET qty = {new_qty} WHERE id = {bookID} ''')
                db.commit()
                print(f"\nSuccessfully updated the quantity to {new_qty} for bookID {bookID}\n")
                break
            except ValueError:
                print("\nUnable to update the database.\n")
                break
        except ValueError:
            print("\nInvalid quantity. Please try again.\n")

# Add new book to database
def add_book(title, authorID, quantity):
    try:
        cursor.execute(f'''INSERT INTO book(title, authorID, qty) VALUES(?, ?, ?)''', (title, authorID, quantity))
        db.commit()
        print("\nNew book added to database!\n")
    except ValueError:
        print("\nUnable to save book to database.\n")

# Update author name in database
def update_name(authorID):
    author_names = get_authors()
    while True:
        try:
            new_name = input("What is the updated name? ")
            # Ensure new name is unique and not in use already
            if new_name in author_names:
                print("\nAuthor name already in use.\n")
            else:
                cursor.execute(f'''UPDATE author SET name = '{new_name}' WHERE id = {authorID}''')
                db.commit()
                break
        except ValueError:
            print("Unable to update author name.")

# Update author country in database
def update_country(authorID):
    try:
        new_country = input("What is the updated country? ")
        cursor.execute(f'''UPDATE author SET country = '{new_country}' WHERE id = {authorID}''')
        db.commit()
    except ValueError:
        print("Unable to update author country.")

# Select what author details to update
def update_author_db(bookID):
    try:
        # Get authorID and details
        cursor.execute(f'''SELECT authorID FROM book WHERE id = {bookID}''')
        authorID = cursor.fetchone()[0]
        cursor.execute(f'''SELECT name FROM author WHERE id = {authorID}''')
        name = cursor.fetchone()[0]
        cursor.execute(f'''SELECT country FROM author WHERE id = {authorID}''')
        country = cursor.fetchone()[0]
        while True:
            menu = input(f'''You want to update the author {name} from {country}. Select an update option:
1 - Update name
2 - Update country
3 - Update name and country
4 - Cancel
: ''')
            if menu == '1':
                update_name(authorID)
                break
            elif menu == '2':
                update_country(authorID)
                break
            elif menu == '3':
                update_name(authorID)
                update_country(authorID)
                break
            elif menu == '4':
                break
            else:
                print("\nInvalid selection. Please try again.\n")
    except ValueError:
        print("Unable to retrieve author details")

# Delete book from db
def delete_book(bookID):
    try:
        cursor.execute(f'''DELETE FROM book WHERE id = {bookID}''')
    except ValueError:
        print(f"\nUnable to delete book with id: {bookID}\n")

while True:
    # Ensure databases are created and populated with data
    create_book_db()
    populate_book_db()
    create_author_db()
    populate_author_db()

    # Get user input
    menu = input(
        '''Select one of the following options:
1 - Enter book
2 - Update book
3 - Delete book
4 - Search books
5 - View details of all books
0 - Exit
: '''
    ).lower()
        
    if menu == '1':
        print("\nEnter details for a new book:\n")
        # Get all authors names
        authors = get_authors()
        while True:
            try:
                title = input("Title: ")
                quantity = int(input("Quantity: "))
                author = input("Author: ")
                if author in authors:
                    # Get existing author's authorID
                    cursor.execute(f'''SELECT id FROM author WHERE name = {author}''')
                    authorID = cursor.fetchone()
                    # Call add book to db method
                    add_book(title, authorID, quantity)
                    break
                else:
                    author_country = input("Author country of origin: ")
                    # Create new author
                    try:
                        cursor.execute(f'''INSERT INTO author(name, country) VALUES(?, ? )''', (author, author_country))
                        db.commit()
                        # Get new authorID
                        cursor.execute(f'''SELECT id FROM author WHERE name = '{author}' ''')
                        authorID = cursor.fetchone()[0]
                        print("\nNew author added to the database!\n")
                        # Call add to db method
                        add_book(title, authorID, quantity)
                        break
                    except ValueError:
                        print("\nUnable to save new author in the database.\n")
                        break
                    break
            except ValueError:
                print("Ensure quantity is an integer.")

    elif menu == '2':
        # Get all book ids:
        books = get_bookIds()
        print("\nUpdate a book:\n")
        while True:
            bookID = input("Enter the bookID: ")
            # Check if book id is in the list of existing ids
            if bookID in books:
                while True:
                    update_type = input("Do you want to update 'quantity' or 'author'? ").lower()
                    if update_type == 'quantity':
                        update_qty(bookID)
                        break
                    elif update_type == 'author':
                        update_author_db(bookID)
                        break
                    else:
                        print("\nInvalid selection. Please try again.\n")
                break
            else:
                print("\nInvalid bookID. Please try again.\n")

    elif menu == '3':
        # Get all book ids:
        books = get_bookIds()
        print("\nDelete a book:\n")
        while True:
            bookID = input("Enter the bookID: ")
            # Check if book id is in the list of existing ids
            if bookID in books:
                # Get name from db
                cursor.execute(f'''SELECT title FROM book WHERE id = {bookID}''')
                title = cursor.fetchone()[0]
                while True:
                    confirm = input(f"Are you sure you want to delete the book {title} (yes/no)? ").lower()
                    if confirm == 'yes':
                        delete_book(bookID)
                        print(f"\nThe book {title} was successfully deleted.\n")
                        break
                    elif confirm == 'no':
                        print("\nDeletion cancelled.\n")
                        break
                    else:
                        print("\nPlease confirm your choice.\n")
                break
            else:
                print("\nInvalid bookID. Please try again.\n")
        
    
    elif menu == '4':
        search = input("Search for a book title here: ")
        # Allow for partial matches
        keyword = f"%{search}%"
        # View all details for each book
        cursor.execute('''SELECT book.id, book.title, book.qty, author.name, author.country FROM book INNER JOIN author on book.authorID = author.id WHERE book.title LIKE ?''', (keyword,))
        search_results = cursor.fetchall()
        if search_results:
            print("\nAll books from search:\n")
            for result in search_results:
                bookID, title, qty, author, country = result
                print("----------------------------------------------------")
                print(f"Book ID: {bookID}")
                print(f"Title: {title}")
                print(f"Quantity: {qty}")
                print(f"Author: {author}")
                print(f"Country: {country}\n")
        else:
            print("\nNo results from your search.\n")
    
    elif menu == '5':
        # View all details for each book
        cursor.execute('''SELECT book.id, book.title, book.qty, author.name, author.country FROM book INNER JOIN author on book.authorID = author.id''')
        book_details = cursor.fetchall()
        if book_details:
            print("\nAll books in the database:\n")
            for book in book_details:
                bookID, title, qty, author, country = book
                print("----------------------------------------------------")
                print(f"Book ID: {bookID}")
                print(f"Title: {title}")
                print(f"Quantity: {qty}")
                print(f"Author: {author}")
                print(f"Country: {country}\n")
        else:
            print("\nNo books in the database.\n")

    elif menu == '0':
        print("\nGoodbye!\n") 
        break

    else:
        print("\nYou have entered an invalid input. Please try again.\n")