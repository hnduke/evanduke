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


@app.route('/business-consultations')
def business():
    return render_template('business.html')


@app.route('/performances')
def performances():
    return render_template('performances.html')


@app.route('/recordings')
def recordings():
    return render_template('recordings.html')


@app.route('/research-projects')
def research():
    return render_template('research.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run()
