#include <SPI.h>
#include "nRF24L01.h"
#include "RF24.h"
#define x_centre 485
#define y_centre 503
int joystick[2];
RF24 radio(7, 8);

unsigned long t0;
unsigned long t1;

void setup()
{
  //pinMode(13,OUTPUT);
  pinMode (1, OUTPUT);//M R
  pinMode (2, OUTPUT); //M R
  pinMode (3, OUTPUT); //M L
  pinMode (4, OUTPUT); //M L

  while (!Serial);
  Serial.begin(115200);

  radio.begin();
  radio.openReadingPipe(1, 0xF0F0F0F0A1LL);
  //radio.openReadingPipe(2, 0xF0F0F0F0A2LL);

  radio.startListening();
  t0 = 0;
}

byte pipeNum = 0; //variable to hold which reading pipe sent data
typedef struct Value {
  float x;
  float y;
  float z;
  int joystick_x_info;
  int joystick_y_info;
  int button_state_info;
} Value;
Value value;
void loop()
{
  

  if (radio.available(&pipeNum))
  {
    //char text[32] = {0};
    //int text[3];

    //radio.read(&text, sizeof(text));
    radio.read(&value, sizeof(value));
    //int coordinates[] ={value.x,value.y};
    Serial.print(t1);
    Serial.print("\t");
    Serial.print(value.x);
    Serial.print("\t");
    Serial.print(value.y);
    Serial.print("\t");
    Serial.print(value.z);
    Serial.print("\t");
    Serial.print(value.joystick_x_info);
    Serial.print("\t");
    Serial.print(value.joystick_y_info);
    Serial.print("\t");
    Serial.println(value.button_state_info);
    

   

    if (value.joystick_x_info < x_centre) {
      digitalWrite (1, LOW);
      digitalWrite (2, HIGH);
      digitalWrite (3, HIGH);
      digitalWrite (4, LOW);
      Serial.println( "LEFT");

    }
    else if (value.joystick_x_info > x_centre) {
      digitalWrite (1, HIGH);
      digitalWrite (2, LOW);
      digitalWrite (3, LOW);
      digitalWrite (4, HIGH);
      Serial.println( "Right");

    }
    else if (value.joystick_y_info > y_centre) {
      digitalWrite (1, HIGH);
      digitalWrite (2, LOW);
      digitalWrite (3, HIGH);
      digitalWrite (4, LOW);
      Serial.println( "Forward");
    }
    else if (value.joystick_y_info < y_centre) {
      digitalWrite (1, LOW);
      digitalWrite (2, HIGH);
      digitalWrite (3, LOW);
      digitalWrite (4, HIGH);
      Serial.println( "Back");
    }
    else {
      digitalWrite (1, LOW);
      digitalWrite (2, LOW);
      digitalWrite (3, LOW);
      digitalWrite (4, LOW);
    }
  }
  else
  {
    Serial.println("No radio available");
  }
}



