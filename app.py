from flask import Flask, request, url_for, render_template

app = Flask(__name__)

@app.route("/")
def Home():
    return render_template('index.html',
           title='Home',
           css='index')

if __name__ == '__main__':
    app.run(debug=True)