# Library Management System

## Overview

The Library Management System is a Flask-based web application designed to manage books, users, and borrowing transactions. It allows users to search for books, borrow books, return books, and view popular books based on the number of borrowings.

## Features

- **Book Management**: Add, update, and delete books with details such as title, author, ISBN, and quantity.
- **User Management**: Add, update, and delete users with details such as full name and user ID.
- **Borrowing Transactions**: Track book borrowings with details such as due date, borrowed date, and user information.
- **Popular Books**: Display a list of popular books sorted by the number of borrowings.
- **Search Functionality**: Search for books by title, author, or ISBN.

## Screenshots

### Homepage
![Homepage](https://res.cloudinary.com/du0x9ut5o/image/upload/v1736681090/v0wwp0arscdn6oc6audd.png)

### Add Book
![Add Book](https://res.cloudinary.com/du0x9ut5o/image/upload/v1736681090/c8uyyrtxvl8j0ijme9eo.png)

### Add Users
![Borrow Book](https://res.cloudinary.com/du0x9ut5o/image/upload/v1736681091/dtrndkvdxa5ciyzxsahc.png)

### Return Book
![Return Book](https://res.cloudinary.com/du0x9ut5o/image/upload/v1736681090/fszcxnbstgwaw5rbtvdd.png)

### Popular Books
![Popular Books](https://res.cloudinary.com/du0x9ut5o/image/upload/v1736681091/irc7sntxv2ixkqefiajb.png)

### Search Functionality
![Search Functionality](https://res.cloudinary.com/du0x9ut5o/image/upload/v1736681098/mmtqu6mnoicoby0kibg0.png)

## Installation

### Prerequisites

- Python 3.x
- Flask
- Bootstrap (for frontend styling)

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Sa3d-Ka/Flask-Library-Management.git
   cd Flask-Library-Management
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   flask run
   ```

5. **Access the Application**:
   Open your web browser and go to `http://127.0.0.1:5000`.

## Usage

### Adding Books

1. Navigate to the "Add Book" page.
2. Fill in the book details (title, author, ISBN, quantity).
3. Submit the form to add the book to the library.

### Borrowing Books

1. Search for a book using the search functionality.
2. Click the "Borrow" button next to the desired book.
3. Select a user and specify the due date.
4. Confirm the borrowing transaction.

### Returning Books

1. Navigate to the "Active Emprunts" page.
2. Click the "Return Book" button next to the borrowing transaction.
3. Confirm the return to update the book quantity and borrowing records.

### Viewing Popular Books

1. Navigate to the "Popular Books" page.
2. View the list of books sorted by the number of borrowings.

## Dependencies

- Flask
- Bootstrap (for frontend styling)

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeatureName`).
5. Open a pull request.

