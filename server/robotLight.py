#!/usr/bin/env python3
# File name   : robotLight.py
# Website     : www.adeept.com
# Author      : Adeept
# Date        : 2025/05/15
import time
import sys
from gpiozero import PWMOutputDevice as PWM
from rpi_ws281x import *
import threading
import spidev
import numpy
from numpy import sin, cos, pi
def check_rpi_model():
    _, result = run_command("cat /proc/device-tree/model |awk '{print $3}'")
    result = result.strip()
    if result == '3':
        return 3
    elif result == '4':
        return 4
    elif result == '5':
        return 5
    else:
        return None

def run_command(cmd=""):
    import subprocess
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = p.stdout.read().decode('utf-8')
    status = p.poll()
    return status, result


def map(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


class RobotWS2812(threading.Thread):
    def __init__(self, *args, **kwargs):
        self.LED_COUNT	  	= 16	  # Number of LED pixels.
        self.LED_PIN		= 12	  # GPIO pin connected to the pixels (18 uses PWM!).
        self.LED_FREQ_HZ	= 800000  # LED signal frequency in hertz (usually 800khz)
        self.LED_DMA		= 10	  # DMA channel to use for generating signal (try 10)
        self.LED_BRIGHTNESS = 255	 # Set to 0 for darkest and 255 for brightest
        self.LED_INVERT	 = False   # True to invert the signal (when using NPN transistor level shift)
        self.LED_CHANNEL	= 0	   # set to '1' for GPIOs 13, 19, 41, 45 or 53

        self.colorBreathR = 0
        self.colorBreathG = 0
        self.colorBreathB = 0
        self.breathSteps = 10


        self.lightMode = 'none'		#'none' 'police' 'breath'


        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()

        super(RobotWS2812, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()
        self.__flag.clear()

    # Define functions which animate LEDs in various ways.
    def set_all_led_color_data(self, R, G, B):
        """Wipe color across display a pixel at a time."""
        color = Color(int(R),int(G),int(B))
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()

    def setSomeColor(self, R, G, B, ID):
        color = Color(int(R),int(G),int(B))
        for i in ID:
            self.strip.setPixelColor(i, color)
            self.strip.show()

    def pause(self):
        self.lightMode = 'none'
        self.set_all_led_color_data(0,0,0)
        self.__flag.clear()

    def resume(self):
        self.__flag.set()

    def led_close(self):
        self.lightMode = 'none'
        self.set_all_led_color_data(0,0,0)
        self.__flag.clear()
    def police(self):
        self.lightMode = 'police'
        self.resume()


    def policeProcessing(self):
        while self.lightMode == 'police':
            for i in range(0,3):
                self.setSomeColor(0,0,255,[0,1,2,3,4,5,6,7,8,9,10,11])
                self.set_all_led_color_data(0,0,255)
                time.sleep(0.05)
                self.setSomeColor(0,0,0,[0,1,2,3,4,5,6,7,8,9,10,11])
                self.set_all_led_color_data(0,0,0)
                time.sleep(0.05)
            if self.lightMode != 'police':
                break
            time.sleep(0.1)
            for i in range(0,3):
                self.setSomeColor(255,0,0,[0,1,2,3,4,5,6,7,8,9,10,11])
                self.set_all_led_color_data(255,0,0)
                time.sleep(0.05)
                self.setSomeColor(0,0,0,[0,1,2,3,4,5,6,7,8,9,10,11])
                self.set_all_led_color_data(0,0,0)
                time.sleep(0.05)
            time.sleep(0.1)


    def breath(self, R_input, G_input, B_input):
        self.lightMode = 'breath'
        self.colorBreathR = R_input
        self.colorBreathG = G_input
        self.colorBreathB = B_input
        self.resume()


    def breathProcessing(self):
        while self.lightMode == 'breath':
            for i in range(0,self.breathSteps):
                if self.lightMode != 'breath':
                    break
                self.set_all_led_color_data(self.colorBreathR*i/self.breathSteps, self.colorBreathG*i/self.breathSteps, self.colorBreathB*i/self.breathSteps)
                time.sleep(0.03)
            for i in range(0,self.breathSteps):
                if self.lightMode != 'breath':
                    break
                self.set_all_led_color_data(self.colorBreathR-(self.colorBreathR*i/self.breathSteps), self.colorBreathG-(self.colorBreathG*i/self.breathSteps), self.colorBreathB-(self.colorBreathB*i/self.breathSteps))
                time.sleep(0.03)

    def lightChange(self):
        if self.lightMode == 'none':
            self.pause()
        elif self.lightMode == 'police':
            self.policeProcessing()
        elif self.lightMode == 'breath':
            self.breathProcessing()


    def run(self):
        while 1:
            self.__flag.wait()
            self.lightChange()
            pass





class Adeept_SPI_LedPixel(threading.Thread):
    def __init__(self, count = 8, bright = 255, sequence='GRB', bus = 0, device = 0, *args, **kwargs):
        self.set_led_type(sequence)
        self.set_led_count(count)
        self.set_led_brightness(bright)
        self.led_begin(bus, device)
        self.lightMode = 'none'
        self.colorBreathR = 0
        self.colorBreathG = 0
        self.colorBreathB = 0
        self.breathSteps = 10

        
        self.rainbow_r = 0
        self.rainbow_g = 0
        self.rainbow_b = 00

        self.colorFlowingR = 0
        self.colorFlowingG = 0
        self.colorFlowingB = 0

        self.set_all_led_color(0,0,0)
        super(Adeept_SPI_LedPixel, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()
        self.__flag.clear()
    def led_begin(self, bus = 0, device = 0):
        self.bus = bus
        self.device = device
        try:
            self.spi = spidev.SpiDev()
            self.spi.open(self.bus, self.device)
            self.spi.mode = 0
            self.led_init_state = 1
        except OSError:
            print("Please check the configuration in /boot/firmware/config.txt.")
            if self.bus == 0:
                print("You can turn on the 'SPI' in 'Interface Options' by using 'sudo raspi-config'.")
                print("Or make sure that 'dtparam=spi=on' is not commented, then reboot the Raspberry Pi. Otherwise spi0 will not be available.")
            else:
                print("Please add 'dtoverlay=spi{}-2cs' at the bottom of the /boot/firmware/config.txt, then reboot the Raspberry Pi. otherwise spi{} will not be available.".format(self.bus, self.bus))
            self.led_init_state = 0
            
    def check_spi_state(self):
        return self.led_init_state
        
    def spi_gpio_info(self):
        if self.bus == 0:
            print("SPI0-MOSI: GPIO10(WS2812-PIN)  SPI0-MISO: GPIO9  SPI0-SCLK: GPIO11  SPI0-CE0: GPIO8  SPI0-CE1: GPIO7")
        elif self.bus == 1:
            print("SPI1-MOSI: GPIO20(WS2812-PIN)   SPI1-MISO: GPIO19  SPI1-SCLK: GPIO21  SPI1-CE0: GPIO18  SPI1-CE1: GPIO17  SPI0-CE1: GPIO16")
        elif self.bus == 2:
            print("SPI2-MOSI: GPIO41(WS2812-PIN)   SPI2-MISO: GPIO40  SPI2-SCLK: GPIO42  SPI2-CE0: GPIO43  SPI2-CE1: GPIO44  SPI2-CE1: GPIO45")
        elif self.bus == 3:
            print("SPI3-MOSI: GPIO2(WS2812-PIN)  SPI3-MISO: GPIO1  SPI3-SCLK: GPIO3  SPI3-CE0: GPIO0  SPI3-CE1: GPIO24")
        elif self.bus == 4:
            print("SPI4-MOSI: GPIO6(WS2812-PIN)  SPI4-MISO: GPIO5  SPI4-SCLK: GPIO7  SPI4-CE0: GPIO4  SPI4-CE1: GPIO25")
        elif self.bus == 5:
            print("SPI5-MOSI: GPIO14(WS2812-PIN)  SPI5-MISO: GPIO13  SPI5-SCLK: GPIO15  SPI5-CE0: GPIO12  SPI5-CE1: GPIO26")
        elif self.bus == 6:
            print("SPI6-MOSI: GPIO20(WS2812-PIN)  SPI6-MISO: GPIO19  SPI6-SCLK: GPIO21  SPI6-CE0: GPIO18  SPI6-CE1: GPIO27")
    
    def led_close(self):
        self.set_all_led_rgb([0,0,0])
        self.spi.close()
    
    def set_led_count(self, count):
        self.led_count = count
        self.led_color = [0,0,0] * self.led_count
        self.led_original_color = [0,0,0] * self.led_count
    
    def set_led_type(self, rgb_type):
        try:
            led_type = ['RGB','RBG','GRB','GBR','BRG','BGR']
            led_type_offset = [0x06,0x09,0x12,0x21,0x18,0x24]
            index = led_type.index(rgb_type)
            self.led_red_offset = (led_type_offset[index]>>4) & 0x03
            self.led_green_offset = (led_type_offset[index]>>2) & 0x03
            self.led_blue_offset = (led_type_offset[index]>>0) & 0x03
            return index
        except ValueError:
            self.led_red_offset = 1
            self.led_green_offset = 0
            self.led_blue_offset = 2
            return -1
    
    def set_led_brightness(self, brightness):
        self.led_brightness = brightness
        for i in range(self.led_count):
            self.set_led_rgb_data(i, self.led_original_color)
            
    def set_ledpixel(self, index, r, g, b):
        p = [0,0,0]
        p[self.led_red_offset] = round(r * self.led_brightness / 255)
        p[self.led_green_offset] = round(g * self.led_brightness / 255)
        p[self.led_blue_offset] = round(b * self.led_brightness / 255)
        self.led_original_color[index*3+self.led_red_offset] = r
        self.led_original_color[index*3+self.led_green_offset] = g
        self.led_original_color[index*3+self.led_blue_offset] = b
        for i in range(3):
            self.led_color[index*3+i] = p[i]

    def set_led_color_data(self, index, r, g, b):
        self.set_ledpixel(index, r, g, b)  
        
    def set_led_rgb_data(self, index, color):
        self.set_ledpixel(index, color[0], color[1], color[2])   
        
    def set_led_color(self, index, r, g, b):
        self.set_ledpixel(index, r, g, b)
        self.show() 
        
    def set_led_rgb(self, index, color):
        self.set_led_rgb_data(index, color)   
        self.show() 
    
    def set_all_led_color_data(self, r, g, b):
        for i in range(self.led_count):
            self.set_led_color_data(i, r, g, b)
            
    def set_all_led_rgb_data(self, color):
        for i in range(self.led_count):
            self.set_led_rgb_data(i, color)   
        
    def set_all_led_color(self, r, g, b):
        for i in range(self.led_count):
            self.set_led_color_data(i, r, g, b)
        self.show()
        
    def set_all_led_rgb(self, color):
        for i in range(self.led_count):
            self.set_led_rgb_data(i, color) 
        self.show()
    
    
    def write_ws2812_numpy8(self):
        d = numpy.array(self.led_color).ravel()        #Converts data into a one-dimensional array
        tx = numpy.zeros(len(d)*8, dtype=numpy.uint8)  #Each RGB color has 8 bits, each represented by a uint8 type data
        for ibit in range(8):                          #Convert each bit of data to the data that the spi will send
            tx[7-ibit::8]=((d>>ibit)&1)*0x78 + 0x80    #T0H=1,T0L=7, T1H=5,T1L=3   #0b11111000 mean T1(0.78125us), 0b10000000 mean T0(0.15625us)  
        if self.led_init_state != 0:
            if self.bus == 0:
                self.spi.xfer(tx.tolist(), int(8/1.25e-6))         #Send color data at a frequency of 6.4Mhz
            else:
                self.spi.xfer(tx.tolist(), int(8/1.0e-6))          #Send color data at a frequency of 8Mhz
        
    def write_ws2812_numpy4(self):
        d=numpy.array(self.led_color).ravel()
        tx=numpy.zeros(len(d)*4, dtype=numpy.uint8)
        for ibit in range(4):
            tx[3-ibit::4]=((d>>(2*ibit+1))&1)*0x60 + ((d>>(2*ibit+0))&1)*0x06 + 0x88  
        if self.led_init_state != 0:
            if self.bus == 0:
                self.spi.xfer(tx.tolist(), int(4/1.25e-6))         
            else:
                self.spi.xfer(tx.tolist(), int(4/1.0e-6))       
        
    def show(self, mode = 1):
        if mode == 1:
            write_ws2812 = self.write_ws2812_numpy8
        else:
            write_ws2812 = self.write_ws2812_numpy4
        write_ws2812()
        
    def wheel(self, pos):
        if pos < 85:
            return [(255 - pos * 3), (pos * 3), 0]
        elif pos < 170:
            pos = pos - 85
            return [0, (255 - pos * 3), (pos * 3)]
        else:
            pos = pos - 170
            return [(pos * 3), 0, (255 - pos * 3)]
    
    def hsv2rgb(self, h, s, v):
        h = h % 360
        rgb_max = round(v * 2.55)
        rgb_min = round(rgb_max * (100 - s) / 100)
        i = round(h / 60)
        diff = round(h % 60)
        rgb_adj = round((rgb_max - rgb_min) * diff / 60)
        if i == 0:
            r = rgb_max
            g = rgb_min + rgb_adj
            b = rgb_min
        elif i == 1:
            r = rgb_max - rgb_adj
            g = rgb_max
            b = rgb_min
        elif i == 2:
            r = rgb_min
            g = rgb_max
            b = rgb_min + rgb_adj
        elif i == 3:
            r = rgb_min
            g = rgb_max - rgb_adj
            b = rgb_max
        elif i == 4:
            r = rgb_min + rgb_adj
            g = rgb_min
            b = rgb_max
        else:
            r = rgb_max
            g = rgb_min
            b = rgb_max - rgb_adj
        return [r, g, b]
    
    def police(self):
        self.lightMode = 'police'
        self.resume()
        
    def breath(self, R_input, G_input, B_input):
        self.lightMode = 'breath'
        self.colorBreathR = R_input
        self.colorBreathG = G_input
        self.colorBreathB = B_input
        self.resume()    

    def rainbow(self, R_input, G_input, B_input):
        self.lightMode = 'rainbow'
        self.rainbow_r = R_input
        self.rainbow_g = G_input
        self.rainbow_b = B_input
        self.resume()

    def flowing(self, R_input, G_input, B_input):
        self.lightMode = 'flowing'
        self.colorFlowingR = R_input
        self.colorFlowingG = G_input
        self.colorFlowingB = B_input
        self.resume()
            
    def resume(self):
        self.__flag.set()



    def pause(self):
        self.lightMode = 'none'
        self.set_all_led_color_data(0,0,0)
        self.__flag.clear()

    def breathProcessing(self):
        while self.lightMode == 'breath':
            for i in range(0,self.breathSteps):
                if self.lightMode != 'breath':
                    break
                self.set_all_led_color(self.colorBreathR*i/self.breathSteps, self.colorBreathG*i/self.breathSteps, self.colorBreathB*i/self.breathSteps)
                time.sleep(0.03)
            for i in range(0,self.breathSteps):
                if self.lightMode != 'breath':
                    break
                self.set_all_led_color(self.colorBreathR-(self.colorBreathR*i/self.breathSteps), self.colorBreathG-(self.colorBreathG*i/self.breathSteps), self.colorBreathB-(self.colorBreathB*i/self.breathSteps))
                time.sleep(0.03)

    def policeProcessing(self):
        while self.lightMode == 'police':
            for i in range(0,3):
                self.set_all_led_color_data(0,0,255)
                self.show()
                time.sleep(0.05)
                self.set_all_led_color_data(0,0,0)
                self.show()
                time.sleep(0.05)
            if self.lightMode != 'police':
                break
            time.sleep(0.1)
            for i in range(0,3):
                self.set_all_led_color_data(255,0,0)
                self.show()
                time.sleep(0.05)
                self.set_all_led_color_data(0,0,0)
                self.show()
                time.sleep(0.05)
            time.sleep(0.1)

    def rainbowProcessing(self):
        while self.lightMode == 'rainbow':
            for i in range(self.led_count):
                self.rainbow_r = self.rainbow_r + i * 10
                self.rainbow_g = self.rainbow_g + i * 10
                self.rainbow_b = self.rainbow_b + i * 10
                if self.rainbow_r > 255:
                    self.rainbow_r -= 255
                if self.rainbow_g > 255:
                    self.rainbow_g -= 255
                if self.rainbow_b > 255:
                    self.rainbow_b -= 255
                self.set_led_color(i, self.rainbow_r + i * 10,self.rainbow_g,self.rainbow_b)
                self.show()
                self.lightMode = 'none'

    def flowingProcessing(self):
        while self.lightMode == 'flowing':
            self.set_all_led_rgb_data([0, 0, 0])
            for i in range(self.led_count):
                self.set_led_color(i, self.colorFlowingR,self.rainbow_g,self.colorFlowingR)
                time.sleep(0.2)
                self.show()
            time.sleep(0.2)    
            
            
    def lightChange(self):
        if self.lightMode == 'none':
            self.pause()
        elif self.lightMode == 'police':
            self.policeProcessing()
        elif self.lightMode == 'breath':
            self.breathProcessing()    
        elif self.lightMode == 'rainbow':
            self.rainbowProcessing()
        elif self.lightMode == 'flowing':
            self.flowingProcessing() 
    
    def run(self):
        while 1:
            self.__flag.wait()
            self.lightChange()
            pass



if __name__ == '__main__':
    import time
    import os
    print("spidev version is ", spidev.__version__)
    print("spidev device as show:")
    
    led = Adeept_SPI_LedPixel(8, 255)              # Use MOSI for /dev/spidev0 to drive the lights
    try:
        if led.check_spi_state() != 0:
            led.set_led_count(8)
            led.set_all_led_color_data(255, 0, 0)
            led.show()
            time.sleep(0.5)
            led.set_all_led_rgb_data([0, 255, 0])
            led.show()
            time.sleep(0.5)
            led.set_all_led_color(0, 0, 255)
            time.sleep(0.5)
            led.set_all_led_rgb([0, 255, 255])
            time.sleep(0.5)

            led.set_led_count(12)
            led.set_all_led_color_data(255, 255, 0)
            for i in range(255):
                led.set_led_brightness(i)
                led.show()
                time.sleep(0.005)
            for i in range(255):
                led.set_led_brightness(255-i)
                led.show()
                time.sleep(0.005)
                  
            led.set_led_brightness(20)
            while True:
                for j in range(255):
                    for i in range(led.led_count):
                        led.set_led_rgb_data(i, led.wheel((round(i * 255 / led.led_count) + j)%256))
                    led.show()
                    time.sleep(0.002)
        else:
            led.led_close()
    except KeyboardInterrupt:
        led.led_close()
