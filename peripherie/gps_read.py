import RPi.GPIO as GPIO
import time

#GPIO Modus (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#GPIO Pins zuweisen
GPIO_TRIGGER_TOP = 23 #top sensor
GPIO_ECHO_TOP = 24
GPIO_TRIGGER_DOWN = 25 #bottom   sensor
GPIO_ECHO_DOWN = 12
GPIO_TRIGGER_LEFT = 16 #front left sensor
GPIO_ECHO_LEFT = 20
GPIO_TRIGGER_RIGHT =19  #front right sensor
GPIO_ECHO_RIGHT = 26
#Richtung der GPIO-Pins festlegen (IN / OUT)
GPIO.setup(GPIO_TRIGGER_TOP, GPIO.OUT)
GPIO.setup(GPIO_ECHO_TOP, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_DOWN, GPIO.OUT)
GPIO.setup(GPIO_ECHO_DOWN, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_LEFT, GPIO.OUT)
GPIO.setup(GPIO_ECHO_LEFT, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_RIGHT, GPIO.OUT)
GPIO.setup(GPIO_ECHO_RIGHT, GPIO.IN)

def distanz(triggerpin, echopin):
    # setze Trigger auf HIGH
    GPIO.output(triggerpin, True)

    # setze Trigger nach 0.01ms aus LOW
    time.sleep(0.00001)
    GPIO.output(triggerpin, False)

    StartZeit = time.time()
    StopZeit = time.time()

    # speichere Startzeit
    while GPIO.input(echopin) == 0:
        StartZeit = time.time()

    # speichere Ankunftszeit
    while GPIO.input(echopin) == 1:
        StopZeit = time.time()

    # Zeit Differenz zwischen Start und Ankunft
    TimeElapsed = StopZeit - StartZeit
    # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
    # und durch 2 teilen, da hin und zurueck
    distanz = (TimeElapsed * 34300) / 2

    return distanz

if __name__ == '__main__':
    try:
        while True:
            abstand = distanz(GPIO_TRIGGER_TOP, GPIO_ECHO_TOP)
            print ("Gemessene Entfernung oben = %.1f cm" % abstand)
            #time.sleep(1)
            abstand = distanz(GPIO_TRIGGER_DOWN, GPIO_ECHO_DOWN)
            print ("Gemessene Entfernung unten = %.1f cm" % abstand)
            #time.sleep(1)
            abstand = distanz(GPIO_TRIGGER_LEFT, GPIO_ECHO_LEFT)
            print ("Gemessene Entfernung links = %.1f cm" % abstand)
            #time.sleep(1)
            abstand = distanz(GPIO_TRIGGER_RIGHT, GPIO_ECHO_RIGHT)
            print ("Gemessene Entfernung rechts = %.1f cm" % abstand)
            print ("\n")
            time.sleep(1)

        # Beim Abbruch durch STRG+C resetten
    except KeyboardInterrupt:
        print("Messung vom User gestoppt")
        GPIO.cleanup()