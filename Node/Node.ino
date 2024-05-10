#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h> // Incluye la biblioteca ArduinoJson
#include <Wire.h>
#include <AHT10.h>

// Reemplaza con los detalles de tu red WiFi
const char* ssid = "705 2,4G";
const char* password = "12345679";

AHT10 myAHT10(AHT10_ADDRESS_0X38);

// Reemplaza con la URL de tu servidor donde enviarás los datos
const String serverUrl = "http://192.168.1.115/receive_data";

void setup() {
  Wire.begin();
  Serial.begin(9600);
  
  // Inicia y espera por la conexión WiFi
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
  HTTPClient http; // Mueve el objeto HTTPClient aquí para que se reinicie en cada ciclo
  // Lee los valores del sensor AHT10
  float temp = myAHT10.readTemperature();
  float hum = myAHT10.readHumidity();
  int viento = 10; // Valor por defecto del viento en km/h
  int risk = 0;

  // Preparar los datos en formato JSON
  DynamicJsonDocument doc(256);
  doc["uuid"] = 1;
  doc["temperature"] = temp;
  doc["humidity"] = hum;
  doc["wind_speed"] = viento;
  String jsonData;
  serializeJson(doc, jsonData);

  // Configura los headers para enviar JSON
  http.begin(serverUrl); // Especifica la URL del request
  http.addHeader("Content-Type", "application/json");

  Serial.println("Data Sent");

  int httpCode = http.POST(jsonData); // Envía la petición POST

  if (httpCode > 0) { // Verifica si la respuesta ha sido recibida correctamente
    String payload = http.getString(); // Obtiene la respuesta
    Serial.println("Data received successfully from server");
    Serial.println("********************");
  } else {
    Serial.print("Error on sending POST: ");
    Serial.println(http.errorToString(httpCode).c_str());
  }

  http.end(); // Cierra la conexión
  
  delay(5000); // Espera 5 segundos antes de enviar los datos nuevamente
}
