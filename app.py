from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about-evan')
def about():
    return render_template('about.html')


@app.route('/lessons')
def lessons():
    return render_template('lessons.html')


if __name__ == '__main__':
    app.run()
