#include <WiFi.h>
#include <HTTPClient.h>
#include <SoftwareSerial.h>
#include "config.h"  // defines WIFI_SSID, WIFI_PASSWORD and SERVER_HOST
// Simple firmware that collects sensor data from the PIR sensor, vibration
// detector and accelerometer. Readings are periodically sent to the web
// server defined in `serverName`. The board also controls a buzzer that
// sounds when strong vibrations are detected.

//#include <TinyGPS.h>
//SoftwareSerial gpsSerial(32,35);//rx,tx
//TinyGPS gps; // create gps object
int ax,ay,az;
String latitude = "32.8755662";
String longitude = "-117.2323252"; 
const int buzzerPin = 19;
const int pirPin = 4;
const int vibPin = 18;
const int axPin = 2;
const int ayPin = 12;
const int azPin = 15;

int vibReadings[10] = {0,0,0,0,0,0,0,0,0,0};
int i = 0;
int changesVib[9] = {0,0,0,0,0,0,0,0,0};

unsigned long timeStart = 0;
int pir = 0;
int vib = 0;

const char* ssid = WIFI_SSID;
const char* password = WIFI_PASSWORD;

String esp32_username = "myesp32_1234";
String esp32_password = "thisisanesp32";

//Your Domain name with URL path or IP address with path
String serverName = String("http://") + SERVER_HOST + "/unlock/" + esp32_username + "/" + esp32_password + "/";


// the following variables are unsigned longs because the time, measured in
// milliseconds, will quickly become a bigger number than can be stored in an int.
unsigned long lastTime = 0;
unsigned long timerDelay = 5000;



void setup() {
  pinMode(buzzerPin,OUTPUT);
  pinMode(pirPin,INPUT);
  pinMode(vibPin,INPUT);
  setupAccelSensor();
//  setupGPSSensor();
  Serial.begin(115200); 

  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
 
  Serial.println("Timer set to 5 seconds (timerDelay variable), it will take 5 seconds before publishing the first reading.");

}

void loop() {

  //readGPSData();
  readAccelSensor();
  pir = digitalRead(pirPin);
  vib = !digitalRead(vibPin);
   vibReadings[i] = vib;
    changesVib[i] = abs(vibReadings[i+1]-vibReadings[i]);
    i++;
    if (i == 10) {i = 0;}

    int sum = 0;
    for(int j = 0; j < 9; j++) {
      sum += changesVib[j];
    }

  Serial.println("!!! Sum:  " + String(sum));
  readAccelSensor();
  Serial.println(String(ax));
  String serverName2 =  String("http://") + SERVER_HOST + "/send_data/" + esp32_username + "/" + esp32_password + "/" + String(pir) + "/" + String(sum) + "/" + String(ax) +  "/" + String(ay) +  "/" + String(az) + "/" + latitude + "/" + longitude + "/";
  Serial.println(serverName2);
  delay(50);
  if(sum > 3) {
    digitalWrite(buzzerPin, HIGH);
  }
  else {
    digitalWrite(buzzerPin,LOW);
  }

  if ((millis() - lastTime) > timerDelay) {
    //Check WiFi connection status
    if(WiFi.status()== WL_CONNECTED){
      HTTPClient http;

//      String serverPath = serverName;
//      
//      // Your Domain name with URL path or IP address with path
//      http.begin(serverPath.c_str());
//      
//      // Send HTTP GET request
//      int httpResponseCode = http.GET();
//      
//      if (httpResponseCode>0) {
//        Serial.print("HTTP Response code: ");
//        Serial.println(httpResponseCode);
//        String payload = http.getString();
//        Serial.println(payload);
//      }
//      else {
//        Serial.print("Error code: ");
//        Serial.println(httpResponseCode);
//      }

      String serverPath = serverName2;
      
      // Your Domain name with URL path or IP address with path
      http.begin(serverPath.c_str());

       pir = digitalRead(pirPin);
  vib = !digitalRead(vibPin);
   vibReadings[i] = vib;
    changesVib[i] = abs(vibReadings[i+1]-vibReadings[i]);
    i++;
    if (i == 10) {i = 0;}

    sum = 0;
    for(int j = 0; j < 9; j++) {
      sum += changesVib[j];
    }

    if(sum > 3) {
    digitalWrite(buzzerPin, HIGH);
  }
  else {
    digitalWrite(buzzerPin,LOW);
  }

      
      // Send HTTP GET request
      int httpResponseCode = http.GET();

       pir = digitalRead(pirPin);
  vib = !digitalRead(vibPin);
   vibReadings[i] = vib;
    changesVib[i] = abs(vibReadings[i+1]-vibReadings[i]);
    i++;
    if (i == 10) {i = 0;}

    sum = 0;
    for(int j = 0; j < 9; j++) {
      sum += changesVib[j];
    }

    if(sum > 3) {
    digitalWrite(buzzerPin, HIGH);
  }
  else {
    digitalWrite(buzzerPin,LOW);
  }

      
      if (httpResponseCode>0) {
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);
        String payload = http.getString();
        Serial.println(payload);
      }
      else {
        Serial.print("Error code: ");
        Serial.println(httpResponseCode);
      }

      
      // Free resources
      http.end();
    }
    else {
      Serial.println("WiFi Disconnected");
    }
    lastTime = millis();
  }
}


void setupAccelSensor(void) {
  pinMode(axPin,INPUT);
  pinMode(ayPin,INPUT);
  pinMode(azPin,INPUT);
}


void readAccelSensor(void) {
  ax = analogRead(axPin);
  ay = analogRead(ayPin);
  az = analogRead(azPin);
}

//
//void setupGPSSensor(void) {
//  gpsSerial.begin(9600); // connect gps sensor
//}
//
//void readGPSData(void) {
//  float lat = 0.0,lon = 0.0; 
//  while(gpsSerial.available()){ // check for gps data
//    if(gps.encode(gpsSerial.read())) { 
//    gps.f_get_position(&lat,&lon); // get latitude and longitude
//   }
//  }
//
// latitude = String(lat,6);
// longitude = String(lon,6);
// Serial.println(latitude);
// Serial.println(longitude);
//}
