# Songquiz - find your songquiz songs!

# running songquiz project:

(1) install dependencies through pip install:
go to the terminal and relocate to the songquiz_project directory and type in:
>$ pip install -r requirements.txt

(2) Open up postgres and start a server.

(3) Open pgAdmin4 and create a new database. Give it a name and remember the name and user of the database. It could be named fx "songquiz_database", and the user could be "postgres"

(4) Create the necessary tables in the database:
In the "Create Songs.SQL" and "Create Users.SQL" change the directory to the full path of the 'filtered_song.csv' and 'Users.csv' files. Should be something like "Path/To/Project/songquiz_project/tmp/filtered_song.csv" or "Path/To/Project/songquiz_project/tmp/Users.csv"

Now in pgAdmin, right click the created database and press the "PSQL Tool" button. Now find the sql files in the songquiz_project directory, named "Create Songs.SQL", "Create Users.SQL", "Favorites.SQL" and copy one by one these files into the PSQL Tool in pgAdmin4. This should create 3 new tables called songs, users and favorites.

(5) In the songquiz_project directory, open the file "app.py" and set your own database username and password
it should look something like: 
db = "dbname='songquiz_database' user='postgres' host='localhost' password='postgres'"

(6) Run Web-App. In terminal go to songquiz_project directory and write:
>$ python src/app.py


----------------------------------------------------------------------------------------------

# How to use the application:

(1) Create account / You start by pressing the 'Create Account' button, you then get to page where you choose your username and password. You may also use the two predefined users with usernames "jakob" or "johan" and the common password "1234"

(2) Login / Now you can login on your account by typing in your username and password.

(3) Frontpage / On the frontpage you will see 30 different songs displayed, a search bar, and some predefined search options

(4) Songs / Each song have their own page where you can see artist, title, album and lyrics. You can also add/remove each song to your own favorite songs.

(5) Searching / In the search bar you can type in a single lowercase word and the machine will search through the song database and try to find that word. Once its done searching, it will display 30 songs on the page, that mathched the search word. It will match the search word on either artist name, album name or lyrics.
		
(6) Predifined search / Underneath the searchbar is some predifined search topics you can press. These consists of a list of words it searches for.

(7) Profile / Each user have their own individual page where they can see their favorite songs.

(8) Contact / At last we have a 'contact' page where you can read a little about the project founders.


