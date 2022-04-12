## ADD ABILITY TO OVERWRITE A LINE IF THE PLANT LOCATION IS DUPLICATE
## ADD REMOVE FUNCTION 
## ADD WARNING IF NOT 22ML INCREMENT
## TWEAK READ DATA FUNCTION TO ONLY RENDER ONCE AND NOT EVERYTIME
## OR WE TAKE IN DATA AND DO INT DIVISION BY 22 AKA SECONDS IT TURNS ON

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
    messageList = []

    with open('OUTPUT.csv', 'r') as f:
        Lines = f.readlines()
        for line in Lines:
            # Take out all of the new lines
            line = line.strip()
            if line != '':
                print("LINE", line)
                # split the file by the commas
                line = line.split(',')
                title = line[0]
                amount = line[1]
                location = line[2]
                tempPlantInfo = f"WATERED: {amount} mL EVERY: 3 Hours LOCATION: {location}"
                tempMessage = {'title': title, 'content': tempPlantInfo}
                messageList.append(tempMessage)
            # else, do nothing
    f.close()
    return messageList

@app.route('/')
def index():
    messageList = read_data()
    print(messageList)
    return render_template('index.html', messages=messageList)

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
            
            # Convert plantLocation to an int
            plantLocation = int(plantLocation)
            print('plantLocation: ', plantLocation)

            with open('OUTPUT.csv', 'r') as f:
                Lines = f.readlines()
                plantLocation -= 1
                Lines[plantLocation] = plantCSV
                f.close()
            
            with open('OUTPUT.csv', 'w') as f:
                f.writelines(Lines)
                f.close()
                            
            return redirect(url_for('index'))
    return render_template('create.html')  

if __name__ == "__main__":
    app.debug=True
    app.run(host="0.0.0.0", port=5000)
