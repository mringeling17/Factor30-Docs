#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <AHT10.h>

const char* ssid = "705 2,4G";
const char* password = "12345679";

AHT10 myAHT10(AHT10_ADDRESS_0X38);
const String serverUrl = "http://192.168.1.115/receive_data";

const int anemometerPin = 34; // Pin donde se conecta el anemómetro

void setup() {
  Wire.begin();
  Serial.begin(9600);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi conectado");
  Serial.print("Dirección IP: ");
  Serial.println(WiFi.localIP());

  if (!myAHT10.begin()) {
    Serial.println("No se pudo encontrar el sensor AHT10. ¡Comprueba las conexiones!");
    while (1);
  }
  Serial.println("Sensor AHT10 iniciado correctamente.");
}

void loop() {
  HTTPClient http;
  float temp = myAHT10.readTemperature();
  float hum = myAHT10.readHumidity();

  // Leer la señal analógica del anemómetro
  int analogValue = analogRead(anemometerPin);
  float voltage = analogValue * (3.3 / 4095.0); // Convertir de lectura ADC a voltaje
  float windSpeed = ((voltage - 0.4) * 32.4) / 1.6; // Convertir voltaje a velocidad del viento en m/s

  DynamicJsonDocument doc(256);
  doc["uuid"] = 1;
  doc["temperature"] = temp;
  doc["humidity"] = hum;
  doc["wind_speed"] = windSpeed;
  doc["risk_level"] = 0;
  String jsonData;
  serializeJson(doc, jsonData);

  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");
  Serial.println("Data Sent");

  int httpCode = http.POST(jsonData);

  if (httpCode > 0) {
    String payload = http.getString();
    Serial.println("Data received successfully from server");
    Serial.println("********************");
  } else {
    Serial.print("Error on sending POST: ");
    Serial.println(http.errorToString(httpCode).c_str());
  }

  http.end();
  delay(5000);
}
