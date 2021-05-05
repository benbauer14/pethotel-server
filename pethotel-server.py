import flask
import psycopg2
from flask import request, jsonify
from psycopg2.extras import RealDictCursor

app = flask.Flask(__name__)
app.config["DEBUG"] = True

connection = psycopg2.connect(
    host='localhost',
    port="5432",
    database="pethotel"
)

@app.route('/api/pets', methods=['POST'])
def create_pet():
    print('request.json is a dict!', request.json)
    print('if you\'re using multipart/form data, use request.form instead!', request.form)
    petname = request.form['petname']
    owner = request.form['owner']

    try:
        # Avoid getting arrays of arrays!
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        print(petname, owner)
        insertQuery = "INSERT INTO pets (petname, owner) VALUES (%s, %s)"
        # if only only one param, still needs to be a tuple --> cursor.execute(insertQuery, (title,)) <-- comma matters!
        cursor.execute(insertQuery, (petname, owner))
        # really for sure commit the query
        connection.commit()
        count = cursor.rowcount
        print(count, "Pet added")
        # respond nicely
        result = {'status': 'CREATED'}
        return jsonify(result), 201
    except (Exception, psycopg2.Error) as error:
        # there was a problem
        print("Failed to add pet", error)
        # respond with error
        result = {'status': 'ERROR'}
        return jsonify(result), 500
    finally:
        # clean up our cursor
        if(cursor):
            cursor.close()


@app.route('/api/pets/', methods=['GET'])
def list_pets():
    # Use RealDictCursor to convert DB records into Dict objects
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    postgreSQL_select_Query = "SELECT * FROM pets"
    # execute query
    cursor.execute(postgreSQL_select_Query)
    # Selecting rows from mobile table using cursor.fetchall
    pets = cursor.fetchall()
    # respond, status 200 is added for us
    return jsonify(pets)

#     # for row in books:
#     #     print("Id = ", row[0], )
#     #     print("Title = ", row[1])
#     #     print("Author  = ", row[2], "\n")


app.run()