# ESP32 Sensor - PdM-Manager v2.0.0

Sistema de monitoreo de vibraciones con ESP32, sensor MPU6050 y comunicación MQTT.

## 🔧 Características

- ✅ **Comunicación MQTT** - Envío de datos en tiempo real
- ✅ **Almacenamiento offline** - SPIFFS para datos sin conexión
- ✅ **Sincronización NTP** - Timestamps precisos
- ✅ **WiFi robusto** - Reconexión automática
- ✅ **Comandos remotos** - Control vía MQTT
- ✅ **Compatible** - ESP32 Core v2.x y v3.x

## 📦 Hardware Requerido

- ESP32 Development Board
- Sensor MPU6050 (acelerómetro/giroscopio)
- Cables jumper
- Breadboard (opcional)

## 🔌 Conexiones

```
ESP32    <-->    MPU6050
GND      <-->    GND
3.3V     <-->    VCC  
GPIO21   <-->    SDA
GPIO22   <-->    SCL
```

## 🚀 Configuración Rápida

### 1. Verificar configuración básica del entorno:
- Arduino IDE instalado (2.x recomendado)
- ESP32 Arduino Core v2.0.2+ o v3.x
- Librerías instaladas (ver siguiente paso)

### 2. Instalar librerías:
```
Herramientas → Gestionar Bibliotecas → Instalar:
- PubSubClient (v2.8.0+)
- Adafruit MPU6050 (v2.0.0+)
- Adafruit Unified Sensor (v1.1.4+)
- ArduinoJson (v6.19.4+)
```

### 3. Configurar placa:
```
Herramientas → Placa → ESP32 Dev Module
- CPU Frequency: 240MHz
- Flash Size: 4MB
- Partition Scheme: Default 4MB with spiffs
- Upload Speed: 921600
```

### 4. Configurar WiFi y MQTT:
Copiar `credentials_example.h` como `credentials.h` y editar:
```cpp
const char* ssid = "TU_WIFI";
const char* password = "TU_PASSWORD";
const int sensorId = 1;  // Cambiar para múltiples sensores
```

## 📊 Datos MQTT

**Tópico de datos:** `GL_Ingenieros/sensores/vibracion`

**Formato JSON:**
```json
{
  "sensor_id": 1,
  "timestamp": "2024-01-15T10:30:45Z",
  "acceleration_x": -0.234,
  "acceleration_y": 9.821,
  "acceleration_z": 0.156
}
```

## 🚨 Solución de Problemas

 

### Sensor no detectado:
- ✅ Verificar conexiones I2C
- ✅ Comprobar alimentación 3.3V
- ✅ Revisar dirección I2C (0x68)

### Error de conexión WiFi:
- ✅ Verificar SSID y contraseña en `credentials.h`
- ✅ Comprobar señal WiFi
- ✅ Revisar configuración de red

### Error MQTT:
- ✅ Verificar broker: broker.hivemq.com:1883
- ✅ Comprobar conectividad a internet
- ✅ Revisar logs en Monitor Serial

## 📈 Monitoreo

- **Monitor Serial:** 115200 baudios
- **Datos cada:** 10 segundos (configurable)
- **Almacenamiento offline:** Hasta 50 registros
 

## 🔄 Comandos MQTT

**Tópico de comandos:** `GL_Ingenieros/sensores/comandos/[sensor_id]`

Comandos disponibles:
- `restart` - Reinicia el ESP32
- `status` - Publica estado en `GL_Ingenieros/status/[sensor_id]` con JSON:
  ```json
  {
    "sensor_id": 1,
    "uptime_ms": 123456,
    "wifi_connected": true,
    "rssi": -62,
    "ip": "192.168.1.50",
    "mqtt_connected": true,
    "offline_count": 0,
    "spiffs": true
  }
  ```

## ⚡ Prueba Rápida

1. **Verifica funcionamiento** en Monitor Serial
2. **Sube código principal:** `ESP32_Sensor.ino`
3. **Monitorea datos** en el cliente MQTT

## 🆘 Soporte

Si tienes problemas:
1. ✅ Verifica librerías instaladas y versión de ESP32 Core
2. ✅ Verifica conexiones de hardware
3. ✅ Revisa logs en Monitor Serial (115200 baudios)

---

**Desarrollado para GL Ingenieros**  
**Sistema PdM-Manager v2.0.0**