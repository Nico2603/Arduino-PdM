/**
 * Example credentials and configuration - copy this file as credentials.h
 */
#ifndef CREDENTIALS_H
#define CREDENTIALS_H

// WiFi configuration
const char* ssid = "TU_WIFI";                  // SSID WiFi
const char* password = "TU_PASSWORD";          // WiFi password

// MQTT configuration (public broker by default)
const char* mqttBrokerHost = "broker.hivemq.com";  // Public HiveMQ broker
const int mqttBrokerPort = 1883;                    // MQTT standard port
const char* mqttUser = "";                         // Empty for public broker
const char* mqttPassword = "";                     // Empty for public broker

// Sensor ID registered in backend/database
const int sensorId = 1;                             // Change for multiple sensors

// Timers configuration
const unsigned long sampleInterval = 10000;         // 10 seconds
const unsigned long connectionTimeout = 15000;      // 15 seconds WiFi connect timeout

#endif

