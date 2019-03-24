# Smart Bathroom
### Internet of Things project: Smart Bathroom by Maria Laura Bisogno, Luca Coppola, Vincenzo Longobardi

Our idea is to create a model of a bathroom including a shower, a heating system and a lamp to simulate a real smart bathroom that can be simply controlled with the users’ smartphone.
We realized an application which shows the current temperature of the room, allows to switch on/off every component of the bathroom and to set the shower time and desired temperature.

We used the NUCLEO-F401RE - STM32 microcontroller, the X-NUCLEO-IDW01M1 Wi-Fi module and X-NUCLEO-IKS01A2 environmental sensor expansion board.
To simulate the shower, we used a submersible pump that works with 220V.
Since the nucleo f401re can output a maximum of 5V we used an external power supply (12V) to excite the 12V relay and a transistor connected in this way:

![alt text](https://github.com/MallyDev/Smart-Bathroom/blob/master/Circuit.jpg)

The same circuit is used to control the heating system, simulated with a state led and two 12KΩ ceramic resistors in parallel. Both will be activated only if the temperature is lower than the desired one.
To simulate the lamp we used a led, controlled through MPS2 222A transistor, that will be switched on only if the light in the room is not enough.
