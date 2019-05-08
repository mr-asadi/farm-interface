from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.spinner import Spinner
from kivy.properties import BooleanProperty
from kivy.clock import Clock
from gauge import Gauge
import serial
from get_ports import serial_ports
import json
from random import random

class AccordionApp(App):
    PORTS = ['COM1','COM2','COM3']
    BAUDRATES = [
    "1200",
    "1800",
    "2400",
    "4800",
    "9600",
    "38400",
    "19200",
    "57600",
    "115200",
    ]
    def __init__(self, **kwargs):
        super(AccordionApp, self).__init__(**kwargs)
        '''read the port and baudrate from config.txt file
        if exist connect past port and baudrate
            if connect correctly end
        else (port and baudrate do not exist or don't work correctly) go to config page and get system ports and baudrates and let user choose
        listen to errors:
        1.not recognize port
        2.port is not config correctly(baudrate)
        3.port does not open
        4.port is suddenly closed
        then open config page'''
        connection_status = BooleanProperty(False)

    def build(self):
        num_page=2
        root = Accordion()
        pages = list()

        for page in range(num_page):
            item = AccordionItem(title=f'Title{page}')
            grid = GridLayout(cols=3,spacing=20,padding=10)
            # with grid.canvas:
            #     Color(0.5,0.6,0.7,0.8)
            #     Rectangle(size=grid.size,pos=grid.pos)
            item.add_widget(grid)
            root.add_widget(item)
            pages.append(grid)
        #!!! this must be get from serial port !!!#
        Buttons_text = list(map(lambda num:'Button '+str(num),range(1,6)))
        Buttons_status0 = ['open','close','deactive','open','close','deactive']
        Buttons_status = dict()
        for name,status in zip(Buttons_text,Buttons_status0):
            Buttons_status[name]=status
        # predefined constants
        Buttons_color = {'open':[random(),random(),random(),0.9],'close':[1,0,0,0.9],'deactive':[0.5,0.5,0.5,0.9]}
        
        # add Buttons to page 0
        Buttons = list(map(lambda name:Button(text=name, background_color=Buttons_color[Buttons_status[name]]),Buttons_text))
        # Clock.schedule_interval(Buttons[0]., 1.0 / 60.0)
        # Buttons[0].bind(on_press=print('hello world'))
        _=list(map(lambda button:pages[0].add_widget(button),Buttons))

         # add Gauges to page 1
        Gauges = list(map(lambda gauge: Gauge(value=50, size_gauge=200, size_text=19),Buttons_text))
        _=list(map(lambda gauge: pages[1].add_widget(gauge),Gauges))
        
        ### defines events
        _=list(map(lambda button:button.bind(on_press=lambda button: self.ErrorWindow()), Buttons))
        return root

    def ErrorWindow(self):

        popupwindow = FloatLayout()

        # add events to the widgets
        def port_on_release(self):
            self.popup_label.text = f'Configure to port: {self.port.text} .' if (self.baudrate.text == 'Baudrate') else f'Configure to port: {self.port.text} and baudtare: {self.baudrate.text} .'
        def baudrate_on_release(self):
            self.popup_label.text = f'Configure to port: {self.port.text} .' if (self.baudrate.text == 'Baudrate') else f'Configure to port: {self.port.text} and baudtare: {self.baudrate.text} .'
        def try_on_press(self):
            print('try_on_press')
        def close_on_press(self):
            print('close_on_press')

        # define popup window widgets
        self.port = Spinner(text='Port',values=AccordionApp.PORTS,pos_hint={'x':0.0,'center_y':0.8},size_hint=[0.5,0.1],on_text=lambda spinner:port_on_release(self))
        self.baudrate = Spinner(text='Baudrate',values=AccordionApp.BAUDRATES,pos_hint={'x':0.5,'center_y':0.8},size_hint=[0.5,0.1],on_release=lambda spinner:baudrate_on_release(self))
        self.popup_label = Label(text='please choose port and baudrate to configure correctly.',pos_hint={'center_x':0.3,'center_y':0.5},size_hint=[0.8,0.1])
        self.popup_try = Button(text='try',pos_hint={'x':0,'y':0},size_hint=[0.5,0.1],on_press=lambda button:try_on_press(self))
        self.popup_close = Button(text='close',pos_hint={'x':0.5,'y':0},size_hint=[0.5,0.1],on_press=lambda button:close_on_press(self))
        # add modules to the popup window
        popupwindow.add_widget(self.popup_label)
        popupwindow.add_widget(self.popup_try)
        popupwindow.add_widget(self.popup_close)
        popupwindow.add_widget(self.port)
        popupwindow.add_widget(self.baudrate)

        # make popup window 
        popup = Popup(content=popupwindow,title='Configuration', auto_dismiss=False)

        # bind the on_press event of the button to the dismiss function
        popupwindow.bind(on_press=popup.dismiss)
        popup.open()
        # class Check_Connection(EventDispatcher):
        #     pass
class connection(AccordionApp):
    def __init__(self):
        '''connect to sensors
        get status of every sensor
        listen to every response'''
        # get serial ports of system
        # first read config.txt file and try to config
        # except get system ports
        # try to config from ports and save at config.txt
        # go to main app
        self.ser = serial.Serial()
        try:
            with open('config.txt') as json_file:  
                data = json.load(json_file)
            PORT = data['PORT']
            BAUDRATE = data['BAUDRATE']
            self.ser.port = PORT
            self.ser.baudrate = BAUDRATE
            
        except:
            PORTS = serial_ports()
            # go to popupWindow and get
            PORT = AccordionApp.port.text
            BAUDRATE = int(AccordionApp.baudrate.text)
            with open('config.txt','w') as outfile:
                json.dump({'PORT':PORT,'BAUDRATE':BAUDRATE},outfile)


        self.ser.port = 'COM3'
        self.ser.baudrate = 9600
        if not self.ser.is_open:
            self.ser.open()
        #read pressure
        self.pressure = self.ser.read()

    def do(self, button_id, action):
        '''write some action on the port''' 
        self.ser.write(action)

if __name__ == '__main__':
    '''read config.txt
    try to connect to port and baudrate
    except get ports
    disp them'''
    AccordionApp().run()
