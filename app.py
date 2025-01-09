from flask import Flask, request, url_for, render_template, redirect
import random

app = Flask(__name__)

books = {}

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

@app.route("/")
def Home():
    return render_template('index.html',
           title='Home',
           css='index',
           books=books)

@app.route("/recherche")
def Recherche():
    return render_template('Recherche/recherche.html',
           title='Recherche',
           css='Recherche/recherche')

@app.route("/livres")
def livres():
    return render_template('Livres/livres.html',
           title='Livres',
           css='Livres/livres',
           books=books)

@app.route('/ajouter_livre', methods=['POST'])
def add_book():
    title = request.form.get('title')
    author = request.form.get('author')
    category = request.form.get('category')
    status = request.form.get('status')
    url = request.form.get('url')
    isbn = generate_isbn13()

    # Add the new book to the dictionary
    books[isbn] = {
        'titre': title,
        'author': author,
        'category': category,
        'status': status,
        'url': url
    }

    # Redirect to the livres page
    return redirect(url_for('livres'))

@app.route('/modifier_livre', methods=['POST'])
def edit_book():
    # Get form data
    isbn = request.form.get('isbn')
    titre = request.form.get('titre')
    author = request.form.get('author')
    category = request.form.get('category')
    url = request.form.get('url')
    status = request.form.get('status')

    # Update the book in the dictionary
    if isbn in books:
        books[isbn] = {
            'titre': titre,
            'author': author,
            'category': category,
            'url': url,
            'status': status
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
    return render_template('Utilisateurs/utilisateur.html',
           title='Utilisateurs',
           css='Utilisateurs/utilisateur')

@app.route("/statiques")
def Statiques():
    return render_template('Statiques/statiques.html',
           title='Statiques',
           css='Statiques/statiques')

if __name__ == '__main__':
    app.run(debug=True)