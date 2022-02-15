from flask import Flask, request, render_template
from os import listdir
app = Flask(__name__)

@app.route('/')
def my_form():
   return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    input_nopol = request.form['text_box']
    if request.method == 'POST':
       with open('nopol.txt', 'a+') as f:
            f.write(str(input_nopol))
    return render_template('index.html', nopol=input_nopol)


if __name__ == '__main__':
    app.debug = True
    app.run()