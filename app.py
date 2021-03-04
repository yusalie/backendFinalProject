import sqlite3
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS


def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Database opened successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS users('
                 'Firstname TEXT,'
                 'Lastname TEXT,'
                 'Username TEXT PRIMARY KEY,'
                 'Email TEXT,'
                 'Password TEXT )'
                 )
    print("user table created successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS manga('
                 'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                 'img TEXT, title TEXT, titleJp TEXT,'
                 'written_by INTEGER,'
                 'published_by TEXT,'
                 'genre TEXT,'
                 'synopsis TEXT)')
    print("manga table created successfully")


init_sqlite_db()

app = Flask(__name__)
CORS(app)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/')
@app.route('/manga-content/', methods=['GET'])
def show_data():
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dict_factory
            cursor = con.cursor()
            cursor.execute('SELECT * FROM manga')
            data = cursor.fetchall()
            return jsonify(data)
    except:
        pass


@app.route('/register-user/', methods=["POST"])
def register_user():
    msg = None
    try:
        post_data = request.get_json()
        firstname = post_data['firstname']
        lastname = post_data['lastname']
        username = post_data['username']
        email = post_data['email']
        password = post_data['password']
        with sqlite3.connect('database.db') as conn:

            cur = conn.cursor()
            cur.execute("INSERT INTO users(Firstname, Lastname, Username, Email, Password)VALUES"
                        "(?, ?, ?, ?, ?)", (firstname, lastname, username, email, password))
            print(cur)
            conn.commit()
            msg = "Record added successfully."

    except Exception as e:
        return {'error': str(e)}
    finally:
        conn.close()
        return {'msg': msg}


@app.route('/show-users/', methods=['GET'])
def show_users():
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dict_factory
            cursor = con.cursor()
            cursor.execute('SELECT * FROM users')
            data = cursor.fetchall()
            return jsonify(data)

    except Exception as e:
        print(e)

# @app.route('/test/')
# def test():
#     return render_template('login_test_file.html/')

@app.route('/login/', methods=['GET'])
def login():
    if request.method == 'GET':
        response = {}
        response['msg'] = None
        response['body'] = []

        try:
            with sqlite3.connect('database.db') as con:
                con.row_factory = dict_factory
                cursor = con.cursor()
                cursor.execute('SELECT * FROM users')
                admins = cursor.fetchall()
                response['body'] = admins
                response['msg'] = "user logged in "

        except Exception as e:
            con.rollback()
            response['msg'] = "wrong bro:" + str(e)
            print(e)

        finally:
            return response

