const express = require('express');
const sqlite3 = require('sqlite3').verbose();

// Crear una nueva instancia de la aplicación Express.js
const app = express();
const port = 3000;

// Configurar la conexión a la base de datos SQLite
const db = new sqlite3.Database(':memory:'); // Cambia ':memory:' por la ruta de tu base de datos SQLite

// Crear las tablas y definir las relaciones
db.serialize(() => {
  db.run('CREATE TABLE IF NOT EXISTS Admin (username TEXT, password TEXT)');
  db.run('CREATE TABLE IF NOT EXISTS Company (id INTEGER PRIMARY KEY, company_name TEXT, company_api_key TEXT)');
  db.run('CREATE TABLE IF NOT EXISTS Location (company_id INTEGER, location_name TEXT, location_country TEXT, location_city TEXT, location_meta TEXT)');
  db.run('CREATE TABLE IF NOT EXISTS Sensor (location_id INTEGER, sensor_id INTEGER, sensor_name TEXT, sensor_category TEXT, sensor_meta TEXT, sensor_api_key TEXT)');
  db.run('CREATE TABLE IF NOT EXISTS SensorData (sensor_id INTEGER, variable_name TEXT, value REAL, timestamp TEXT)');

  // Definir relaciones
  db.run('PRAGMA foreign_keys = ON');
  db.run('CREATE INDEX IF NOT EXISTS idx_sensor_data_sensor_id ON SensorData (sensor_id)');
});

// Configurar los middleware para parsear el cuerpo de las solicitudes en formato JSON
app.use(express.json());

// Definir los endpoints
// Ejemplo de endpoint para obtener todos los registros de un modelo
app.get('/api/v1/:model', (req, res) => {
  const model = req.params.model;

  db.all(`SELECT * FROM ${model}`, (err, rows) => {
    if (err) {
      console.error(err);
      res.status(500).send('Internal Server Error');
    } else {
      res.json(rows);
    }
  });
});

// Ejemplo de endpoint para obtener un registro específico de un modelo
app.get('/api/v1/:model/:id', (req, res) => {
  const model = req.params.model;
  const id = req.params.id;

  db.get(`SELECT * FROM ${model} WHERE id = ?`, [id], (err, row) => {
    if (err) {
      console.error(err);
      res.status(500).send('Internal Server Error');
    } else if (!row) {
      res.status(404).send('Not Found');
    } else {
      res.json(row);
    }
  });
});

// Resto de endpoints (PUT, DELETE, inserción de sensor_data, etc.)

// Endpoint para la inserción de sensor_data
app.post('/api/v1/sensor_data', (req, res) => {
  const { api_key, json_data } = req.body;

  // Verificar el sensor_api_key para autorizar la inserción de datos
  db.get('SELECT * FROM Sensor WHERE sensor_api_key = ?', [api_key], (err, row) => {
    if (err) {
      console.error(err);
      res.status(500).send('Internal Server Error');
    } else if (!row) {
      res.status(400).send('Invalid sensor_api_key');
    } else {
      // Insertar los datos de sensor_data en la base de datos
      const sensorId = row.sensor_id;
      const timestamp = new Date().toISOString();

      json_data.forEach((data) => {
        const { variable_name, value } = data;
        db.run(
          'INSERT INTO SensorData (sensor_id, variable_name, value, timestamp) VALUES (?, ?, ?, ?)',
          [sensorId, variable_name, value, timestamp],
          (err) => {
            if (err) {
              console.error(err);
            }
          }
        );
      });

      res.status(201).send('Data inserted successfully');
    }
  });
});

// Endpoint para la consulta de sensor_data
app.get('/api/v1/sensor_data', (req, res) => {
  const { company_api_key, from, to, sensor_id } = req.query;

  // Verificar el company_api_key para autorizar la consulta de datos
  db.get('SELECT * FROM Company WHERE company_api_key = ?', [company_api_key], (err, row) => {
    if (err) {
      console.error(err);
      res.status(500).send('Internal Server Error');
    } else if (!row) {
      res.status(400).send('Invalid company_api_key');
    } else {
      // Consultar los datos de sensor_data según los parámetros proporcionados
      db.all(
        'SELECT * FROM SensorData WHERE sensor_id IN (?) AND timestamp >= ? AND timestamp <= ?',
        [sensor_id, from, to],
        (err, rows) => {
          if (err) {
            console.error(err);
            res.status(500).send('Internal Server Error');
          } else {
            res.json(rows);
          }
        }
      );
    }
  });
});

// Iniciar el servidor
app.listen(port, () => {
  console.log(`Servidor Express.js escuchando en el puerto ${port}`);
});
