from machine import Pin, PWM
class Electromagnet:
    def __init__(self):
        self.pwm = PWM(Pin(8)) #Pin 8 from the Pico
        self.pwm.freq(8000) # pwm freq 8kHz
    #Start
    def start(self):
        duty = int(65535*0.4) #40% duty, duty can be between 0 and 100% (0<duty<1)
        self.pwm.duty_u16(duty)
    def stop(self):
        self.pwm.duty_u16(0) #Min duty

#magnet = Electromagnet()
#magnet.start()
#magnet.stop()






