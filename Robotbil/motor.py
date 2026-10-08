from machine import Pin, PWM

class Motor:
    """Klasse til styring af én DC-motor med 2 retningspins og 1 PWM Enable-pin."""
    def __init__(self, in1_pin, in2_pin, ena_pin, pwm_freq=1000):
        self.in1 = Pin(in1_pin, Pin.OUT)
        self.in2 = Pin(in2_pin, Pin.OUT)
        self.ena = PWM(Pin(ena_pin))
        self.ena.freq(pwm_freq)
        self.stop()

    def set_speed(self, speed):
        speed = max(-100, min(100, speed))
        duty = int(abs(speed) * 65535 / 100)

        if speed > 0:
            self.in1.value(0)
            self.in2.value(1)
            self.ena.duty_u16(duty)
        elif speed < 0:
            self.in1.value(1)
            self.in2.value(0)
            self.ena.duty_u16(duty)
        else:
            self.stop(brake=True)

    def stop(self, brake=True):
        if brake:
            self.in1.value(1)
            self.in2.value(1)
            self.ena.duty_u16(65535)
        else:
            self.in1.value(0)
            self.in2.value(0)
            self.ena.duty_u16(0)


class RobotDrive:
    """Klasse til samlet styring af venstre og højre motor med trim-justering."""
    def __init__(self, left_trim=1.0, right_trim=1.0):
        # Venstre motor: IN1=GP18, IN2=GP19, ENA=GP26 (tilpasset dine pinde)
        self.left = Motor(in1_pin=26, in2_pin=21, ena_pin=16)
        # Højre motor: IN3=GP20, IN4=GP21, ENB=GP27
        self.right = Motor(in1_pin=20, in2_pin=19, ena_pin=18)

        self.left_trim = left_trim
        self.right_trim = right_trim

    def drive(self, left_speed, right_speed):
        adj_left = left_speed * self.left_trim
        adj_right = right_speed * self.right_trim
        self.left.set_speed(adj_left)
        self.right.set_speed(adj_right)

    def stop(self, brake=True):
        self.left.stop(brake)
        self.right.stop(brake)