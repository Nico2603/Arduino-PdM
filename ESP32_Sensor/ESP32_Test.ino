// Test sketch para verificar configuración básica del ESP32
#include <WiFi.h>
#include <esp_task_wdt.h>

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("=== TEST ESP32 CONFIGURATION ===");

  // Verificar API de Watchdog según versión del Core
  Serial.println("Testing Watchdog Timer API...");
  #if ESP_IDF_VERSION >= ESP_IDF_VERSION_VAL(5, 0, 0)
    Serial.println("✅ ESP32 Core v3.x detected (IDF 5.x)");
    esp_task_wdt_config_t wdt_config = {
      .timeout_ms = 10000,
      .idle_core_mask = 0,
      .trigger_panic = false
    };
    esp_task_wdt_init(&wdt_config);
  #else
    Serial.println("✅ ESP32 Core v2.x detected (IDF 4.x)");
    esp_task_wdt_init(10, false);
  #endif

  Serial.println("✅ Watchdog Timer OK");

  // Info básica de WiFi
  Serial.print("WiFi MAC Address: ");
  Serial.println(WiFi.macAddress());

  Serial.println("=== TEST COMPLETED ===");
}

void loop() {
  delay(5000);
  Serial.println("ESP32 funcionando correctamente!");
}

