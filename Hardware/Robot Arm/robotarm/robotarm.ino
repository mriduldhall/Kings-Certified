#include <Servo.h>
#include <LinkedList.h>


struct Move {
  float servoOneState;
  float servoTwoState;
  float servoThreeState;
  float servoFourState;
  float servoFiveState;
  float servoSixState;

  Move (float ServoOneState, float ServoTwoState, float ServoThreeState, float ServoFourState, float ServoFiveState, float ServoSixState) {
    servoOneState = ServoOneState;
    servoTwoState = ServoTwoState;
    servoThreeState = ServoThreeState;
    servoFourState = ServoFourState;
    servoFiveState = ServoFiveState;
    servoSixState = ServoSixState;
  }
};

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;
Servo servo6;

LinkedList<Move*> moves;

void setup() {
  Serial.begin(9600);

  servo1.attach(9);
  servo2.attach(10);
  servo3.attach(11);
  servo4.attach(12);
  servo5.attach(7);
  servo6.attach(6);

}

void loop() {
  ManageInputs();
  if (moves.size() != 0) {
    MoveArm(moves.remove(0));
  }
}

void ManageInputs() {
  
  if (Serial.available() > 0) {
    float servo1 = Serial.parseFloat();
    float servo2 = Serial.parseFloat();
    float servo3 = Serial.parseFloat();
    float servo4 = Serial.parseFloat();
    float servo5 = Serial.parseFloat();
    float servo6 = Serial.parseFloat();
    Serial.read();
    
    Move* nextMove = new Move(servo1, servo2, servo3, servo4, servo5, servo6);
    moves.add(nextMove);
  }
}


void MoveArm(Move* move) {
  servo1.write(move->servoOneState);
  servo2.write(move->servoTwoState);
  servo3.write(move->servoThreeState);
  servo4.write(move->servoFourState);
  servo5.write(move->servoFiveState);
  servo6.write(move->servoSixState);
  delay(2000);

  Serial.println("Arrived");

  delete move;
}
