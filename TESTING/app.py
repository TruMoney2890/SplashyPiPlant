## ADD ABILITY TO OVERWRITE A LINE IF THE PLANT LOCATION IS DUPLICATE
## ADD REMOVE FUNCTION 
## ADD WARNING IF NOT 22ML INCREMENT
## TWEAK READ DATA FUNCTION TO ONLY RENDER ONCE AND NOT EVERYTIME

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

def read_data():
    with open('OUTPUT.csv', 'r') as f:
        Lines = f.readlines()
        for line in Lines:
            # split the file by the commas
            line = line.split(',')
            title = line[0]
            amount = line[1]
            location = line[2]
            tempPlantInfo = f"WATERED: {amount} mL EVERY: 3 Hours LOCATION: {location}"
            tempMessage = {'title': title, 'content': tempPlantInfo}
            messages.append(tempMessage)

    f.close()
    return 0

@app.route('/')
def index():
    
    return render_template('index.html', messages=messages)


def main():
    return render_template('index.html')


@app.route('/create/', methods=('GET', 'POST'))
def create():

    if request.method == 'POST':
        title = request.form['title']
        plantLocation = request.form['plantLocation']
        water_amount = request.form['water_amount']
        water_notes = request.form['water_notes']
        
        plantInfo = f'WATERED: {water_amount} mL EVERY: 3 Hours' + '\n' + 'LOCATION: ' + plantLocation + '\n' + 'NOTES: ' + '\n' + water_notes

        plantCSV = f'{title}, {water_amount}, {plantLocation} \n'
        
        if not title:
            flash('Title is required!')
        elif not water_amount:
            flash('Water amount is required!')
        elif not plantLocation:
            flash('Plant location is required!')
        else:
            messages.append({'title': title, 'content': plantInfo})

            with open('OUTPUT.csv', 'a') as f:
                # Lines = f.readlines()
                # for line in Lines:
                #     # split the file by the commas
                #     line = line.split(',')
                #     title = line[0]
                #     amount = line[1]
                #     location = line[2]
                #     if location == plantLocation:
                #         # overwrite that line
                #         f.write(plantCSV)
                #         f.close()

                f.write(str(plantCSV))
            # Close the file
            f.close()

            flash(f'Added {title}: {plantInfo}')

            return redirect(url_for('index'))
    return render_template('create.html')  

if __name__ == "__main__":
    app.debug=True
    app.run(host="0.0.0.0", port=5000)
