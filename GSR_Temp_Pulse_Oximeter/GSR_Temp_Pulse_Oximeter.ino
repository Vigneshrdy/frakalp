
#include "MAX30105.h"               // MAX30102 Library

#include <Wire.h>
#include "DHT.h"
#define DHTPIN 8     
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);
 #include <LiquidCrystal_I2C.h>
int x=0;
LiquidCrystal_I2C lcd(0x27, 16, 2);
MAX30102 Sensor
MAX30105 particleSensor;

// Heart Rate Variables
long irValue, redValue;

int sensorValue;


double T,P,p0,a;

int e=0;
int b=0;
int c=0;
int d=0;


void setup() {

Serial.begin(9600);
  dht.begin();
// Initialize MAX30102 Sensor
  if (!particleSensor.begin(Wire, I2C_SPEED_STANDARD)) {
    Serial.println("MAX30102 not found. Check connections.");
    while (true); // Stop if sensor fails
  }

  particleSensor.setup(); // Configure MAX30102
  pinMode(8, INPUT);
  pinMode(7, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(A0, INPUT);
  digitalWrite(7, HIGH);
  digitalWrite(11, LOW);
lcd.init(); // initialize the lcd
lcd.backlight();
lcd.setCursor(0,0);
  lcd.print("Health parameters");
  lcd.setCursor(0,1);
  lcd.print("Monitor System");
  delay(2000);
  lcd.clear();

}

 

void loop() {

float conductivevoltage;
sensorValue=analogRead(A3);
conductivevoltage = sensorValue*(5.0/1023.0);
//sensorValue=(1024-sensorValue);
sensorValue=sensorValue/2;
//Serial.print("sensorValue=");
//Serial.print(sensorValue);
//Serial.println("uS");
lcd.setCursor(0,0);
lcd.print("GSR=");
lcd.print(sensorValue);
lcd.print(" uS    ");
if(sensorValue>=600)
{
  lcd.setCursor(0,0);
lcd.print("GSR=NF");
Serial.println("GSR=NF");
lcd.print("  ");
}
if(sensorValue<600)
{
lcd.setCursor(0,0);
lcd.print("GSR=");
//Serial.print("GSR=");
//Serial.print(sensorValue);
lcd.print(sensorValue);
lcd.print(" uS    ");
//Serial.println(" uS    ");
}
/*float h = dht.readHumidity();
  int t = dht.readTemperature();
  float f = dht.readTemperature(true);
  float hif = dht.computeHeatIndex(f, h);
  float hic = dht.computeHeatIndex(t, h, false);
 lcd.setCursor(0, 0);
  lcd.print("Temp:");
 lcd.print(f);
 lcd.print((char)223);
 lcd.print("F  ");*/

 irValue = particleSensor.getIR();
  redValue = particleSensor.getRed();
/*lcd.setCursor(0, 1);
  lcd.print("Pulse:");
 lcd.print(irValue/1100);
 lcd.print(" ");
Serial.print("Pulse:");
 Serial.println(irValue/1100);
 lcd.print(" ");
 lcd.setCursor(9, 1);
  lcd.print("O2:");
 lcd.print(redValue/680);
 lcd.print("%");
 Serial.print("O2:");
 Serial.print(redValue/680);
 Serial.println("%");
 Serial.println("");
 lcd.print("     ");

/*if(f>100)
{
  digitalWrite(11, HIGH);
  digitalWrite(7, LOW);
  lcd.setCursor(0, 1);
  lcd.print("High Temperature...   ");
  delay(500);
  digitalWrite(7, HIGH);
  digitalWrite(11, LOW);
    //delay(500);

}*/
if(sensorValue<=10)
{
    Serial.println("Place fingers...            "); 

}
if(sensorValue>10)
{
  for(x=0;x<=15;x++)
  {
sensorValue=analogRead(A3);
conductivevoltage = sensorValue*(5.0/1023.0);
//sensorValue=(1024-sensorValue);
sensorValue=sensorValue/2;
irValue = particleSensor.getIR();
  redValue = particleSensor.getRed();
lcd.setCursor(0, 1);
  lcd.print("Pulse:");
 lcd.print(irValue/1100);
 lcd.print(" ");
//Serial.print("Pulse:");
 //Serial.println(irValue/1100);
 lcd.print(" ");
 lcd.setCursor(9, 1);
  lcd.print("O2:");
 lcd.print(redValue/680);
 lcd.print("%");
 //Serial.print("O2:");
 //Serial.print(redValue/680);
 //Serial.println("%");
 //Serial.println("");
 lcd.print("     ");

delay(1000);
  }
  x=0;
  Serial.print("GSR=");
Serial.print(sensorValue);
lcd.print(sensorValue);
lcd.print(" uS    ");
Serial.println(" uS    ");
if(sensorValue>10 && sensorValue<=100)
{
   lcd.setCursor(0, 1);
  lcd.print("Low Stress            "); 
  Serial.println("Low Stress            "); 

  }
  if(sensorValue>100 && sensorValue<=200)
{
   lcd.setCursor(0, 1);
  lcd.print("Moderate stress    ");  
  Serial.println("Moderate stress    ");  

  }
  if(sensorValue>200 && sensorValue<600)
{
   lcd.setCursor(0, 1);
  lcd.print("High stress        "); 
  Serial.println("High stress        "); 

  }
  irValue = particleSensor.getIR();
  redValue = particleSensor.getRed();
  lcd.setCursor(0, 1);
  lcd.print("Pulse:");
 lcd.print(irValue/1100);
 lcd.print(" ");
Serial.print("Pulse:");
 Serial.println(irValue/1100);
 lcd.print(" ");
 lcd.setCursor(9, 1);
  lcd.print("O2:");
 lcd.print(redValue/680);
 lcd.print("%");
 Serial.print("O2:");
 Serial.print(redValue/680);
 Serial.println("%");
 Serial.println("");
 lcd.print("     ");
while(1);

}

 delay(2000);
 lcd.clear();
}