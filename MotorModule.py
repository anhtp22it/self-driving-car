import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Motor():
    def __init__(self, EN, IN1, IN2, ENB, IN1B, IN2B):
        self.EN = EN
        self.IN1 = IN1
        self.IN2 = IN2
        self.ENB = ENB
        self.IN1B = IN1B
        self.IN2B = IN2B
        GPIO.setup(self.EN, GPIO.OUT)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)
        GPIO.setup(self.IN1B, GPIO.OUT)
        GPIO.setup(self.IN2B, GPIO.OUT)
        self.pwmA = GPIO.PWM(self.EN, 100)
        self.pwmA.start(0)
        self.pwmB = GPIO.PWM(self.ENB, 100)
        self.pwmB.start(0)
        
    def move(self, speed=0.5, turn=0, time=0):
        speed = int(speed * 100)
        turn = int(turn * 100)
        leftSpeed = speed - turn
        rightSpeed = speed + turn
        
        if leftSpeed > 100:
            leftSpeed = 100
        elif leftSpeed < -100:
            leftSpeed = -100
            
        if rightSpeed > 100:
            rightSpeed = 100
        elif rightSpeed < -100:
            rightSpeed = -100
            
        self.pwmA.ChangeDutyCycle(abs(leftSpeed))
        self.pwmB.ChangeDutyCycle(abs(rightSpeed))
        
        if leftSpeed > 0:
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
        elif leftSpeed < 0:
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            
        if rightSpeed > 0:
            GPIO.output(self.IN1B, GPIO.HIGH)
            GPIO.output(self.IN2B, GPIO.LOW)
        elif rightSpeed < 0:
            GPIO.output(self.IN1B, GPIO.LOW)
            GPIO.output(self.IN2B, GPIO.HIGH)
        sleep(time)
        
    def stop(self, time=0):
        self.pwmA.ChangeDutyCycle(0)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        self.pwmB.ChangeDutyCycle(0)
        GPIO.output(self.IN1B, GPIO.LOW)
        GPIO.output(self.IN2B, GPIO.LOW)
        sleep(time)
    
    def cleanup(self):
        self.pwmA.stop()
        self.pwmB.stop()
        GPIO.cleanup()
         