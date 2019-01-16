from flask import Flask, render_template, request, session
import objectDetector
app = Flask(__name__)

@app.route('/getform')
def get_and_display_form():
    return render_template('index.html',
                           the_title="GIP Strip Result Detection", )

@app.route('/processform', methods=['POST'])
def process_form():
    session['file'] = request.form["answer"]
    for x in range(23):
        session['file'] = session['file'][1:]


    result = objectDetector.Object_Detection(session['file'].encode())

    result = result.decode('UTF-8')
    result = "data:image/jpeg;base64," + result
    return render_template('process.html',
                           the_title="Process Results", the_result = result )




if __name__ == '__main__':
    app.secret_key = "rkngfdbsakvbfkhjfnsakbvfknkblkfldsanvbkrjlrwewhcnkgkr"
    app.run(debug=True)
