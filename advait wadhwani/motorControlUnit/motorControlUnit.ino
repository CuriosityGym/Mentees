#include <ESP8266WiFi.h>
#include <WiFiUDP.h>

unsigned int UDPPort = 4210;      // local port to listen on

char packetBuffer[255]; //buffer to hold incoming packet
char  ReplyBuffer[] = "acknowledged";       // a string to send back
WiFiUDP Udp;


const char* ssid = "Measuring Unit";
const char* password = "advait123";

String msg="";
int pwmValue =1023;
void setup() {
   pinMode(5, OUTPUT);
   pinMode(4, OUTPUT);
   pinMode(0, OUTPUT);
   pinMode(2, OUTPUT);
   Serial.begin(115200);
   WiFi.mode(WIFI_STA);
   WiFi.begin(ssid, password);
   Serial.println();
   Serial.print("Wait for WiFi");

    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: " + WiFi.localIP().toString());
  Udp.begin(UDPPort);
  Serial.println();
    Serial.println("Started ap. Local ip: " + WiFi.localIP().toString());

 
}

void loop() {
  // if there's data available, read a packet
  int packetSize = Udp.parsePacket();
  if (packetSize) {
   /* Serial.print("Received packet of size ");
    Serial.println(packetSize);
    Serial.print("From ");
    IPAddress remoteIp = Udp.remoteIP();
    Serial.print(remoteIp);
    Serial.print(", port ");
    Serial.println(Udp.remotePort());*/

    // read the packet into packetBufffer
    int len = Udp.read(packetBuffer, 255);
    if (len > 0) {
      packetBuffer[len] = 0;
    }
    msg = packetBuffer;
    Serial.println("Contents:");
    Serial.println(msg);
    // send a reply, to the IP address and port that sent us the packet we received
    //Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    //Udp.write(ReplyBuffer);
   // Udp.endPacket();
 
   if (msg == "1") {
         forward();
      }
      if (msg == "0") {
        stopMotor();
      }
  }

}


void stopMotor(void)
{
    analogWrite(5, 0);
   // analogWrite(4, 0);
}

 
void forward(void)
{
    analogWrite(5, pwmValue);
   // analogWrite(4, pwmValue);
    digitalWrite(0, HIGH);
   // digitalWrite(2, HIGH);
}
