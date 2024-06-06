from flask import Flask, render_template, redirect, url_for, session, request, flash
import psycopg2
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__, static_url_path='/static')

# Set your own database name, username and password
db = "dbname='INSERT HERE' user='' host='localhost' password='INSERT HERE'"
conn = psycopg2.connect(db)
cursor = conn.cursor()

bcrypt = Bcrypt(app)

@app.route("/createaccount", methods=['POST', 'GET'])
def createaccount():
    cur = conn.cursor()
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        cur.execute("SELECT * FROM users WHERE username = %s", (new_username,))
        unique = cur.fetchall()
        if len(unique) == 0:
            cur.execute("INSERT INTO users(username, password) VALUES (%s, %s)", (new_username, new_password))
            conn.commit()
            flash('Account created!')
            return redirect(url_for("home"))
        else:
            flash('Username already exists!')

    return render_template("createaccount.html")

@app.route("/", methods=["POST", "GET"])
def home():
    try:
        cur = conn.cursor()

        if request.method == "POST":
            input_lyrics = request.form.get("id").lower()
            radio_value = request.form.get("radio")

            if radio_value == "animals":
                # Define the regex pattern for animal names
                animal_pattern = "(^|[^a-zA-Z])(dog|horse|cat|cow|panda|snake|bird|owl|kitty|puppy|crocodile)($|[^a-zA-Z])"
                cur.execute("SELECT * FROM Songs WHERE word_search_column ~ %s LIMIT 30", (animal_pattern,))

            elif radio_value == "countries":
                # Define the regex pattern for animal names
                country_pattern = "(^|[^a-zA-Z])(usa|uk|denmark|america|england|australia|brazil)($|[^a-zA-Z])"
                cur.execute("SELECT * FROM Songs WHERE word_search_column ~ %s LIMIT 30", (country_pattern,))            

            elif radio_value == "weather":
                # Define the regex pattern for animal names
                weather_pattern = "(^|[^a-zA-Z])(storm|sun|rain|raining|stormy|sunny|snow|snowing|sandstorm|wind)($|[^a-zA-Z])"
                cur.execute("SELECT * FROM Songs WHERE word_search_column ~ %s LIMIT 30", (weather_pattern,))     

            elif radio_value == "cities":
                # Define the regex pattern for animal names
                city_pattern = "(^|[^a-zA-Z])(new york|chicago|los angeles|tokyo|copenhagen|oslo|seattle|london|paris|berlin)($|[^a-zA-Z])"
                cur.execute("SELECT * FROM Songs WHERE word_search_column ~ %s LIMIT 30", (city_pattern,))  

            elif input_lyrics:
                # Define the regex pattern for the input lyrics
                regex_pattern = f"(^|[^a-zA-Z]){input_lyrics}($|[^a-zA-Z])"
                cur.execute("SELECT * FROM Songs WHERE word_search_column ~ %s LIMIT 30", (regex_pattern,))
            else:
                # Get 30 random rows from Songs if no input lyrics and no animal filter are provided
                tenrand = '''SELECT * FROM Songs ORDER BY RANDOM() LIMIT 30'''
                cur.execute(tenrand)
        else:
            # Get 30 random rows from Songs when the page is loaded initially
            tenrand = '''SELECT * FROM Songs ORDER BY RANDOM() LIMIT 30'''
            cur.execute(tenrand)

        songs = list(cur.fetchall())
        length = len(songs)

        # Getting random id from table Songs

        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            return render_template("index.html", content=songs, length=length)
    except psycopg2.Error as e:
        conn.rollback()
        print("Database error:", e)
        flash("Error: Failed to retrieve data from the database.")
        return redirect(url_for('home'))
    finally:
        cur.close()


@app.route('/login', methods=['POST'])
def do_admin_login():
    cur = conn.cursor()
    username = request.form['username']
    password = request.form['password'] 

    cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    ifcool = len(cur.fetchall()) != 0

    if ifcool:
        session['logged_in'] = True
        session['username'] = username
    else:
        flash('wrong password!')
    return redirect(url_for("home"))

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route("/profile")
def profile():
    cur = conn.cursor()
    if not session.get('logged_in'):
        return render_template('login.html')
    
    username = session['username']

    sql1 = "SELECT Songs.id, Songs.Artist, Songs.Title FROM Songs JOIN Favorites ON Songs.id = Favorites.id WHERE Favorites.username = %s;"
    cur.execute(sql1, (username,))
    favs = cur.fetchall()
    return render_template("profile.html", content=favs, length=len(favs), username=username)

@app.route("/song/<id>", methods=["POST", "GET"])
def songpage(id):
    try:
        cur = conn.cursor()
        print("Reached songpage route")
        if not session.get('logged_in'):
            print("Not logged in")
            return render_template('login.html')

        
        sql_retrieve_data = f'''SELECT * FROM songs WHERE id = '{id}' '''
        print("SQL Query:", sql_retrieve_data)
        cur.execute(sql_retrieve_data)
        song_data = cur.fetchone()
        print("Song data:", song_data)

        if song_data:
            return render_template("song.html", song_data=song_data)
        else:
            flash("Error: No data found for the given id.")
            return redirect(url_for('home'))
    except psycopg2.Error as e:
        conn.rollback()
        print("Database error:", e)
        flash("Error: Failed to retrieve data from the database.")
        return redirect(url_for('home'))
    finally:
        cur.close()


@app.route("/add_to_favorites_song", methods=["POST"])
def add_to_favorites_song():
    try:
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        
        cur = conn.cursor()
        
        song_id = request.form.get('id')
        title = request.form.get('Title')
        artist = request.form.get('Artist')
        username = session['username']
        
        cur.execute("INSERT INTO Favorites (id, username, artist, title) VALUES (%s, %s, %s, %s)", 
                    (song_id, username, artist, title))
        conn.commit()
        
        flash("Song added to favorites successfully!","success")
        return redirect(url_for('songpage', id=song_id))
    except psycopg2.Error as e:
        conn.rollback()
        print("Database error:", e)
        flash("Error: Song is already added to favorites!","error")
        return redirect(url_for('home'))
    finally:
        cur.close()


@app.route("/remove_favorites", methods=["POST"])
def remove_from_favorites():
    try:
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        
        cur = conn.cursor()
        
        song_id = request.form.get('id')
        username = session['username']
        
        cur.execute("DELETE FROM Favorites WHERE id = %s AND username = %s", 
                    (song_id,username))
        conn.commit()
        
        flash("Song removed from favorites successfully!", "success")
        return redirect(url_for('songpage', id=song_id))
    except psycopg2.Error as e:
        conn.rollback()
        print("Database error:", e)
        flash("Error: Song is not in favorites!","error")
        return redirect(url_for('home'))
    finally:
        cur.close()


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
