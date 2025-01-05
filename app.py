from flask import Flask, request, url_for, render_template

app = Flask(__name__)

@app.route("/")
def Home():
    return render_template('index.html',
           title='Home',
           css='index')

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