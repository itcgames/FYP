from flask import Flask, render_template, request, session, jsonify
import objectDetector
import mysql.connector

app = Flask(__name__)


mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  passwd="",
  database="results"
)


@app.route('/getform')
def get_and_display_form():
    return render_template('index.html',
                           the_title="GIP Strip Result Detection", )



@app.route('/getHistory/<int:limit>', methods=['GET'])
def get_history(limit):
    cursor = mydb.cursor()
    sql_select_Query = "SELECT * FROM strip ORDER BY ts DESC LIMIT " + str(limit)
    print(sql_select_Query)
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

@app.route('/getuserresults/<string:user_name>', methods=['GET'])
def get_user_results(user_name):
    cursor = mydb.cursor()
    sql_select_query = "select * from strip WHERE userId ='" + str(user_name) + "'"
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

@app.route('/addEntry/<string:user_name>/<string:user_result>', methods=['POST'])
def addEntry(user_name, user_result):
    if not request.json or not 'image' in request.json:
        abort(400)

    file = request.json["image"]
    for x in range(23):
        file = file[1:]


    result = objectDetector.Object_Detection(file.encode())
    result['image'] = result['image'].decode('UTF-8')
    result['image'] = "data:image/jpeg;base64," + result['image']
    result['accuracy'] = int(result['accuracy'] * 100)

    cursor = mydb.cursor()

    sql = "INSERT INTO strip (userId,result,accuracy,photo,userResult) VALUES (%s, %s, %s ,%s ,%s)"
    val = (user_name, result['name'][0].lower(), result['accuracy'], result['image'], user_result[0].lower())

    cursor.execute(sql, val)
    mydb.commit()


    return jsonify(results = result), 201

@app.route('/processform', methods=['POST'])
def process_form():
    session['file'] = request.form["answer"]
    session['userName'] = request.form["Username"]
    session['userResult'] = request.form["UserResult"]
    for x in range(23):
        session['file'] = session['file'][1:]


    result = objectDetector.Object_Detection(session['file'].encode())
    result['image'] = result['image'].decode('UTF-8')
    result['image'] = "data:image/jpeg;base64," + result['image']
    result['accuracy'] = int(result['accuracy'] * 100)

    cursor = mydb.cursor()

    sql = "INSERT INTO strip (userId,result,accuracy,photo,userResult) VALUES (%s, %s, %s ,%s ,%s)"
    val = (session['userName'], result['name'][0].lower(), result['accuracy'], result['image'], session['userResult'][0].lower())

    cursor.execute(sql, val)
    return render_template('process.html',
                           the_title="Process Results", the_result = result['image'], the_name = result['name'], the_accuracy = result['accuracy'] )




if __name__ == '__main__':
    app.secret_key = "rkngfdbsakvbfkhjfnsakbvfknkblkfldsanvbkrjlrwewhcnkgkr"
    app.run(debug=True)
