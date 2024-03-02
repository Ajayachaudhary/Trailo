from flask import Flask, Response, render_template, request, redirect, flash
import mysql.connector
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY','a_default_secret_key')

mydb = mysql.connector.connect(
    host = "localhost",
    user ="ajay",
    password = "Aj@ya",
    database="project"
)

def serializer(data):
    # Modify serializer to handle a list of tuples
    serialized_list = []
    for item in data:
        serialized_item = {
            "id": item[0],
            "i_name": item[1],
            "name": item[2],
            "type": item[3],
            "description":item[4],
            "url": item[5]    
        }
        serialized_list.append(serialized_item)
    return serialized_list

def image_serializer(data):
    # Modify serializer to handle a list of tuples
    serialized_list = []
    for item in data:
        serialized_item = {
            "id": item[0],
            "i_name": item[1],
            "name": item[2],
            "type": item[3],
            "description":item[4],
        }
        serialized_list.append(serialized_item)
    return serialized_list

@app.route("/")
def home():
    # cursor = mysql.connection.cursor()
    cursor = mydb.cursor(buffered=True)
    cursor.execute("SELECT * FROM image WHERE  types='Movie'") 
    movie_images= image_serializer(cursor.fetchall())
    cursor.execute("SELECT * FROM image WHERE  types='Series'") 
    series_images= image_serializer(cursor.fetchall())
    cursor.close()
    return render_template("index.html", movie_images=movie_images, series_images = series_images) 

@app.route('/video-play',methods=["GET"])
def video_url_retrieve():
    video_id= request.args.get('id',type=int)
    cursor = mydb.cursor(buffered=True)
    cursor.execute('SELECT video_link FROM video_url WHERE id=%s',(video_id,))
    video_link= cursor.fetchone()
    cursor.execute('SELECT description_of_movies_series from image WHERE id=%s',(video_id,))
    description = cursor.fetchone()
    cursor.close()
    return render_template("video.html", video_link=video_link[0],description = description)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/loginauth", methods=['POST'])
def loginauth():
    email = request.form.get('email')
    password = request.form.get('password')
    if email == 'admin' and password == 'password':
        return render_template("admin.html")
    else:
        return render_template("login.html",message='invalid usernamr or password. Try again!')

@app.route('/logout')
def logout():
    return redirect("/")


@app.route('/add', methods=['POST'])
def add_data():
    try:
        image =request.files['myimage']
        image_name = secure_filename(image.filename)
        movie_series_name = request.form.get('Name')
        video_url = request.form.get('link')
        types_of_video = request.form.get('type').capitalize()
        description_of_video = request.form.get('description')

        cursor = mydb.cursor(buffered=True)
        query_to_image = ("INSERT INTO image (image_name, movie_series_name, types, description_of_movies_series) "
                        "VALUES (%s, %s, %s, %s)")
        data_to_image = (image_name, movie_series_name, types_of_video, description_of_video)
        cursor.execute(query_to_image, data_to_image)
        image_id = cursor.lastrowid # get the id of the inserted image data

        query_to_video = ("INSERT INTO video_url (id, video_link) VALUES (%s, %s)")
        data_to_video = (image_id,video_url)
        cursor.execute(query_to_video,data_to_video)

        mydb.commit() # make sure data is committed to database
        cursor.close()
        flash('Data successfully added')
        if types_of_video == 'Movie':
            return redirect("/admin_movie")
        else:
            return redirect("/admin_series")
    except Exception as e:
        flash(str(e))
        return redirect("/admin_movie")


@app.route('/admin_movie')
def movie_data():
    cursor = mydb.cursor(buffered=True)
    cursor.execute("SELECT * FROM image natural join video_url where types='Movie'")
    datas = serializer(cursor.fetchall())
    cursor.close()
    return render_template("admin_movie.html", datas = datas)


@app.route('/delete', methods=['GET'])
def delete():
    id = request.args.get('id', type=int)
    content_type = request.args.get('type', type=str)  # Get the type of content

    cursor = mydb.cursor(buffered=True)
    cursor.execute('DELETE from image where id = %s', (id,))
    affected_rows = cursor.rowcount
    mydb.commit()
    cursor.close()

    if affected_rows > 0:
        # Redirect based on the content type
        if content_type == 'Movie':
            return redirect("/admin_movie")
        else:
            return redirect("/admin_series")
    else:
        # Handle the case where no rows were affected/deleted
        return "Error: No item found with the specified ID", 404 
    

@app.route('/update',methods = ['POST'])
def update_data():
    try:
        # Convert id to integer
        id = int(request.form.get('id'))
        movie_series_name = request.form.get('Name')
        video_url = request.form.get('link')
        types_of_video = request.form.get('type').capitalize()
        description_of_video = request.form.get('description')

        cursor = mydb.cursor(buffered=True)

        # Corrected column name assuming it was a typo
        cursor.execute("""UPDATE image SET 
                       movie_series_name = %s, types = %s,
                       description_of_movies_series = %s 
                       WHERE id = %s
                       """, (movie_series_name, types_of_video, description_of_video, id))

        cursor.execute("UPDATE video_url SET video_link = %s WHERE id = %s", (video_url, id))

        mydb.commit()
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        # Optionally, add a redirect to an error page or return an error message
    finally:
        cursor.close()

    if types_of_video == 'Movie':
        return redirect("/admin_movie")
    else:  # Assuming the other type is for series, adjust as necessary
        return redirect("/admin_series")


   
@app.route('/admin_series')
def series_data():
    cursor = mydb.cursor(buffered=True)
    cursor.execute("SELECT * FROM image natural join video_url where types='Series'")
    datas = serializer(cursor.fetchall())
    cursor.close()
    return render_template("admin_series.html", datas = datas)

if __name__ == '__main__':
    app.run(debug=True)

