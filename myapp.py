from flask import Flask, Response, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
    host = "localhost",
    user ="",
    password = "",
    database="project"
)

def serializer(data):
    # Modify serializer to handle a list of tuples
    serialized_list = []
    for item in data:
        serialized_item = {
            "id": item[0],
            "image_name": item[1],
            "image_desc": item[2]
        }
        serialized_list.append(serialized_item)
    return serialized_list



@app.route("/")
def home():
    # cursor = mysql.connection.cursor()
    cursor = mydb.cursor(buffered=True)
    cursor.execute('SELECT * FROM image') 
    images= serializer(cursor.fetchall())
    cursor.close()
    return render_template("index.html", images=images) 

@app.route('/video-play',methods=["GET"])
def video_url_retrieve():
    video_id= request.args.get('id',type=int)
    cursor = mydb.cursor(buffered=True)
    cursor.execute('SELECT video_link FROM video_url WHERE id=%s',(video_id,))
    video_link= cursor.fetchone()
    cursor.close()
    return render_template("video_template.html", video_link=video_link[0])

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/loginauth", methods=['POST'])
def loginauth():
    email = request.form.get('email')
    password = request.form.get('password')
    if email == 'admin' and password == 'password':
        return redirect("/")
    else:
        return render_template("login.html",message='invalid usernamr or password. Try again!')



if __name__ == '__main__':
    app.run(debug=True)