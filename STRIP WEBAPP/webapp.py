# Author: Michael Bridgette
# Description: Flask backend for my GIP Object detection model.
# Date of last edit: 10/04/2019
from flask import Flask, render_template, request, session, jsonify

#import mysql.connector

import object_detector

app = Flask(__name__)

# Connect to mySql database (Note: FILL IN PASSWORD)
# mydb = mysql.connector.connect(
#   host="127.0.0.1",
#   user="root",
#   passwd="",
#   database="results"
# )

# Function that takes mySql records and
# appends them to a list of results
def create_list(records):
    listOfResults = []      # empty list
    for row in records:
        result = {
        'Id': row[0],
        'UserId': row[1],
        'Result': row[2],
        'Accuracy': row[3],
        'Photo': row[4].decode('UTF-8'),        # decode b64 string
        'UserResult': row[5],
        'Timestamp': row[6],
        'ModelVersion': row[7]
        }
        listOfResults.append(result)        # put into the list
    return listOfResults

####################################################################################################################################################################################

# Rest API routes

# This will send JSON containing the last entries in the database. The amount
# of entries will be based on <int:limit>.
@app.route('/get_history/<int:limit>', methods=['GET'])
def get_history(limit):
    # cursor = mydb.cursor()
    # sql_query = "SELECT * FROM strip ORDER BY ts DESC LIMIT %s" # sql query
    # cursor.execute(sql_query, (limit,))
    # records = cursor.fetchall()
    #
    # listOfResults = create_list(records)
    #
    # cursor.close()
    listOfResults = []
    return jsonify(results = listOfResults), 201

# This will return JSON for particular entry based on <int:result_id>
@app.route('/get_result/<int:result_id>', methods=['GET'])
def get_result(result_id):
    # cursor = mydb.cursor()
    # sql_query = "SELECT * FROM strip WHERE id = %s" # sql_query
    # cursor.execute(sql_query, (result_id,))
    # records = cursor.fetchall()
    #
    # listOfResults = create_list(records)
    #
    # cursor.close()
    listOfResults = []
    return jsonify(results = listOfResults), 201

# This will return JSON with all entries for a particular user based on <string:user_name>
@app.route('/get_user_results/<string:user_name>', methods=['GET'])
def get_user_results(user_name):
    # cursor = mydb.cursor()
    # sql_query = "SELECT * FROM strip WHERE userId = %s" #sql query
    # cursor.execute(sql_query, (user_name,))
    # records = cursor.fetchall()
    #
    # listOfResults = create_list(records)
    #
    # cursor.close()
    listOfResults = []
    return jsonify(results = listOfResults), 201


# Returns JSON containing Base64 string of the result image and also the accuracy as text
@app.route('/object_detection', methods=['POST'])
def detect_object():
    if not request.json or not 'image' in request.json:
        abort(400)

    # remove the first 23 characters from the string this is necessary
    # because these characters have to be removed in order for the object detection to work
    file = request.json["image"]
    for x in range(23):
        file = file[1:]

    result = object_detector.object_detection(file.encode())     # perform the actual object detection on the image
    result['image'] = "data:image/jpeg;base64," + result['image']       # add this string to beginning of the b64 string
    result['accuracy'] = int(result['accuracy'] * 100)      # result is between 0-1, Im converting it to a percentage for readability and consistency with the image

    return jsonify(results = result), 201

# Adds new entry to database and returns what was added to the database as JSON
@app.route('/add_entry/<string:user_name>/<string:user_result>', methods=['POST'])
def addEntry(user_name, user_result):
    if not request.json or not 'image' in request.json:
        abort(400)

    # remove the first 23 characters from the string this is necessary
    # because these characters have to be removed in order for the object detection to work
    file = request.json["image"]
    for x in range(23):
        file = file[1:]


    result = object_detector.object_detection(file.encode())     # perform the actual object detection on the image
    result['image'] = "data:image/jpeg;base64," + result['image']       # add this string to beginning of the b64 string
    result['accuracy'] = int(result['accuracy'] * 100)      # result is between 0-1, Im converting it to a percentage for readability and consistency with the image

    # cursor = mydb.cursor()
    #
    # sql = "INSERT INTO strip (userId,result,accuracy,photo,userResult) VALUES (%s, %s, %s ,%s ,%s)" # sql query
    # val = (user_name, result['name'][0].lower(), result['accuracy'], result['image'], user_result[0].lower())
    #
    # cursor.execute(sql, val)
    # mydb.commit() # commit change to the database

    return jsonify(results = result), 201

####################################################################################################################################################################################

# Demo Webapp routes

# Home page for demo web application.
@app.route('/home')
def get_and_display_form():
    return render_template('index.html',
                           the_title="GIP Strip Result Detection", )

# Results page of the demo web application
@app.route('/results', methods=['POST'])
def process_form():
    session['file'] = request.form["answer"]        # get the image from the form
    session['userName'] = request.form["Username"]      # get the username from the form
    session['userResult'] = request.form["UserResult"]      # get the users result from the form

    # remove the first 23 characters from the string this is necessary
    # because these characters have to be removed in order for the object detection to work
    for x in range(23):
        session['file'] = session['file'][1:]


    result = object_detector.object_detection(session['file'].encode())      # perform the actual object detection on the image
    result['image'] = "data:image/jpeg;base64," + result['image']       # add this string to beginning of the b64 string
    result['accuracy'] = int(result['accuracy'] * 100)      # result is between 0-1, Im converting it to a percentage for readability and consistency with the image

    # cursor = mydb.cursor()
    #
    # sql = "INSERT INTO strip (userId,result,accuracy,photo,userResult) VALUES (%s, %s, %s ,%s ,%s)" # sql query
    # val = (session['userName'], result['name'][0].lower(), result['accuracy'], result['image'], session['userResult'][0].lower())
    #
    # cursor.execute(sql, val)
    # mydb.commit() # commit change to the database
    return render_template('process.html',
                           the_title="Process Results", the_result = result['image'], the_name = result['name'], the_accuracy = result['accuracy'] )

if __name__ == '__main__':
    app.secret_key = "rkngfdbsakvbfkhjfnsakbvfknkblkfldsanvbkrjlrwewhcnkgkr"
    app.run(host='0.0.0.0', port=5000, debug=True)
