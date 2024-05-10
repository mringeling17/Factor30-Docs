#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>

const char* ssid = "705 2,4G";
const char* password = "12345679";

// La URL del servidor al cual reenviar los datos recibidos
const char* serverUrl = "http://192.168.1.118:5000/receive_data";
const char* errorUrl = "http://192.168.1.118:5000/error"; // Endpoint para enviar errores

WebServer server(80);

void setup() {
  Serial.begin(9600);
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConectado a WiFi. Dirección IP: ");
  Serial.println(WiFi.localIP());

  server.on("/receive_data", HTTP_POST, []() {
    if (!server.hasArg("plain")) {
      server.send(200, "text/plain", "Error: No se recibieron datos");
      return;
    }

    HTTPClient http;
    
    String payload = server.arg("plain");
    DynamicJsonDocument doc(1024);
    deserializeJson(doc, payload);

    // Asignando valores
    int temperature = doc["temperature"];
    int humidity = doc["humidity"];
    int wind_speed = doc["wind_speed"];
    String uuid = doc["uuid"]; // Asegúrate de que el UUID se envíe en los datos

    // Verificando errores
    String errorFields = "";
    if (temperature == 255) errorFields += "temperature ";
    if (humidity == 255) errorFields += "humidity ";
    if (wind_speed == 255) errorFields += "wind_speed ";

    if (errorFields.length() > 0) {
      http.begin(errorUrl);
      http.addHeader("Content-Type", "application/json");
      String errorMsg = "{\"uuid\":\"" + uuid + "\", \"error_fields\":\"" + errorFields.trim() + "\"}";
      http.POST(errorMsg);
      http.end(); // Cierre después del envío de error
    }

    // Envío de datos al servidor
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");
    Serial.println("Sending payload: " + payload); // Debugging output
    int httpCode = http.POST(payload);
    Serial.println("HTTP Code: " + String(httpCode)); // Debugging output

    if (httpCode > 0) {
      String response = http.getString();
      Serial.println("Response: " + response); // Debugging output
    } else {
      Serial.println("Failed to receive response");
    }
    
    http.end();
    server.send(200, "text/plain", "Datos reenviados correctamente");
    Serial.println("****************************************");
  });

  server.begin();
}

void loop() {
  server.handleClient();
}
