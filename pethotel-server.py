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

@app.route('/api/pets/', methods=['POST'])
def create_pet():
    print('request.json is a dict!', request.json)
    print('if you\'re using multipart/form data, use request.form instead!', request.form)
    print(request.json)
    pet = request.json['pet']
    owner = request.json['owner']
    breed = request.json['breed']
    color = request.json['color']

    try:
        # Avoid getting arrays of arrays!
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        print(pet, owner)
        insertQuery = "INSERT INTO pets (pet, owner, breed, color) VALUES (%s, %s, %s, %s)"
        # if only only one param, still needs to be a tuple --> cursor.execute(insertQuery, (title,)) <-- comma matters!
        cursor.execute(insertQuery, (pet, owner, breed, color))
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

    postgreSQL_select_Query = "SELECT pets.id, owners.name, pets.pet, pets.breed, pets.color, pets.checkedin FROM pets JOIN owners ON pets.owner = owners.id ORDER BY pets.id"
    # execute query
    cursor.execute(postgreSQL_select_Query)
    # Selecting rows from mobile table using cursor.fetchall
    pets = cursor.fetchall()
    # respond, status 200 is added for us
    return jsonify(pets)

# OWNER ROUTES
@app.route( '/api/owners/', methods=['POST'] )
def create_owner():
    print('request.json is a dict!', request.json)
    print('if you\'re using multipart/form data, use request.form instead!', request.form)
    print(request.json)
    name = request.json['name']
    try:
        # Avoid getting arrays of arrays!
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        print( 'owner:', name )
        insertQuery = "INSERT INTO owners ( name ) VALUES ( %s )"
        # if only only one param, still needs to be a tuple --> cursor.execute(insertQuery, (title,)) <-- comma matters!
        cursor.execute(insertQuery, ( name, ))
        # really for sure commit the query
        connection.commit()
        count = cursor.rowcount
        print(count, "Owner added")
        # respond nicely
        result = {'status': 'CREATED'}
        return jsonify(result), 201
    except (Exception, psycopg2.Error) as error:
        # there was a problem
        print("Failed to add owner", error)
        # respond with error
        result = {'status': 'ERROR'}
        return jsonify(result), 500
    finally:
        # clean up our cursor
        if(cursor):
            cursor.close()

@app.route('/api/owners/', methods=['GET'])
def list_owners():
    # Use RealDictCursor to convert DB records into Dict objects
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    postgreSQL_select_Query = "SELECT owners.id, owners.name, COUNT(pets.pet) FROM owners LEFT JOIN pets ON owners.id = pets.owner GROUP BY owners.name, owners.id ORDER BY owners.id"

    # execute query
    cursor.execute(postgreSQL_select_Query)
    # Selecting rows from mobile table using cursor.fetchall
    owners = cursor.fetchall()
    # respond, status 200 is added for us
    return jsonify(owners)

@app.route('/api/pets/', methods=['PUT'])
def checkedin():
    print('request.json is a dict!', request.json)
    print('if you\'re using multipart/form data, use request.form instead!', request.form)
    print(request.json)
    id = request.json['id']
    checkedin = request.json['checkedin']
    try:
        # Avoid getting arrays of arrays!
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        insertQuery = 'UPDATE pets SET "checkedin"=%s WHERE "id"=%s'
        # if only only one param, still needs to be a tuple --> cursor.execute(insertQuery, (title,)) <-- comma matters!
        cursor.execute(insertQuery, ( checkedin, id ))
        # really for sure commit the query
        connection.commit()
        count = cursor.rowcount
        print(count, "CHECKEDIN updated")
        # respond nicely
        result = {'status': 'UPDATED'}
        return jsonify(result), 201
    except (Exception, psycopg2.Error) as error:
        # there was a problem
        print("Failed to update", error)
        # respond with error
        result = {'status': 'ERROR'}
        return jsonify(result), 500
    finally:
        # clean up our cursor
        if(cursor):
            cursor.close()

# Delete PET
@app.route('/api/delete/', methods=['POST'])
def deletePet():
    print('request.json is a dict!', request.json)
    print('if you\'re using multipart/form data, use request.form instead!', request.form)

    try:
        # Avoid getting arrays of arrays!
        id = request.json['id']
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        insertQuery = 'DELETE FROM pets WHERE "id"=%s'
        # if only only one param, still needs to be a tuple --> cursor.execute(insertQuery, (title,)) <-- comma matters!
        cursor.execute(insertQuery, ( id, ))
        # really for sure commit the query
        connection.commit()
        count = cursor.rowcount
        print(count, "Pet Deleted")
        # respond nicely
        result = {'status': 'DELETED'}
        return jsonify(result), 201
    except (Exception, psycopg2.Error) as error:
        # there was a problem
        print("Failed to add owner", error)
        # respond with error
        result = {'status': 'ERROR'}
        return jsonify(result), 500
    finally:
        # clean up our cursor
        if(cursor):
            cursor.close()

app.run()