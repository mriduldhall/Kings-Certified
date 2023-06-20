import serial
from time import sleep
from pickle import dump, load 


class RobotArm:
    def __init__(self, transmitting=False, manual_zero=True):
        self.transmitting = transmitting

        if self.transmitting:
            self.ser = serial.Serial('COM3', 9600)
            sleep(2)

        self.zero_state = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

        if manual_zero:
            self.servo_position = self.zero_state

        else:
            self.servo_position = self.retrieve_position()

        self.calibration_dict = {
            1: [57, 65, 55, 20, self.servo_position[5], 25],
            2: [68, 65, 55, 20, 5, 25],
            3: [79, 65, 55, 20, 8, 25],
            4: [90, 65, 55, 20, 10, 25],
            5: [101, 65, 55, 20, 12, 25],
            6: [122, 65, 55, 20, 14, 25],
            7: [133, 55, 65, 20, 25, 17],
            'token': [153, 70, self.servo_position[3], self.servo_position[4], self.servo_position[5], 70]
        }

        self.xt_dict = {
            1: [175, self.servo_position[2], self.servo_position[3], self.servo_position[4], self.servo_position[5], self.servo_position[6]],
            2: [5, self.servo_position[2], self.servo_position[3], self.servo_position[4], self.servo_position[5], self.servo_position[6]],
            3: [90, self.servo_position[2], self.servo_position[3], self.servo_position[4], self.servo_position[5], 30],
            4: [20, self.servo_position[2], 40, self.servo_position[4], 35, self.servo_position[6]],
            5: [self.servo_position[1], self.servo_position[2], self.servo_position[3], self.servo_position[4], 35, self.servo_position[6]],
            6: [self.servo_position[1], self.servo_position[2], self.servo_position[3], self.servo_position[4], 0, self.servo_position[6]],
            7: [90, self.servo_position[2], self.servo_position[3], self.servo_position[4], self.servo_position[5], self.servo_position[6]]
        }

    def run_servos(self, servo_one_position, servo_two_position, servo_three_position, servo_four_position, servo_five_position, servo_six_position,):
        move_list = f"{servo_one_position},{servo_two_position},{servo_three_position},{servo_four_position},{servo_five_position},{servo_six_position}\n"
        
        self.servo_position = {1: servo_one_position, 2: servo_two_position, 3: servo_three_position, 4: servo_four_position, 5: servo_five_position, 6: servo_five_position}
        
        if self.transmitting:
            self.ser.write(move_list.encode())
            self.wait_for_arrival()

    def wait_for_arrival(self):
        while True:
            if self.ser.inWaiting() > 0:
                _ = self.ser.readline().decode().strip()
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
        self.run_servos(*self.zero_state)
        self.servo_position = self.zero_state

    def move(self, move):
        self.run_servos(*self.calibration_dict[move])
        sleep(1)
        self.zero()

    def xt(self):
        for i in self.xt_dict:
            self.run_servos(*self.xt_dict[i])
            sleep(0.2)
    

if __name__ == "__main__":
    robot_arm = RobotArm(True, True)
    print(robot_arm.servo_position)
    # robot_arm.zero()
    robot_arm.run_servos(10, 0, 0, 0, 0, 0)
    sleep(1)
    # robot_arm.zero()
    # sleep(1)
    # robot_arm.move(1)
