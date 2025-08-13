// Test sketch para verificar configuración básica del ESP32
#include <WiFi.h>

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("=== TEST ESP32 CONFIGURATION ===");

  // Información básica de WiFi

  // Info básica de WiFi
  Serial.print("WiFi MAC Address: ");
  Serial.println(WiFi.macAddress());

  Serial.println("=== TEST COMPLETED ===");
}

void loop() {
  delay(5000);
  Serial.println("ESP32 funcionando correctamente!");
}

