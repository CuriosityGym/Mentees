#include <ESP8266WiFi.h>
#include <WiFiUDP.h>

unsigned int UDPPortRemote = 4210;      // local port to listen on
unsigned int UDPPortLocal = 2392;      // local port to listen on

char packetBuffer[255]; //buffer to hold incoming packet
char  replyBuffer[] = "acknowledged";       // a string to send back
String value="";
WiFiUDP Udp;

const char* ssid = "Measuring Unit";
const char* password = "advait123";

int trigPin = 15;
int echoPin = 13;
long duration;
int distance;
String msg = "";
int limit = 75;

int maxheight= 6;
int minheight= 18;
int finalMaxHeight = 15;
int finalMinHeight = 6;
int delaytime= 3000;
int interval= 1000;
int motorStop=false;

void setup() {
    pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
    pinMode(echoPin, INPUT); // Sets the echoPin as an Input

    Serial.begin(115200);

      WiFi.mode(WIFI_AP);
  WiFi.softAP(ssid, password);
  /*
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    Serial.println();
    Serial.print("Wait for WiFi");

    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }*/
    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: " + WiFi.localIP().toString());

    Udp.begin(UDPPortLocal);

    Udp.beginPacket("192.168.4.2", UDPPortRemote);//send ip to server
    char ipBuffer[255];
    WiFi.localIP().toString().toCharArray(ipBuffer, 255);
    Udp.write(ipBuffer);
    Udp.endPacket();
    Serial.println("Sent ip adress to server");
    }

void loop() {

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // put your main code here, to run repeatedly:
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance= duration*0.0346/2;
  // Prints the distance on the Serial Monitor
  Serial.print("Distance: ");
  Serial.println(distance);
  Serial.print("maxheight ");
  Serial.println(maxheight);
  // if there's data available, read a packet
  int packetSize = Udp.parsePacket();
  if (packetSize) {
    Serial.print("Received packet of size ");
    Serial.println(packetSize);
    Serial.print("From ");
    IPAddress remoteIp = Udp.remoteIP();
    Serial.print(remoteIp);
    Serial.print(", port ");
    Serial.println(Udp.remotePort());

    // read the packet into packetBufffer
    int len = Udp.read(packetBuffer, 255);
    if (len > 0) {
      packetBuffer[len] = 0;
    }
    Serial.print("Contents:");
    Serial.println(packetBuffer);
    msg = packetBuffer;
    if (msg.startsWith("max")) {
       String maxHeight = msg.substring(3);
       finalMaxHeight = maxHeight.toInt();
       Serial.print("max height:");
       Serial.println(finalMaxHeight);
    }
    if (msg.startsWith("min")) {
       String minHeight = msg.substring(3);
       finalMinHeight = minHeight.toInt();
       Serial.print("min height:");
       Serial.println(finalMinHeight);
    }
    if (msg.startsWith("del")) {
       String delayTime = msg.substring(3);
       delaytime = delayTime.toInt();
       Serial.print("delay time:");
       Serial.println(delaytime);
    }
    if (msg.startsWith("int")) {
       String intravalTime = msg.substring(3);
       interval = intravalTime.toInt();
       Serial.print("interval:");
       Serial.println(interval);
    }
    //String dBlimit = msg.substring(2);
    //limit = dBlimit.toInt();
  }

    if (distance<=maxheight){
    value = "0";
    Udp.beginPacket("192.168.4.2", UDPPortRemote);
    char ipBuffer[255];
    value.toCharArray(ipBuffer, 255);
    Udp.write(ipBuffer);
    Udp.endPacket();
    Serial.print("Motor off");
    delay(delaytime);
    motorStop=true;
    minheight=finalMaxHeight;
    }
  if(motorStop==true && distance>(maxheight+2) && distance<minheight){
    maxheight=(maxheight+2);
    value = "0";
    Udp.beginPacket("192.168.4.2", UDPPortRemote);
    char ipBuffer[255];
    value.toCharArray(ipBuffer, 255);
    Udp.write(ipBuffer);
    Udp.endPacket();
    Serial.print("Motor off");
    delay(delaytime);
  }
  
  if (distance>=minheight){
    //digitalWrite(led,HIGH);
    value = "1";
    Udp.beginPacket("192.168.4.2", UDPPortRemote);
    char ipBuffer[255];
    value.toCharArray(ipBuffer, 255);
    Udp.write(ipBuffer);
    Udp.endPacket();
    Serial.print("Motor on");
    delay(delaytime);
    motorStop=false;
    maxheight=finalMinHeight;
  }
  
  
  if(motorStop==false && distance<(minheight-2) && distance>maxheight){
    minheight=(minheight-2);
    value = "1";
    Udp.beginPacket("192.168.4.2", UDPPortRemote);
    char ipBuffer[255];
    value.toCharArray(ipBuffer, 255);
    Udp.write(ipBuffer);
    Udp.endPacket();
    Serial.print("Motor on");
    delay(delaytime);
  }
  //Serial.println("Sent ip adress to server");

}

 
