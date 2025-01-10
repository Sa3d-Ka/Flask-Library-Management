from flask import Flask, request, url_for, render_template, redirect, flash
import random
from datetime import datetime
import secrets

app = Flask(__name__)

# Generate a secret key if not already set
if not app.secret_key:
    app.secret_key = secrets.token_hex(16)

books = {}
users = {}

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

@app.route("/")
def Home():
    return render_template('index.html',
           title='Home',
           css='index',
           books=books)

@app.route("/recherche")
def Recherche():
    query = request.args.get('query', '').lower()
    category = request.args.get('category', '')

    filtered_books = {}
    for isbn, book in books.items():
        # Check if the book matches the search query (title, author, or ISBN)
        matches_query = (
            query in book['titre'].lower() or
            query in book['author'].lower() or
            query in isbn.lower()
        )

        # Check if the book matches the selected category
        matches_category = (not category) or (book['category'] == category)

        if matches_query and matches_category:
            filtered_books[isbn] = book

    return render_template('Recherche/recherche.html',
           title='Recherche',
           css='Recherche/recherche',
           books=filtered_books)

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

    for isbn, book in books.items():
            if book['titre'].lower() == title.lower():
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
            'quantite': quantite
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
    return render_template('Statiques/statiques.html',
           title='Statiques',
           css='Statiques/statiques',
           books=books)

if __name__ == '__main__':
    app.run(debug=True)