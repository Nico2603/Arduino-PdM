### Ingestor MQTT → PostgreSQL (Linux)

Servicio que se suscribe al tópico MQTT y guarda los datos en PostgreSQL.

#### Requisitos en Linux
- Python 3.10+ (ideal 3.12)
- Acceso a PostgreSQL (servidor: 10.1.11.230 puerto 5432)

#### Instalación
```bash
# 1) Entrar a la carpeta
cd mqtt_ingestor

# 2) Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3) Instalar dependencias
pip install -r requirements.txt

# 4) Variables de entorno
cp .env.example .env
# (ya dejamos .env con tus valores reales)

# 5) Crear tablas (opcional, main.py también las crea)
psql -h 10.1.11.230 -p 5432 -U consultadb -d sensor -f create_tables.sql

# 6) Ejecutar
python3 main.py
```

#### Variables de entorno (`.env`)
- MQTT_BROKER (ej. broker.hivemq.com)
- MQTT_PORT (1883)
- MQTT_TOPIC (GL_Ingenieros/sensores/vibracion)
- PG_HOST (10.1.11.230)
- PG_PORT (5432)
- PG_DB (sensor)
- PG_USER (consultadb)
- PG_PASSWORD

#### Ejecutar como servicio (systemd)
```bash
# Edita la ruta absoluta del repo en mqtt_ingestor.service
sudo cp mqtt_ingestor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable mqtt_ingestor
sudo systemctl start mqtt_ingestor
sudo systemctl status mqtt_ingestor -l
```

#### Esquema de datos
- Tópico: `GL_Ingenieros/sensores/vibracion`
- JSON esperado:
```json
{
  "sensor_id": 1,
  "timestamp": "2024-01-15T10:30:45Z",
  "acceleration_x": -0.234,
  "acceleration_y": 9.821,
  "acceleration_z": 0.156
}
```
- Tabla: `public.vibration_data`
  - `id` BIGSERIAL PK
  - `sensor_id` INTEGER NOT NULL
  - `ts` TIMESTAMPTZ NOT NULL
  - `acceleration_x|y|z` DOUBLE PRECISION NOT NULL
  - `raw_json` JSONB (copia completa del mensaje)
