import time
import RPi.GPIO as GPIO
import BlynkLib

GPIO.setmode(GPIO.BCM)

TRIG_PIN = 17
ECHO_PIN = 27

GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

RED_LED_PIN = 23
GREEN_LED_PIN = 24
BUZZER_PIN = 20
TOUCH_SENSOR_PIN = 22  
VIRTUAL_PIN_1 = 2  

GPIO.setup(RED_LED_PIN, GPIO.OUT)
GPIO.setup(GREEN_LED_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(TOUCH_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Assuming active-low touch sensor

BLYNK_AUTH_TOKEN = "place your auth token here"
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)

def measure_distance():
    GPIO.output(TRIG_PIN, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)

    pulse_start = time.time()
    while GPIO.input(ECHO_PIN) == GPIO.LOW:
        pulse_start = time.time()
    
    pulse_end = time.time()
    while GPIO.input(ECHO_PIN) == GPIO.HIGH:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # in cm
    distance = round(distance, 2)

    return distance

def update_parking_status():
    distance = measure_distance()
    if distance >= 20 and GPIO.input(TOUCH_SENSOR_PIN) == GPIO.LOW:  
        print("No Intruder Nearby.\n")
        blynk.virtual_write(VIRTUAL_PIN_1, 0)
        blynk.virtual_write(1, "Safe")  
        GPIO.output(RED_LED_PIN, GPIO.LOW)  # Red LED OFF
        GPIO.output(GREEN_LED_PIN, GPIO.HIGH)  # Green LED ON
        GPIO.output(BUZZER_PIN, GPIO.LOW)
    else:        
        print("INTRUDER IN PROXIMITY!\n")
        blynk.virtual_write(VIRTUAL_PIN_1, 1)
        blynk.virtual_write(1, "INTRUDER ALERT !")  
        GPIO.output(RED_LED_PIN, GPIO.HIGH)  # Red LED ON (Occupied)
        GPIO.output(GREEN_LED_PIN, GPIO.LOW)  # Green LED OFF
        GPIO.output(BUZZER_PIN, GPIO.HIGH)

def blynk_loop():
    while True:
        blynk.run()
        update_parking_status()
        time.sleep(1)

if __name__ == "__main__":
    try:
        print("Intruder Alert System with Ultrasonic & Touch Sensor")
        blynk_loop()
    except KeyboardInterrupt:
        print("Khel Khatam")
        GPIO.cleanup()

