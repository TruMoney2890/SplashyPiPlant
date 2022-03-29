import json
from flask import Flask, render_template, request, url_for, flash, redirect
import urllib

app = Flask(__name__)

## ADD PLANT LOCATION, AS IN WHAT LINE IT IS AT
## ADD REMOVE FUNCTION 
## CHECKBOXES FOR mL AMOUNTS
## ADD ABILITY TO SELECT WHICH LINE THE PLANT IS AT AND DRAW A DIAGRAM 

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

@app.route('/create/', methods=('GET', 'POST'))
def create():

    if request.method == 'POST':
        title = request.form['title']
        # content = request.form['content']
        water_amount = request.form['water_amount']
        water_frequency = request.form['water_frequency']
        water_notes = request.form['water_notes']

        # Need to figure out the source of each piece of text, and put it in the output file
        #with open('OUTPUT.txt', 'w') as f:
         #   f.write(str(f'Title:{title}'))
          #  f.write(str(f'Content:{content}'))



        # url = 'http://127.0.0.1:5000/'
        # urllib.urlretrieve(url, fielname='webpage.html')

        # getting input with name = fname in HTML form
        titleForm = request.form.get("title")
        # getting input with name = lname in HTML form 
        contentForm = request.form.get("content") 

        plantInfo = 'WATERED: '+ water_amount+ ' mL EVERY: '+ water_frequency + ' hours' + '\n' + 'NOTES: ' + '\n' + water_notes

        if not title:
            flash('Title is required!')
        elif not water_amount:
            flash('Water amount is required!')
        else:
            messages.append({'title': title, 'content': plantInfo})

            # Need to figure out the source of each piece of text, and put it in the output file
            with open('OUTPUT.txt', 'w') as f:
                f.write(str(f'Title: {title}\n'))
                f.write(str(f' Water Amount: {water_amount}\n'))
                f.write(str(f' Water Frequency: {water_frequency}\n'))
                f.write(str(f' Notes: {water_notes}\n'))

            flash('Added ' + title + ': ' + plantInfo)
            #flash(water_amount)



            # # Need to figure out how to format text inside of a JSON file
            
            # # the file to be converted to 
            # # json format
            # filename = 'OUTPUT.txt'
            
            # # dictionary where the lines from
            # # text will be stored
            # dict1 = {}
            
            # # creating dictionary
            # with open(filename) as fh:
            
            #     for line in fh:
            #         print(line)
            
            #         # reads each line and trims of extra the spaces 
            #         # and gives only the valid words
            #         command, description = line.strip().split(None, 1)
            
            #         dict1[command] = description.strip()
            
            # # creating json file
            # # the JSON file is named as test1
            # out_file = open("test1.json", "w")
            # json.dump(dict1, out_file, indent = 4, sort_keys = False)
            # out_file.close()

            return redirect(url_for('index'))
    return render_template('create.html')  