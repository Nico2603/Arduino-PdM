import os
import json
import time
import logging
from datetime import datetime
from typing import Optional

import psycopg2
from psycopg2.extras import Json
import paho.mqtt.client as mqtt
from dotenv import load_dotenv


def setup_logging() -> logging.Logger:
	logger = logging.getLogger("mqtt_ingestor")
	logger.setLevel(logging.INFO)
	if not logger.handlers:
		handler = logging.StreamHandler()
		handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
		logger.addHandler(handler)
	return logger


logger = setup_logging()
load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER", "broker.hivemq.com")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "GL_Ingenieros/sensores/vibracion")

PG_HOST = os.getenv("PG_HOST", "10.1.11.230")
PG_PORT = int(os.getenv("PG_PORT", "5432"))
PG_DB = os.getenv("PG_DB", "sensor")
PG_USER = os.getenv("PG_USER", "consultadb")
PG_PASSWORD = os.getenv("PG_PASSWORD", "")


class PostgresClient:
	def __init__(self) -> None:
		self.conn: Optional[psycopg2.extensions.connection] = None

	def connect(self) -> None:
		if self.conn is not None:
			try:
				self.conn.close()
			except Exception:
				pass
		self.conn = psycopg2.connect(
			host=PG_HOST,
			port=PG_PORT,
			database=PG_DB,
			user=PG_USER,
			password=PG_PASSWORD,
			connect_timeout=10,
		)
		self.conn.autocommit = True
		logger.info("Conexión a PostgreSQL establecida")

	def ensure_tables(self) -> None:
		assert self.conn is not None
		create_sql = """
		CREATE TABLE IF NOT EXISTS public.vibration_data (
			id BIGSERIAL PRIMARY KEY,
			sensor_id INTEGER NOT NULL,
			ts TIMESTAMPTZ NOT NULL,
			acceleration_x DOUBLE PRECISION NOT NULL,
			acceleration_y DOUBLE PRECISION NOT NULL,
			acceleration_z DOUBLE PRECISION NOT NULL,
			raw_json JSONB NOT NULL DEFAULT '{}'::jsonb
		);
		CREATE INDEX IF NOT EXISTS idx_vibration_data_ts ON public.vibration_data (ts);
		CREATE INDEX IF NOT EXISTS idx_vibration_data_sensor ON public.vibration_data (sensor_id);
		"""
		with self.conn.cursor() as cur:
			cur.execute(create_sql)
		logger.info("Tabla vibration_data verificada/creada")

	def insert_vibration(self, data: dict) -> None:
		assert self.conn is not None
		insert_sql = (
			"INSERT INTO public.vibration_data (sensor_id, ts, acceleration_x, acceleration_y, acceleration_z, raw_json) "
			"VALUES (%s, %s, %s, %s, %s, %s)"
		)
		with self.conn.cursor() as cur:
			cur.execute(
				insert_sql,
				[
					int(data["sensor_id"]),
					parse_timestamp(data.get("timestamp")),
					float(data["acceleration_x"]),
					float(data["acceleration_y"]),
					float(data["acceleration_z"]),
					Json(data),
				],
			)


def parse_timestamp(ts_value: Optional[str]) -> datetime:
	if not ts_value:
		return datetime.utcnow()
	# Aceptar ISO8601 con Z
	try:
		ts_norm = ts_value.replace("Z", "+00:00")
		return datetime.fromisoformat(ts_norm)
	except Exception:
		return datetime.utcnow()


class MQTTIngestor:
	def __init__(self, db: PostgresClient) -> None:
		self.db = db
		self.client = mqtt.Client()
		self.client.on_connect = self.on_connect
		self.client.on_message = self.on_message
		self.client.on_disconnect = self.on_disconnect

	def on_connect(self, client, userdata, flags, rc):
		if rc == 0:
			logger.info(f"Conectado a MQTT {MQTT_BROKER}:{MQTT_PORT}")
			client.subscribe(MQTT_TOPIC)
			logger.info(f"Suscrito a: {MQTT_TOPIC}")
		else:
			logger.error(f"Error de conexión MQTT rc={rc}")

	def on_disconnect(self, client, userdata, rc):
		logger.warning(f"Desconectado de MQTT rc={rc}")
		# reconexión automática se maneja por loop_forever

	def on_message(self, client, userdata, msg):
		payload = msg.payload.decode("utf-8", errors="ignore")
		logger.info(f"Mensaje en {msg.topic}: {payload}")
		try:
			data = json.loads(payload)
			for field in ["sensor_id", "timestamp", "acceleration_x", "acceleration_y", "acceleration_z"]:
				if field not in data:
					raise ValueError(f"Campo requerido faltante: {field}")
			self.db.insert_vibration(data)
			logger.info("✓ Insertado en PostgreSQL")
		except Exception as e:
			logger.error(f"Error procesando/insertando mensaje: {e}")

	def start(self) -> None:
		# Conectar DB
		attempt = 0
		while True:
			try:
				self.db.connect()
				self.db.ensure_tables()
				break
			except Exception as e:
				attempt += 1
				wait_s = min(30, 2 * attempt)
				logger.error(f"Error conectando a PostgreSQL: {e}. Reintentando en {wait_s}s...")
				time.sleep(wait_s)

		# Conectar MQTT (loop bloqueante con autoreconexión)
		while True:
			try:
				self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
				self.client.loop_forever()
			except Exception as e:
				logger.error(f"Error en cliente MQTT: {e}. Reintentando en 5s...")
				time.sleep(5)


def main() -> None:
	logger.info("Iniciando ingestor MQTT → PostgreSQL")
	db = PostgresClient()
	ingestor = MQTTIngestor(db)
	ingestor.start()


if __name__ == "__main__":
	main()
