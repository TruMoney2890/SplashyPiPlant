## ADD REMOVE FUNCTION 
## CHECKBOXES FOR mL AMOUNTS

import json
from flask import Flask, render_template, request, url_for, flash, redirect
import urllib

app = Flask(__name__)

app.config['SECRET_KEY'] = '15d95fea91abf12688dde77bf2ce14f98bd78533b71217e4'

messages = [{'title': 'Spring Cactus',
            'content': 'WATERED: 3 times a day'},
            {'title': 'Arabian Bonzai Tree',
            'content': 'WATERED: 2 times a day'}
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

plantArt = {
    "         __/)\ " + "\n" + 
    "        .-(__(=:" + "\n" +
    "        |    \)" + "\n" +
    "  (\__  | " + "\n" +
    " :=)__)-|  __/)" + "\n" +
    "  (/    |-(__(=:" + "\n" + 
    "______  |  _ \)" + "\n" +
    "/     \ | / \ " + "\n" +
    "    ___\|/___\ " + "\n" +
    "   [         ]\ " + "\n" +
    "    \       /  " + "\n" + 
    "     \     / " + "\n" + 
    "      \___/ "
    
}

@app.route('/create/', methods=('GET', 'POST'))
def create():

    if request.method == 'POST':
        title = request.form['title']
        plantLocation = request.form['plantLocation']
        water_amount = request.form['water_amount']
        water_notes = request.form['water_notes']

        # url = 'http://127.0.0.1:5000/'
        # urllib.urlretrieve(url, fielname='webpage.html')

        plantInfo = f'WATERED: {water_amount} mL EVERY: 3 Hours' + '\n' + 'LOCATION: ' + plantLocation + '\n' + 'NOTES: ' + '\n' + water_notes

        if not title:
            flash('Title is required!')
        elif not water_amount:
            flash('Water amount is required!')
        else:
            messages.append({'title': title, 'content': plantInfo})

            # Need to figure out the source of each piece of text, and put it in the output file
            with open('OUTPUT.txt', 'a') as f:
                f.write(str(f'{title}, {water_amount}, {plantLocation} \n'))
            # Close the file
            f.close()

            flash(f'Added {title}: {plantInfo}')
            #flash(water_amount)

            return redirect(url_for('index'))
    return render_template('create.html')  

if __name__ == "__main__":
    app.debug=True
    app.run(host="0.0.0.0", port=5000)
