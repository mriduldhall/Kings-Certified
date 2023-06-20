import serial
from time import sleep
from pickle import dump, load 


class RobotArm:
    def __init__(self, transmitting=False, manual_zero=True):
        self.transmitting = transmitting
        
        if self.transmitting:
            self.ser = serial.Serial('COM3', 9600)
            sleep(2)
        
        if manual_zero:
            self.servo_position = {1: 90, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
                
        else:
            self.servo_position = self.retrieve_position()

    def run_servos(self, servo_one_position, servo_two_position, servo_three_position, servo_four_position, servo_five_position, servo_six_position,):
        move_list = f"{servo_one_position},{servo_two_position},{servo_three_position},{servo_four_position},{servo_five_position},{servo_six_position}\n"
        
        self.servo_position = {1: servo_one_position, 2: servo_two_position, 3: servo_three_position, 4: servo_four_position, 5: servo_five_position, 6: servo_five_position}
        
        if self.transmitting:
            self.ser.write(move_list.encode())
            self.wait_for_arrival()

    def wait_for_arrival(self):
        while True:
            if self.ser.inWaiting() > 0:
                recv_data = self.ser.readline().decode().strip()
                self.save_position()
                return 0

    def save_position(self):
        with open('ServoPositions.pkl', 'wb') as position_file:
            dump(self.servo_position, position_file)
            position_file.close()

    @staticmethod
    def retrieve_position():
        with open('ServoPositions.pkl', 'rb') as position_file:
            servo_position = load(position_file)
            position_file.close()
        return servo_position
    
    def zero(self):
        self.run_servos(90, 0, 0, 0, 0, 0)
        self.servo_position = {1: 90, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

    def take_token(self):
        self.run_servos(153, 70, self.servo_position[3], self.servo_position[4], self.servo_position[5], 70)
        sleep(1)
        self.zero()
    
    def column1(self):
        self.run_servos(57, 65, 55, 20, self.servo_position[5], 25)
        sleep(1)
        self.zero()
    
    def column2(self):
        self.run_servos(68, 65, 55, 20, 5, 25)
        sleep(1)
        self.zero()
    
    def column3(self):
        self.run_servos(79, 65, 55, 20, 8, 25)
        sleep(1)
        self.zero()
    
    def column4(self):
        self.run_servos(90, 65, 55, 20, 10, 25)
        sleep(1)
        self.zero()
    
    def column5(self):
        self.run_servos(101, 65, 55, 20, 12, 25)
        sleep(1)
        self.zero()
    
    def column6(self):
        self.run_servos(122, 65, 55, 20, 14, 25)
        sleep(1)
        self.zero()
    
    def column7(self):
        self.run_servos(133, 55, 65, 20, 25, 17)
        sleep(1)
        self.zero()
    
    def xt(self):
        self.run_servos(175, self.servo_position[2], self.servo_position[3], self.servo_position[4], self.servo_position[5], self.servo_position[6])
        sleep(0.2)
        self.run_servos(5, self.servo_position[2], self.servo_position[3], self.servo_position[4], self.servo_position[5], self.servo_position[6])
        sleep(0.2)
        self.run_servos(90, self.servo_position[2], self.servo_position[3], self.servo_position[4], self.servo_position[5], 30)
        sleep(0.2)
        self.run_servos(20, self.servo_position[2], 40, self.servo_position[4], 35, self.servo_position[6])
        sleep(0.2)
        self.run_servos(self.servo_position[1], self.servo_position[2], self.servo_position[3], self.servo_position[4], 35, self.servo_position[6])
        sleep(0.2)
        self.run_servos(self.servo_position[1], self.servo_position[2], self.servo_position[3], self.servo_position[4], 0, self.servo_position[6])
        sleep(0.2)
        self.run_servos(90, self.servo_position[2], self.servo_position[3], self.servo_position[4], self.servo_position[5], self.servo_position[6])
        sleep(0.2)
    

if __name__ == "__main__":
    robot_arm = RobotArm()
    print(robot_arm.servo_position)

    robot_arm.column1()
