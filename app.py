from flask import Flask, request, url_for, render_template, redirect, flash
import random
from datetime import datetime
import secrets

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

books = {}
users = {}
emprunts = {}
emprunts_time = {}



def generate_isbn13():
    prefix = random.choice(["978", "979"])
    registration_group = str(random.randint(0, 9))
    registrant = str(random.randint(100, 9999))
    publication = str(random.randint(100, 99999))
    isbn_without_check = prefix + registration_group + registrant + publication
    check_digit = calculate_check_digit(isbn_without_check)
    return isbn_without_check + str(check_digit)

def calculate_check_digit(isbn_without_check):
    total = 0
    for i, digit in enumerate(isbn_without_check):
        total += int(digit) if i % 2 == 0 else 3 * int(digit)
    remainder = total % 10
    return 0 if remainder == 0 else 10 - remainder

# Function to calculate new users this month
def get_new_users_this_month(users):
    current_month = datetime.now().month  # Get the current month (1-12)
    current_year = datetime.now().year    # Get the current year

    new_users_this_month = 0

    for user_id, user in users.items():
        registration_date = datetime.strptime(user['registration_date'], "%Y-%m-%d")
        if registration_date.month == current_month and registration_date.year == current_year:
            new_users_this_month += 1

    return new_users_this_month

def get_new_emprunts_this_month(emprunts):
    # Get the current month and year
    current_month = datetime.now().month  # Current month (1-12)
    current_year = datetime.now().year    # Current year

    # Initialize a counter for borrowings this month
    new_emprunts_this_month = 0

    # Iterate through the emprunts dictionary
    for emprunt_id, emprunt in emprunts.items():
        try:
            # Parse the borrowed_date string into a datetime object
            borrowed_date = datetime.strptime(emprunt['borrowed_date'], "%Y-%m-%d %H:%M:%S")
            
            # Check if the borrowing was made in the current month and year
            if borrowed_date.month == current_month and borrowed_date.year == current_year:
                new_emprunts_this_month += 1
        except (KeyError, ValueError):
            # Skip invalid or missing dates
            continue

    return new_emprunts_this_month

def calculate_delay(emprunts):
    delay_time = 0  # Counter for overdue borrowings

    # Iterate through the emprunts dictionary
    for transaction_id, details in emprunts.items():
        try:
            # Parse the due_date string into a datetime object
            due_date = datetime.strptime(details['due_date'], "%Y-%m-%d")
            # Get the current date
            current_date = datetime.now()
            # Calculate the delay in days
            delay = (current_date - due_date).days
            # If the delay is positive, the book is overdue
            if delay > 0:
                delay_time += 1
        except (KeyError, ValueError):
            # Skip invalid or missing due dates
            continue

    return delay_time


@app.route("/")
def Home():
    return render_template('index.html',
           title='Home',
           css='index',
           books=books,
           users=users,
           emprunts=emprunts)

@app.route("/borrow_book", methods=["POST"])
def borrow_book():
    isbn = request.form.get("isbn")
    due_date = request.form.get("dueDate")
    user_id = request.form.get("userId")

    if not isbn or not due_date or not user_id:
        flash("Invalid request. Please provide ISBN, due date, and user ID.", "danger")
        return redirect(url_for("Recherche"))

    if isbn not in books:
        flash("Book not found.", "danger")
        return redirect(url_for("Recherche"))

    if user_id not in users:
        flash("User not found.", "danger")
        return redirect(url_for("Recherche"))

    if books[isbn]["quantite"] <= 0:
        flash("This book is currently on loan.", "danger")
        return redirect(url_for("Recherche"))

    # Decrease the book quantity
    books[isbn]["quantite"] -= 1

    # Create a unique transaction ID (e.g., using a timestamp)
    transaction_id = f"{user_id}_{isbn}_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    # Save the borrowing details in the emprunts dictionary
    emprunts[transaction_id] = {
        "isbn": isbn,
        "user_id": user_id,
        "due_date": due_date,
        "borrowed_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "book_title": books[isbn]["titre"],
        "user_name": users[user_id]["fullname"]
    }
    
    book_title = books[isbn]["titre"]
    if book_title in emprunts_time:
        emprunts_time[book_title] += 1
    else:
        emprunts_time[book_title] = 1

    flash(f"Book '{books[isbn]['titre']}' borrowed successfully by User {users[user_id]['fullname']}. Due Date: {due_date}", "success")
    return redirect(url_for("Recherche"))

@app.route("/recherche")
def Recherche():
    query = request.args.get('query', '').lower()
    category = request.args.get('category', '')

    filtered_books = {}
    for isbn, book in books.items():
        matches_query = (
            query in book['titre'].lower() or
            query in book['author'].lower() or
            query in isbn.lower()
        )
        matches_category = (not category) or (book.get('category') == category)

        if matches_query and matches_category:
            filtered_books[isbn] = book

    return render_template('Recherche/recherche.html',
           title='Recherche',
           css='Recherche/recherche',
           books=filtered_books,
           users=users,  # Pass the users dictionary to the template
           js='Recherche/recherche')

@app.route("/livres")
def livres():
    return render_template('Livres/livres.html',
           title='Livres',
           css='Livres/livres',
           js='Livres/livres',
           books=books)

@app.route('/ajouter_livre', methods=['POST'])
def add_book():
    title = request.form.get('title')
    author = request.form.get('author')
    category = request.form.get('category')
    quantite = request.form.get('quantite')
    url = request.form.get('url')

    # Check if the book already exists
    for isbn, book in books.items():
        if book['titre'].lower() == title.lower():
            flash("A book with this title already exists.", "danger")
            return redirect(url_for('livres'))

    # Generate a new ISBN
    isbn = generate_isbn13()

    # Add the new book to the dictionary
    books[isbn] = {
        'titre': title,
        'author': author,
        'category': category,
        'quantite': int(quantite),
        'url': url
    }

    flash(f"Book '{title}' added successfully!", "success")
    return redirect(url_for('livres'))

@app.route('/modifier_livre', methods=['POST'])
def edit_book():
    # Get form data
    isbn = request.form.get('isbn')
    titre = request.form.get('titre')
    author = request.form.get('author')
    category = request.form.get('category')
    url = request.form.get('url')
    quantite = request.form.get('quantite')

    # Update the book in the dictionary
    if isbn in books:
        books[isbn] = {
            'titre': titre,
            'author': author,
            'category': category,
            'url': url,
            'quantite': int(quantite)
        }

    # Redirect to the livres page
    return redirect(url_for('livres'))

@app.route('/supprimer_livre/<isbn>', methods=['DELETE'])
def delete_book(isbn):
    # Remove the book from the dictionary
    if isbn in books:
        del books[isbn]

    # Redirect to the livres page
    return redirect(url_for('livres'))


@app.route("/emprunts")
def Emprunts():
    x = datetime.now()
    formatted_date = x.strftime("%Y/%m/%d %H:%M")
    return render_template(
        'Emprunts/emprunts.html',
        title='Emprunts',
        css='Emprunts/emprunts',
        js='Emprunts/emprunts',
        formatted_date=formatted_date,
        emprunts=emprunts,
        books=books
    )

@app.route("/return_book", methods=["POST"])
def return_book():
    # Get the transaction_id from the form
    transaction_id = request.form.get("transaction_id")

    # Check if the transaction_id exists in the emprunts dictionary
    if transaction_id not in emprunts:
        flash("Invalid transaction ID.", "danger")
        return redirect(url_for("Emprunts"))

    # Get the borrowing details
    borrowing_details = emprunts[transaction_id]
    isbn = borrowing_details["isbn"]

    # Increase the book quantity in the books dictionary
    if isbn in books:
        books[isbn]["quantite"] += 1
    else:
        flash("Book not found in the library.", "danger")
        return redirect(url_for("Emprunts"))

    # Remove the borrowing record from the emprunts dictionary
    del emprunts[transaction_id]

    # Flash a success message
    flash(f"Book '{borrowing_details['book_title']}' returned successfully.", "success")

    # Redirect to the Emprunts page
    return redirect(url_for("Emprunts"))

@app.route("/utilisateurs")
def Utilisateur():
    new_users_this_month = get_new_users_this_month(users)
    return render_template(
        'Utilisateurs/utilisateur.html',
        title='Utilisateurs',
        css='Utilisateurs/utilisateur',
        js='Utilisateurs/utilisateur',
        users=users,
        new_users_this_month=new_users_this_month
    )

# Route to add a new user
@app.route("/ajouter_utilisateur", methods=["POST"])
def ajouter_utilisateur():
    fullname = request.form.get("fullname")
    email = request.form.get("email")

    for id, info in users.items():
            if info['email'].lower() == email.lower():
                return redirect(url_for('utilisateurs'))
    # Generate a new user ID (replace with a proper ID generator in production)
    new_user_id = f"{fullname[:2] + str(random.randint(10,99))}"

    # Add the new user to the dictionary
    users[new_user_id] = {
        "fullname": fullname,
        "email": email,
        "registration_date": datetime.now().strftime("%Y-%m-%d")  # Add current date
    }

    # Redirect to the user management page
    return redirect(url_for("Utilisateur"))

# Route to edit an existing user
@app.route("/modifier_utilisateur", methods=["POST"])
def modifier_utilisateur():
    user_id = request.form.get("user_id")
    fullname = request.form.get("fullname")
    email = request.form.get("email")

    # Update the user's details
    if user_id in users:
        users[user_id]["fullname"] = fullname
        users[user_id]["email"] = email

    # Redirect to the user management page
    return redirect(url_for("Utilisateur"))

# Route to delete a user
@app.route("/supprimer_utilisateur/<user_id>", methods=["DELETE"])
def supprimer_utilisateur(user_id):
    if user_id in users:
        del users[user_id]

    # Return a success response
    return redirect(url_for("Utilisateur"))

@app.route("/statiques")
def Statiques():
    new_emprunts_this_month = get_new_emprunts_this_month(emprunts)
    delay_time = calculate_delay(emprunts)
    sorted_emprunts_time = dict(sorted(emprunts_time.items(), key=lambda item: item[1], reverse=True))
    return render_template('Statiques/statiques.html',
           title='Statiques',
           css='Statiques/statiques',
           books=books,
           emprunts=emprunts,
           sorted_emprunts_time=sorted_emprunts_time,
           new_emprunts_this_month=new_emprunts_this_month,
           delay_time=delay_time)

if __name__ == '__main__':
    app.run(debug=True)