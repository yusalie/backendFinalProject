from flask import jsonify, Flask
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def dict_factory(cursor, row):
    d={}
    for idx, col in enumerate(cursor.description):
        d[col[0]]=row[idx]
    return d

@app.route('/' , methods=['GET'])
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

if __name__ == '__main__':
    app.run(debug=True)
    