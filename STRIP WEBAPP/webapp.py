from flask import Flask, render_template, request, session, jsonify
import objectDetector
import mysql.connector

app = Flask(__name__)


mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  passwd="pizza123",
  database="results"
)


@app.route('/getform')
def get_and_display_form():
    return render_template('index.html',
                           the_title="GIP Strip Result Detection", )



@app.route('/getHistory', methods=['GET'])
def get_history():
    cursor = mydb.cursor()
    sql_select_Query = "select * from strip"
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()

    listOfResults = []

    for row in records:
        result = {
        'id': row[0],
        'userId': row[1],
        'result': row[2],
        'accuracy': row[3],
        'photo': row[4].decode('UTF-8'),
        'userResult': row[5],
        'timestamp': row[6]
        }
        listOfResults.append(result)
    cursor.close()
    return jsonify(results = listOfResults)

@app.route('/getresult/<int:user_id>', methods=['GET'])
def get_result(user_id):
    cursor = mydb.cursor()
    sql_select_query = "select * from strip WHERE id ='" + str(user_id) + "'"
    cursor.execute(sql_select_query)
    records = cursor.fetchall()
    listOfResults = []
    for row in records:
        result = {
        'id': row[0],
        'userId': row[1],
        'result': row[2],
        'accuracy': row[3],
        'photo': row[4].decode('UTF-8'),
        'userResult': row[5],
        'timestamp': row[6]
        }
        listOfResults.append(result)
    cursor.close()
    return jsonify(results = listOfResults)

@app.route('/objectdetection', methods=['POST'])
def detect_object():
    if not request.json or not 'image' in request.json:
        abort(400)

    file = request.json["image"]
    for x in range(23):
        file = file[1:]


    result = objectDetector.Object_Detection(file.encode())
    result['image'] = result['image'].decode('UTF-8')
    result['image'] = "data:image/jpeg;base64," + result['image']
    result['accuracy'] = int(result['accuracy'] * 100)

    return jsonify(results = result), 201



@app.route('/processform', methods=['POST'])
def process_form():
    session['file'] = request.form["answer"]
    for x in range(23):
        session['file'] = session['file'][1:]


    result = objectDetector.Object_Detection(session['file'].encode())

    imageResult = result['image'].decode('UTF-8')
    imageResult = "data:image/jpeg;base64," + imageResult
    name = result['name']
    accuracy = int(result['accuracy'] * 100)
    return render_template('process.html',
                           the_title="Process Results", the_result = imageResult, the_name = name, the_accuracy = accuracy )




if __name__ == '__main__':
    app.secret_key = "rkngfdbsakvbfkhjfnsakbvfknkblkfldsanvbkrjlrwewhcnkgkr"
    app.run(debug=True)
