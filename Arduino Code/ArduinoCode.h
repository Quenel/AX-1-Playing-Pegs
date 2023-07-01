#include <Servo.h>

Servo servo1; // create servo object to control a servo
Servo servo2; // twelve servo objects can be created on most boards
Servo servo3;
Servo servo4;

void setup()
{
    servo1.attach(5); // attaches the servo on pin 4 to the servo object
    servo2.attach(4);
    servo3.attach(6);
    servo4.attach(7);

    Serial.begin(9600); // open serial communication
}

void loop()
{
    if (Serial.available())
    {
        String input = Serial.readStringUntil('\n');                          // read the serial input until a new line
        int firstComma = input.indexOf(',');                                  // find the position of the first comma
        int secondComma = input.indexOf(',', firstComma + 1);                 // find the position of the second comma
        int thirdComma = input.indexOf(',', secondComma + 1);                 // find the position of the third comma
        int servo1Pos = input.substring(0, firstComma).toInt();               // read the servo position from the first value
        int servo2Pos = input.substring(firstComma + 1, secondComma).toInt(); // read the servo position from the second value
        int servo3Pos = input.substring(secondComma + 1, thirdComma).toInt(); // read the servo position from the third value
        int servo4Pos = input.substring(thirdComma + 1).toInt();              // read the servo position from the fourth value
        servo1.write(servo1Pos);                                              // move servo 1 to the position
        servo2.write(servo2Pos);                                              // move servo 2 to the position
        servo3.write(servo3Pos);                                              // move servo 3 to the position
        servo4.write(servo4Pos);                                              // move servo 4 to the position
    }
}