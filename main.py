# Progettone
# Created at 2017-05-28 07:42:37.889559

import streams
import threading
from wireless import wifi
from stm.spwf01sa import spwf01sa
from zerynthapp import zerynthapp
from stm.hts221 import hts221
import adc

streams.serial()

uid='FesQpAiuRSql-VCvmbkGSQ'
token='UrTHdXIaTGKNyW6durt50A'

# Variable def
heating_pin=D9
water_pin=D10
light_pin=D11
light_test_pin=D12
photoresistor=A0
wifi_reset_pin=D15
btn_pin=BTN0

delay=0
desired_temp=22
heat_state=False 
heat_active=False
light_state=False
light_active=False
water_state=False
water_active=False
state=False

#Functions
def set_desired_temp(desired):
    global desired_temp
    print('Desired temp from app: ', desired)
    desired_temp=int(desired)

def get_initial_state(*args):
    global desired_temp, water_state, heat_state, light_state, state
    print('I am getting the initial state')
    res = ({'state': state, 'water_state': water_state, 'heat_state': heat_state, 'light_state': light_state, 'desired_temp': desired_temp})
    return res

def heating_switch(new_state):
    global heat_state
    heat_state=new_state
    print('New heating state: ', heat_state)


def water_switch(new_state):
    global water_state
    water_state=new_state
    print('New water state: ', water_state)


def light_switch(new_state):
    global light_state
    light_state=new_state
    print('New light state: ', light_state)


def set_delay(time):
    global delay
    print('I am setting delay of', time)
    delay=time
    thread(tred)

def set_state(new_state):
    global state
    print('I am setting the new state - after setting the shower time ', new_state)
    state=new_state

def button_press():
    global state, light_state, water_state, heat_state
    print('I am resetting all')
    state = False
    heat_state = False
    light_state = False
    water_state = False
    zapp.event({'control':0, 'state':state, 'water_state': water_state, 'heat_state': heat_state, 'light_state': light_state})

#questo è il thread
def tred():
    global delay, state, light_state, water_state, heat_state
    print('Inside the thread')
    if state:
        if delay < 1800000:
            heat_state = True
            zapp.event({'control':2, 'heat_state': heat_state})
            sleep(delay)
            light_state = True
            water_state = True
            zapp.event({'control':3, 'water_state': water_state, 'light_state': light_state})
            #notify("Shower", "It's shower time")
        else:
            sleep(delay-1800000)
            heat_state = True
            zapp.event({'control':2, 'heat_state': heat_state})
            sleep(1800000)
            light_state = True
            water_state = True
            zapp.event({'control':3, 'water_state': water_state, 'light_state': light_state})
            #notify("Shower", "It's shower time")

# Initialize pins
pinMode(heating_pin, OUTPUT)
digitalWrite(heating_pin, LOW)
pinMode(water_pin, OUTPUT)
digitalWrite(water_pin, LOW)
pinMode(light_pin, OUTPUT)
digitalWrite(light_pin, LOW)
pinMode(light_test_pin, OUTPUT)
digitalWrite(light_test_pin, LOW)
pinMode(photoresistor, INPUT_ANALOG)
onPinFall(btn_pin, button_press) #quando BTN0 viene premuto tutto viene spento
    
try:
    sleep(5000)
    print('Initialize wifi')
    spwf01sa.init(SERIAL2, wifi_reset_pin)
    sleep(3000)
    
    print('Connecting...')
    wifi.link('Vodafone2.4GHz-33915375', wifi.WIFI_WPA2, 'Rosato65wifi95')
    print('Connected to wifi')
    sleep(1000)
    zapp = zerynthapp.ZerynthApp(uid, token)
    print('zapp object created!')
    #############################################
    #Associate the method calls to Python funcs
    zapp.on('set_desired_temp', set_desired_temp) #gestione della temperatura desiderata
    zapp.on('heating_switch', heating_switch)       #gestione on/off riscaldamento
    zapp.on('water_switch', water_switch)           #gestion on/off acqua
    zapp.on('light_switch', light_switch)           #gestion on/off luce
    zapp.on('set_delay', set_delay)                 #gestion on/off "doccia automatica"
    zapp.on('set_state', set_state)                 #var bool che tiene traccia dell'effettivo on/off del sistema automatico 
    zapp.on('get_initial_state', get_initial_state) #invia lo stato iniziale di tutte le variabili
    
    print('Start the app instance...')
    zapp.run()
    print('Instance started.')
    sleep(3000)
    
    print('Initialize temperature sensor')
    sensor = hts221.HTS221(I2C0, D32)
    sleep(1000)
    
    while True:
        #Heating operations
        print('Reading temp:')
        temp, humidity=sensor.get_temp_humidity()
        print("Actual temp: ",temp)
        heat_active = heat_state and temp<desired_temp
        print('Setting heating pin: ', heat_active)
        if heat_active:
            digitalWrite(heating_pin, HIGH)
        else:
            digitalWrite(heating_pin, LOW)
        #Sending temp event
        erature=int((temp - int(temp))*10)  #decimal digits of temperature (we need it for html)
        temp=int(temp)                      #integer digits of temperature
        zapp.event({'control' : 1, 'temp' : temp,'erature' : erature})
        
        # Light operations
        print('Reading light')
        digitalWrite(light_test_pin, HIGH)
        sleep(500)
        light_value = analogRead(photoresistor)                    #reading from photoresistor
        print('Light value: ', light_value)
        sleep(500)
        digitalWrite(light_test_pin, LOW)
        light_active = light_state and light_value < 1000   #if the light isn't enough, the led will be switched on
        print('Setting light pin: ', light_active)
        if light_active:
            digitalWrite(light_pin, HIGH)
        else:
            digitalWrite(light_pin, LOW)
            
        # Water operations
        water_active = water_state
        print('Setting water pin: ', water_active)
        if water_active:
            digitalWrite(water_pin, HIGH)
        else:
            digitalWrite(water_pin, LOW)
        sleep(5000)
        print('-----')
except Exception as e:
    print(e)