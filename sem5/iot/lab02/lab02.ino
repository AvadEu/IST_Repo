using namespace std;
// const int BUTTON_ON_OFF = 12;
// const int BUTTON_COLOR = 11;
// const int LED_RED = 10;
// const int LED_GREEN = 9;
// const int LED_BLUE = 8;

void setup() {
  // put your setup code here, to run once:
  pinMode(12, INPUT_PULLUP);
  pinMode(11, INPUT_PULLUP);
  pinMode(10, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(8, OUTPUT);
  Serial.begin(9600);
}
// bool lightOn = false;
// int colorPossition = 0;
// int colorBrightness = 0;
int colorRedBrightness = 255;
int colorGreenBrightness = 0;
int colorBlueBrightness = 0;
int colorChange = 0;

void loop() {
  //put your main code here, to run repeatedly:
  // if (digitalRead(12) == LOW) {
  //   lightOn = !lightOn;
  //   delay(300);
  // }

  // if (lightOn && digitalRead(11) == LOW) {
  //   colorPossition = (colorPossition + 1) % 3;
  //   delay(300);
  // }

  // if(lightOn){
  //   switch (colorPossition){
  //     // RED
  //     case 0:
  //       digitalWrite(10, HIGH);
  //       digitalWrite(9, LOW);
  //       digitalWrite(8, LOW);
  //       break;
  //     // GREEN
  //     case 1:
  //       digitalWrite(10, LOW);
  //       digitalWrite(9, HIGH);
  //       digitalWrite(8, LOW);
  //       break;
  //     //BLUE
  //     case 2:
  //       digitalWrite(10, LOW);
  //       digitalWrite(9, LOW);
  //       digitalWrite(8, HIGH);
  //       break;
  //   }
  // }

// analogWrite(10, colorBrightness);

// if (digitalRead(12) == LOW){
//   if(colorBrightness < 255) colorBrightness +=1;
//   delay(5);
//   Serial.println(colorBrightness);
// }

// if (digitalRead(11) == LOW){
//   if(colorBrightness > 0) colorBrightness -=1;
//   delay(5);
//   Serial.println(colorBrightness);
// }
  analogWrite(10, colorRedBrightness);
  analogWrite(9, colorGreenBrightness);
  analogWrite(8, colorBlueBrightness);


   switch (colorChange){
      // RED
      case 0:
        colorRedBrightness -= 1;
        colorGreenBrightness +=1;
        delay(5);
        break;
      // GREEN
      case 1:
        colorGreenBrightness -= 1;
        colorBlueBrightness +=1;
        delay(5);
        break;
      //BLUE
      case 2:
        colorBlueBrightness -= 1;
        colorRedBrightness +=1;
        delay(5);
        break;
    }
  
  if(colorRedBrightness == 255 || colorGreenBrightness == 255 || colorBlueBrightness == 255) colorChange = (colorChange + 1) % 3;
}
