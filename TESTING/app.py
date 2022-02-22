from flask import Flask, render_template, request, url_for, flash, redirect
import urllib

app = Flask(__name__)


app.config['SECRET_KEY'] = '15d95fea91abf12688dde77bf2ce14f98bd78533b71217e4'

messages = [{'title': 'Spring Cactus',
             'content': 'Watered 3 times a day'},
            {'title': 'Arabian Bonzai Tree',
             'content': 'Watered 2 times a day'}
            ]

@app.route('/')
def index():
    return render_template('index.html', messages=messages)

@app.route('/', methods=['POST'])
def my_form_post():
    input_nopol = request.form['title']
    #input_nopol2 = request.form['content']
    if request.method == 'POST':
       with open('OUTPUT.txt', 'w') as f:
            f.write(str(input_nopol))
    return render_template('create.html', nopol=input_nopol)

def main():
    return render_template('index.html')


@app.route('/create/', methods=('GET', 'POST'))
def create():

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        # Need to figure out the source of each piece of text, and put it in the output file
        with open('OUTPUT.txt', 'w') as f:
            f.write(str(f'Title:{title}'))
            f.write(str(f'Content:{content}'))



        # url = 'http://127.0.0.1:5000/'
        # urllib.urlretrieve(url, fielname='webpage.html')

        # getting input with name = fname in HTML form
        titleForm = request.form.get("title")
        # getting input with name = lname in HTML form 
        contentForm = request.form.get("content") 

        flash(titleForm)
        flash(contentForm)

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            messages.append({'title': title, 'content': content})

            flash(title)
            flash(content)

            return redirect(url_for('index'))
    return render_template('create.html')  