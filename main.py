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
    name = request.json["name"]
    country = request.json["country"]
    city = request.json["city"]

    db.execute(f"UPDATE location SET location_name = '{name}', location_country = '{country}', location_city = '{city}', location_meta = '{meta_location}' WHERE location_id = ?",(id_location))
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
    cursor = db.execute("SELECT * FROM location WHERE location_id=?", (location_id,))
    location = cursor.fetchone()
    if not location:
        return jsonify({"message":"No se encontro el id"})
    
    # Eliminamos el Location de la base de datos
    db.execute("DELETE FROM location WHERE location_id=?", (location_id,))

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
    api_key = request.json["token"]  # location_api_key
    sensor_name = request.json["name"]
    sensor_cat = request.json["categoria"]
    sensor_meta = request.json["meta"]
    
    db = sqlite3.connect("database.db")
    cursor = db.execute("SELECT * FROM location WHERE location_api_key=?", (api_key,))
    company = cursor.fetchone()
    if not company:
        return jsonify({"error": "Clave API invalida."}), 401
    
    sensor_api_key = generate_random_string(4)

    db.execute("INSERT INTO sensor (location_id,sensor_name,sensor_category,sensor_meta,sensor_api_key) VALUES (?, ?, ?, ?, ?)",
                (company[0],sensor_name,sensor_cat,sensor_meta, sensor_api_key))
    
    # Guardamos los cambios
    db.commit()
    db.close()
    return jsonify({"message": "Sensor agregada correctamente."})

@app.route("/sensor", methods=["PUT"])
def updatesensor():
    api_key = request.json["token"]  # company_api_key
    sensor_name = request.json["name"]
    sensor_cat = request.json["categoria"]
    sensor_meta = request.json["meta"]
    sensor_id = request.json["id"]
    
    db = sqlite3.connect("database.db")
    cursor = db.execute("SELECT * FROM location WHERE location_api_key=?", (api_key,))
    company = cursor.fetchone()
    if not company:
        return jsonify({"error": "Clave API invalida."}), 401
    
    db.execute(f"UPDATE sensor SET sensor_name = '{sensor_name}', sensor_category = '{sensor_cat}', sensor_meta = '{sensor_meta}' WHERE sensor_id = ?",(sensor_id))
    db.commit()
    db.close()

    return jsonify({"message":"Update con exito"})

@app.route("/sensor/delete", methods=["POST"])
def deletesensor():
    sensor_id=request.json["id"]
    api_key=request.json["token"]
    db = sqlite3.connect("database.db")
    cursor = db.execute("SELECT * FROM location WHERE location_api_key=?", (api_key,))
    company = cursor.fetchone()
    if not company:
        return jsonify({"error": "Clave API invalida."}), 401
    
    # Verificamos si el Location existe
    cursor = db.execute("SELECT * FROM sensor WHERE sensor_id=?", (sensor_id,))
    location = cursor.fetchone()
    if not location:
        return jsonify({"message":"No se encontro el id"})
    
    # Eliminamos el Location de la base de datos
    db.execute("DELETE FROM sensor WHERE sensor_id=?", (sensor_id,))

    db.commit()
    db.close()

    return jsonify({"message":"Se borro con exito"})

@app.route("/sensor_data", methods=["POST"])
def create_sensor_data():
    api_key = request.json["token"]  # sensor_api_key
    time = request.json["time"]
    data = request.json["data"]
    
    db = sqlite3.connect("database.db")
    cursor = db.execute("SELECT * FROM sensor WHERE sensor_api_key=?", (api_key,))
    sensor = cursor.fetchone()
    if not sensor:
        return jsonify({"error": "Clave API invalida."}), 401
    
    db.execute("INSERT INTO sensor_data (sensor_id,timestamp,data) VALUES (?, ?, ?)",
                (sensor[0],time,data))

    db.commit()
    db.close()

    return jsonify({"message":"Se guardo la data correctamente"})


@app.route("/sensor_data", methods=["GET"])
def get_sensor_data():
    api_key = request.json["token"]  # sensor_api_key
    time_i = request.json["time0"]
    time_f = request.json["time1"]
    sensor_id = request.json["sensor_id"]
    db = sqlite3.connect("database.db")
    cursor = db.execute("SELECT * FROM sensor WHERE sensor_api_key=?", (api_key,))
    sensor = cursor.fetchone()
    if not sensor:
        return jsonify({"error": "Clave API invalida."}), 401
    
    cursor = db.execute("SELECT * FROM sensor_data WHERE sensor_id IN ({}) AND timestamp >= ? AND timestamp <= ?".format(','.join('?'*len(sensor_id))),(*sensor_id, time_i, time_f))
    sensor_data = cursor.fetchall()
    
    sensor_data_list = []
    for row in sensor_data:
        sensor = {
            'sensor_data_id':row[0],
            'sensor_id':row[1],
            'variable1':row[2],
            'variable2':row[3],
            'timestamp':row[4]
        }
        sensor_data_list.append(sensor)
    db.close()
    if(len(sensor_data_list) == 0):
        return jsonify({"error": "no hay datos."}), 401
     
    return jsonify({"message": "You are in the protected area", "Lista data": sensor_data_list})

    

if __name__ == "__main__":
    app.run(port=8000,debug=True)