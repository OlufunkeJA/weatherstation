#include <rom/rtc.h> 
#include <math.h>  // https://www.tutorialspoint.com/c_standard_library/math_h.htm 
#include <ctype.h>

#ifndef _WIFI_H 
#include <WiFi.h>
#endif

#ifndef STDLIB_H
#include <stdlib.h>
#endif

#ifndef STDIO_H
#include <stdio.h>
#endif

#ifndef ARDUINO_H
#include <Arduino.h>
#endif 
 
#ifndef ARDUINOJSON_H
#include <ArduinoJson.h>
#endif

//Import Required Libraries
#include <DHT.h>
#include <Adafruit_ILI9341.h>
#include <Adafruit_BMP280.h>
#include <SPI.h>
#include "Adafruit_GFX.h"
#include <Wire.h>

//Declare Variables
#define dhtControl 25
#define dhtType DHT22

#define TFT_DC 17
#define TFT_CS 5
#define TFT_RST 16
#define TFT_CLK 18
#define TFT_MOSI 23
#define TFT_MISO 19

#define BMP_MOSI 21   //SDA 
#define BMP_MISO  33  //SDO 

#define csmControl 34

#define BOX_WIDTH 103
#define BOX_HEIGHT 70
#define SPACING 15
#define MARGIN 10

double h = 0.0;
double t = 0.0;
double p = 0.0;
double alt = 0.0;
double m = 0.0;

//Import Fonts for TFT
#include <Fonts/FreeSansBold18pt7b.h>
#include <Fonts/FreeSansBold9pt7b.h>
#include <Fonts/FreeSansBold12pt7b.h>

//MQTT Client Configuration
static const char *pubtopic = "620162688";                      // Add your ID number here
static const char *subtopic[] = {"620162688_sub", "/elet2415"}; // Array of Topics(Strings) to subscribe to
static const char *mqtt_server = "www.yanacreations.com";       // Broker IP address or Domain name as a String
static uint16_t mqtt_port = 1883;

/*const char *ssid = "Nijam2"; // Add your Wi-Fi ssid
const char *password = "diojao271104";      // Add your Wi-Fi password*/

const char *ssid = "MonaConnect"; // Add your Wi-Fi ssid
const char *password = "";      // Add your Wi-Fi password

/*const char *ssid = "DESKTOP-5OQ7KPH 7364";
const char *password = "88J]7v84";*/

//Task Handles
TaskHandle_t xMQTT_Connect = NULL;
TaskHandle_t xNTPHandle = NULL;
TaskHandle_t xLOOPHandle = NULL;
TaskHandle_t xUpdateHandle = NULL;
TaskHandle_t xButtonCheckeHandle = NULL;

//Function Declaration
void checkHEAP(const char* Name);   // RETURN REMAINING HEAP SIZE FOR A TASK
void initMQTT(void);                // CONFIG AND INITIALIZE MQTT PROTOCOL
unsigned long getTimeStamp(void);   // GET 10 DIGIT TIMESTAMP FOR CURRENT TIME
void callback(char* topic, byte* payload, unsigned int length);
void initialize(void);
bool publish(const char *topic, const char *payload); // PUBLISH MQTT MESSAGE(PAYLOAD) TO A TOPIC
void vUpdate( void * pvParameters );  
bool isNumber(double number);

#ifndef NTP_H
#include "NTP.h"
#endif

#ifndef MQTT_H
#include "mqtt.h"
#endif

double convert_Celsius_to_fahrenheit(double c);
double convert_fahrenheit_to_Celsius(double f);
double calcHeatIndex(double Temp, double Humid);
void displayTemp(double h,double t);
void displayPress(double p,double a);
void displayMoist(double s);

// Init class Instances for sensors and tft
DHT dht(dhtControl, dhtType); 
Adafruit_BMP280 bmp;
Adafruit_ILI9341 tft(TFT_CS, TFT_DC, TFT_MOSI, TFT_CLK, TFT_RST, TFT_MISO);

void setup(){
  Serial.begin(115200); // INIT SERIAL

  //Configure initialisations for senors & TFT
  dht.begin();
  bmp.begin(0x76);

  tft.begin();
  tft.fillScreen(ILI9341_WHITE);
  tft.setFont(&FreeSansBold9pt7b);
  tft.setTextColor(ILI9341_WHITE);
  
  //Configure IO pins
  pinMode(dhtControl, INPUT_PULLUP);

  initialize();           // INIT WIFI, MQTT & NTP
  //vButtonCheckFunction(); 
  vUpdateFunction();
}

void loop(){

  vTaskDelay(1000 / portTICK_PERIOD_MS);
}

void vUpdate( void * pvParameters )  {
    configASSERT( ( ( uint32_t ) pvParameters ) == 1 );    

    for( ;; ) {
          // #######################################################
          // ## This function must PUBLISH to topic every second. ##
          // #######################################################
          //Read DHT variables
          h = dht.readHumidity();
          t = dht.readTemperature();    

          //Read BMP variables
          p = bmp.readPressure()/100;
          alt = bmp.readAltitude(1013.25);

          //Read CSM variables
          //m = analogRead(csmControl);
          m = map(analogRead(csmControl),3450,1430,0,100);

          displayTemp(t,h);
          displayPress(p,alt);
          displayMoist(m);

          tft.setTextColor(ILI9341_PURPLE);
          tft.setCursor(33,tft.height() - 35);
          tft.setFont(&FreeSansBold9pt7b);
          tft.setTextSize(1);
          tft.print("Olufunke's Weather");
          tft.setCursor(88,tft.height() - 20);
          tft.print("Station");
          tft.setTextColor(ILI9341_WHITE);
 
          if(isNumber(t) and isNumber(p) and isNumber(alt) and isNumber(h) and isNumber(m)){
              // 1. Create JSon object
              JsonDocument doc;
              
              // 2. Create message buffer/array to store serialized JSON object
              char message[1100]  = {0};
              
              // 3. Add key:value pairs to JSon object based on above schema
              doc["id"] = "620162688";
              doc["timestamp"] = getTimeStamp();
              doc["temperature"] = t;
              doc["humidity"] = h;
              doc["heatindex"] = calcHeatIndex(t,h);
              doc["pressure"] = p;
              doc["altitude"] = alt;
              doc["moisture"] = m;

              // 4. Seralize / Convert JSon object to JSon string and store in message array
              serializeJson(doc, message);
               
              // 5. Publish message to a topic sobscribed to by both backend and frontend   
              if(mqtt.connected() ){
                publish(pubtopic, message);
              }       
          }   

          /*Serial.println("Humidity");
          Serial.println(h);
          Serial.println("Temp");
          Serial.println(t); 
          Serial.println("Heat Index");     
          Serial.println(calcHeatIndex(t,h));
          Serial.println("Pressure");
          Serial.println(p);
          Serial.println("Altitude");
          Serial.println(alt);
          Serial.println(bmp.readTemperature());*/

        vTaskDelay(1000 / portTICK_PERIOD_MS);  
    }
}

unsigned long getTimeStamp(void) {
          // RETURNS 10 DIGIT TIMESTAMP REPRESENTING CURRENT TIME
          time_t now;         
          time(&now); // Retrieve time[Timestamp] from system and save to &now variable
          return now;
}

void callback(char* topic, byte* payload, unsigned int length) {
  // ############## MQTT CALLBACK  ######################################
  // RUNS WHENEVER A MESSAGE IS RECEIVED ON A TOPIC SUBSCRIBED TO
  
  Serial.printf("\nMessage received : ( topic: %s ) \n",topic ); 
  char *received = new char[length + 1] {0}; 
  
  for (int i = 0; i < length; i++) { 
    received[i] = (char)payload[i];    
  }

  // PRINT RECEIVED MESSAGE
  Serial.printf("Payload : %s \n",received);
 
  // CONVERT MESSAGE TO JSON
  JsonDocument doc;
  DeserializationError error = deserializeJson(doc, received);  

  if (error) {
    Serial.print("deserializeJson() failed: ");
    Serial.println(error.c_str());
    return;
  }

  // PROCESS MESSAGE
  const char* type = doc["type"]; 

  if (strcmp(type, "controls") == 0){}
}

bool publish(const char *topic, const char *payload){   
     bool res = false;
     try{
        res = mqtt.publish(topic,payload);
        // Serial.printf("\nres : %d\n",res);
        if(!res){
          res = false;
          throw false;
        }
     }
     catch(...){
      Serial.printf("\nError (%d) >> Unable to publish message\n", res);
     }
  return res;
}

bool isNumber(double number){       
        char item[20];
        snprintf(item, sizeof(item), "%f\n", number);
        if( isdigit(item[0]) )
          return true;
        return false; 
} 

//DHT Functions
double convert_Celsius_to_fahrenheit(double c){
  return (c * 9/5) + 32;
}

double convert_fahrenheit_to_Celsius(double f){
  return (f - 32) * 5/9;
}

double calcHeatIndex(double temp, double Humid){
  double Temp = convert_Celsius_to_fahrenheit(temp);
  return convert_fahrenheit_to_Celsius(-42.379 + (2.04901523 * Temp) + (10.14333127 * Humid) + (-0.22475541 * Temp * Humid) + (-0.00683783 * Temp * Temp) + (-0.05481717 * Humid * Humid) + (0.00122874 * Temp * Temp * Humid) + (0.00085282 * Temp * Humid * Humid)  + (-0.00000199 * Temp * Temp * Humid * Humid));
}

//Complete Soil Moisture Sensor Functions

//TFT Functions
void displayTemp(double t, double h){
  // tft.height = 320
  //tft.width = 240

  tft.fillRoundRect(MARGIN,MARGIN, BOX_WIDTH, BOX_HEIGHT, 10, ILI9341_PURPLE);
  tft.setFont(&FreeSansBold9pt7b);
  tft.setCursor(MARGIN+5,30);
  tft.setTextSize(1);
  tft.print("Temp");
  tft.setCursor(MARGIN + 5, MARGIN + 55);
  tft.setFont(&FreeSansBold18pt7b);
  tft.setTextSize(1);
  tft.print(t);

  tft.fillRoundRect(MARGIN + BOX_WIDTH + SPACING, MARGIN, BOX_WIDTH, BOX_HEIGHT, 10, ILI9341_PURPLE);
  tft.setCursor(MARGIN + BOX_WIDTH + SPACING + 5, 30);
  tft.setFont(&FreeSansBold9pt7b);
  tft.setTextSize(1);
  tft.print("Humidity");
  tft.setCursor(MARGIN + BOX_WIDTH + SPACING + 5, MARGIN + 55);
  tft.setFont(&FreeSansBold18pt7b);
  tft.setTextSize(1);
  tft.print(h);

  tft.fillRoundRect(MARGIN, MARGIN + BOX_HEIGHT + SPACING, BOX_WIDTH, BOX_HEIGHT, 10, ILI9341_PURPLE);
  tft.setCursor(MARGIN + 5, 30 + BOX_HEIGHT + SPACING);
  tft.setFont(&FreeSansBold9pt7b);
  tft.setTextSize(1);
  tft.print("Heat Index");
  tft.setCursor(MARGIN+5, MARGIN + BOX_HEIGHT + SPACING + 55);
  tft.setFont(&FreeSansBold18pt7b);
  tft.setTextSize(1);
  tft.print(calcHeatIndex(t,h));
}

void displayPress(double press, double alt){
  tft.fillRoundRect(MARGIN + BOX_WIDTH + SPACING, MARGIN + BOX_HEIGHT + SPACING, BOX_WIDTH, BOX_HEIGHT, 10, ILI9341_PURPLE);
  tft.setCursor(MARGIN + BOX_WIDTH + SPACING + 5, 30 + BOX_HEIGHT + SPACING);
  tft.setFont(&FreeSansBold9pt7b);
  tft.setTextSize(1);
  tft.print("Pressure");
  tft.setCursor(MARGIN + BOX_WIDTH + SPACING + 5, MARGIN + 52 + SPACING + BOX_HEIGHT);
  tft.setFont(&FreeSansBold12pt7b);
  tft.setTextSize(1);
  tft.print(press);

  tft.fillRoundRect(MARGIN, MARGIN + BOX_HEIGHT + BOX_HEIGHT + SPACING + SPACING, BOX_WIDTH, BOX_HEIGHT, 10, ILI9341_PURPLE);
  tft.setCursor(MARGIN + 5, 30 + BOX_HEIGHT + BOX_HEIGHT + SPACING + SPACING);
  tft.setFont(&FreeSansBold9pt7b);
  tft.setTextSize(1);
  tft.print("Altitude");
  tft.setCursor(MARGIN + 5, MARGIN + BOX_HEIGHT + BOX_HEIGHT + SPACING + SPACING+ 52);
  tft.setFont(&FreeSansBold12pt7b);
  tft.setTextSize(1);
  tft.print(alt);
}

void displayMoist(double m){
  tft.fillRoundRect(MARGIN + BOX_WIDTH + SPACING, MARGIN + BOX_HEIGHT + SPACING + SPACING + BOX_HEIGHT, BOX_WIDTH, BOX_HEIGHT, 10, ILI9341_PURPLE);
  tft.setCursor(MARGIN + BOX_WIDTH + SPACING + 5, 30 + BOX_HEIGHT + SPACING + SPACING + BOX_HEIGHT);
  tft.setFont(&FreeSansBold9pt7b);
  tft.setTextSize(1);
  tft.print("Soil Moist.");
  tft.setCursor(MARGIN + BOX_WIDTH + SPACING + 5, MARGIN + 52 + SPACING + SPACING + BOX_HEIGHT + BOX_HEIGHT);
  tft.setFont(&FreeSansBold18pt7b);
  tft.setTextSize(1);
  tft.print(m);
}
