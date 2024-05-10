El **factor 30-30-30** es una regla utilizada en el manejo de incendios forestales para identificar condiciones críticas que podrían llevar a incendios extremadamente peligrosos y de rápida propagación. Esta regla es una herramienta sencilla que ayuda a los bomberos y gestores de emergencias a evaluar el riesgo de incendios de forma rápida y efectiva.

### Descripción del Factor 30-30-30

El factor 30-30-30 se refiere a tres condiciones meteorológicas específicas:
1. **Temperatura superior a 30°C**: Altas temperaturas pueden contribuir significativamente a la desecación de la vegetación, haciéndola más inflamable.
2. **Humedad relativa inferior al 30%**: Baja humedad relativa también implica condiciones más secas, lo que favorece la ignición y la propagación del fuego.
3. **Vientos superiores a 30 km/h**: Los vientos fuertes pueden llevar rápidamente las llamas a nuevas áreas, aumentando la velocidad de propagación del incendio.

Cuando estas tres condiciones se cumplen simultáneamente, el riesgo de que se produzcan incendios forestales peligrosos aumenta drásticamente. Esta regla proporciona un método rápido para identificar días de alto riesgo sin necesidad de análisis complicados o tecnología avanzada.

### Uso del Factor 30-30-30

El factor 30-30-30 es especialmente útil para los siguientes propósitos:
- **Alerta rápida**: Permite a los responsables de la gestión de incendios identificar rápidamente las condiciones potencialmente peligrosas y tomar medidas preventivas.
- **Movilización de recursos**: Facilita la decisión de cuándo y dónde movilizar recursos adicionales para la lucha contra incendios, como aviones de extinción de incendios, equipos terrestres y voluntarios.
- **Planificación y preparación de la comunidad**: Ayuda a las comunidades a prepararse para posibles evacuaciones y otras medidas de seguridad en días de alto riesgo.


# Proyecto de Estación Meteorológica con Arduino

## Descripción
Este proyecto implementa una estación meteorológica utilizando un microcontrolador ESP32 como cliente y un servidor que recibe y procesa datos ambientales. El sistema mide temperatura, humedad y velocidad del viento utilizando un sensor AHT10 y un anemómetro Adafruit. Los datos se envían a un servidor donde pueden ser almacenados y analizados.

## Componentes Hardware
- **ESP32**: Controla los sensores y maneja la comunicación con el servidor.
- **Sensor AHT10**: Sensor de temperatura y humedad.
- **Anemómetro**: Mide la velocidad del viento.
- **Cables y conexiones**: Para conectar los sensores al ESP32.

## Configuración del Hardware
1. Conectar el sensor AHT10 al ESP32:
   - **Vcc** a 3.3V del ESP32.
   - **GND** a GND del ESP32.
   - **SDA** a pin 21 del ESP32.
   - **SCL** a pin 22 del ESP32.
2. Conectar el anemómetro al ESP32:
   - **Cable negro** a GND.
   - **Cable marrón** a una fuente de alimentación externa de 7-24V.
   - **Cable azul** al pin 34 del ESP32 (ADC).

## Software y Librerías
Utilice las siguientes librerías en el entorno de desarrollo de Arduino:
- `WiFi.h`: para la conectividad WiFi.
- `HTTPClient.h`: para hacer solicitudes HTTP.
- `ArduinoJson.h`: para manipular JSON.
- `Wire.h` y `AHT10.h`: para interactuar con el sensor AHT10.

### Nodos
El código principal para el ESP32 maneja la lectura de los sensores y la comunicación con el servidor. Este envia mediante post al servidor los datos (UUDI,temperatura, humedad, y velocidad el viento) con un intervalo de 5 segundos, para garantizar la captura de datos en tiempo real.

## Servidor
El servidor principal actua como puente entre los nodos y el servidor cloud. Se encarga de verificar que el formato de datos este correcto y los reenvia al servidor cloud. Esto sirve para que los nodos se conecten a este, en formato estrella y asi disminuir las conexiones al cloud.

## Servidor Cloud
Es el encargado de recibir los datos y almacenarlos en la base de datos, montada en posgresql. Luego de almacenar los datos, mediante procesos automaticos y segun los datos actuales, se realiza una prediccion de los cambios que pueden ocurrir en estos, como aumento de temperatura, baja de humedad, etc. Y en base a ciertas categorizaciones de esta prediccion, se dara la alerta de un posible incendio forestal. Esto se hara tanto de forma global (Agrupando los datos de todos los nodos, a forma general de la zona), como por nodo (Riesgo en un punto especifico). Este podra mandar tambien una alerta a personas previamente definidas para alertar el riesgo de incendio de forma automatica

## Servidor Web
Se alimenta de los datos guardados en el servidor cloud. Este permitira ver los datos capturados en tiempo real, como graficos de los datos, mapas con las ubicaciones de los nodos, lugares con riesgo de incendio, etc.
