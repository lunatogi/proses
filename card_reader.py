import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

def ReadCard():               #Reads data from rfid reader
    GPIO.setwarnings(False)     
    reader = SimpleMFRC522()
        
    try:
        id, text = reader.read()
        return text
    except:
        return None
    finally:
        GPIO.cleanup()
