from flask import Flask, render_template, request, redirect, send_from_directory, url_for
import pymongo
import os


connection = pymongo.MongoClient('localhost', 27017)
database = connection['task4']
collection = database['users']


app = Flask (__name__)
app.secret_key = 'secret key'
app.config['UPLOAD_FOLDER'] = 'upload'

#################################
#task3 authentication data
#users={
#    "mr admin": "admin",
#    "ms admin": "admin",
#    "mr user": "user",
#    "ms user": "user"
#}
#################################

@app.route("/", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		username = request.form['username']
		password = request.form['password']
		us = database.users.find_one({"username": username})
		pa = database.users.find_one({"password": password})
		try:
			if password == pa["password"] or username == us["username"]:
				return redirect ('/cabinet')    
		except:
			return render_template('invalid.html')
	else:
		return render_template('login.html')
	return render_template('login.html')

@app.route("/cabinet", methods=['GET', 'POST'])
def cabinet():
    if request.method == "POST":
        ff = request.files['file']
        ff.save(os.path.join(app.config['UPLOAD_FOLDER'], ff.filename))
    else:
        return render_template('cabinet.html')
    return redirect(url_for('uploaded_file', filename=ff.filename))

@app.route("/upload/<filename>")
def uploaded_file (filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/favicon.ico')
def favicon():
	return send_from_directory("static", "favicon.ico", mimetype="image/vnd.microsoft.icon")

if __name__ == "__main__":
	app.run(host='localhost', port=5000, debug=True)

connection.close()
