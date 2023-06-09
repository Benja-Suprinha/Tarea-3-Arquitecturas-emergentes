from flask import Flask, request, jsonify, make_response
import sqlite3
from flask import g
import jwt
from datetime import datetime, timedelta
from json import dumps
import random
import string

DATABASSE = 'database.db'

def generate_random_string(length):
    alphanumeric = string.ascii_letters + string.digits
    return ''.join(random.choices(alphanumeric, k=length))


#KEY = 'secret'

app = Flask(__name__)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/api")
def api():
    return "API 1.0v"


# Agregar una nueva locación
@app.route("/location", methods=["POST"])
def location():
    api_key = request.json["token"]  # company_api_key
    name = request.json["name"]
    country = request.json["country"]
    city = request.json["city"]
    meta = request.json["meta"]

    db = sqlite3.connect("database.db")
    cursor = db.execute("SELECT * FROM company WHERE company_api_key=?", (api_key,))
    company = cursor.fetchone()
    if not company:
        return jsonify({"error": "Clave API invalida."}), 401
    
    location_api_key = generate_random_string(4)
    print(company[0])
    # Insertamos el Location en la base de datos
    print(company[0])
    print(name)
    print(country)
    print(city)
    print(meta)
    print(location_api_key)
    db.execute("INSERT INTO location (company_id,location_name,location_country,location_city,location_meta,location_api_key) VALUES (?, ?, ?, ?, ?, ?)",
                (company[0],name,country,city,meta, location_api_key))
    
    # Guardamos los cambios
    db.commit()
    db.close()
    return jsonify({"message": "Locacion agregada correctamente."})

    


# Mostrar lista completa
@app.route("/location", methods=["GET"])
def listlocation():
    api_key=request.json["token"]
    db = sqlite3.connect("database.db")
    cursor = db.execute("SELECT * FROM company WHERE company_api_key=?", (api_key,))
    company = cursor.fetchone()
    if not company:
        return jsonify({"error": "Clave API invalida."}), 401
    
    cursor = db.execute("SELECT * FROM Location")
    locations = cursor.fetchall()

    return jsonify({"message": "You are in the protected area", "Lista location": locations})

#por motivos de seguridad solo se podra cambiar la meta, para lo demas se tiene que borrar y volver a crear
@app.route("/location", methods=["PUT"])
def updatelocation():
    api_key=request.json["token"]
    db = sqlite3.connect("database.db")
    cursor = db.execute("SELECT * FROM company WHERE company_api_key=?", (api_key,))
    company = cursor.fetchone()
    if not company:
        return jsonify({"error": "Clave API invalida."}), 401
    
    id_location = request.json["id"]
    meta_location = request.json["meta"]

    db.execute(f"UPDATE location SET location_meta = '{meta_location}' WHERE location_id = ?",(id_location))
    db.commit()
    db.close()

    return jsonify({"message":"Update con exito"})

@app.route("/location/delete", methods=["POST"])
def deletelocation():
    location_id=request.json["id"]
    api_key=request.json["token"]
    db = sqlite3.connect("database.db")
    cursor = db.execute("SELECT * FROM company WHERE company_api_key=?", (api_key,))
    company = cursor.fetchone()
    if not company:
        return jsonify({"error": "Clave API invalida."}), 401
    
    # Verificamos si el Location existe
    cursor = db.execute("SELECT * FROM Location WHERE location_id=?", (location_id,))
    location = cursor.fetchone()
    if not location:
        return jsonify({"message":"No se encontro el id"})
    
    # Eliminamos el Location de la base de datos
    db.execute("DELETE FROM Location WHERE location_id=?", (location_id,))

    db.commit()
    db.close()

    return jsonify({"message":"Se borro con exito"})

@app.route("/sensor", methods=["GET"])
def listsensors():
    api_key=request.json["token"]
    db = sqlite3.connect("database.db")
    cursor = db.execute("SELECT * FROM location WHERE location_api_key=?", (api_key,))
    company = cursor.fetchone()
    if not company:
        return jsonify({"error": "Clave API invalida."}), 401
    
    cursor = db.execute("SELECT * FROM sensor")
    locations = cursor.fetchall()

    return jsonify({"message": "You are in the protected area", "Lista sensores": locations})

@app.route("/sensor", methods=["POST"])
def create_sensor():
    api_key = request.json["token"]  # company_api_key
    sensor_name = request.json["name"]
    sensor_cat = request.json["categoria"]
    sentor_meta = request.json["meta"]
    
    db = sqlite3.connect("database.db")
    cursor = db.execute("SELECT * FROM location WHERE location_api_key=?", (api_key,))
    company = cursor.fetchone()
    if not company:
        return jsonify({"error": "Clave API invalida."}), 401
    
    sensor_api_key = generate_random_string(4)

    db.execute("INSERT INTO sensor (location_id,sensor_name,sensor_category,sensor_meta,sensor_api_key) VALUES (?, ?, ?, ?, ?)",
                (company[0],sensor_name,sensor_cat,sentor_meta, sensor_api_key))
    
    # Guardamos los cambios
    db.commit()
    db.close()
    return jsonify({"message": "Sensor agregada correctamente."})

@app.route("/sensor", methods=["PUT"])
def updatesensor():
    return True

@app.route("/sensor/delete", methods=["POST"])
def deletesensor():
    return True

@app.route("/sensor_data", methods=["POST"])
def create_sensor_data():
    return True


@app.route("/sensor_data", methods=["GET"])
def get_sensor_data():
    return True


if __name__ == "__main__":
    app.run(port=8000,debug=True)