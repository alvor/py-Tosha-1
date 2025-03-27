import gc
import machine as m
from machine import reset, Pin
from libs.kernel import os_kernel , Kernel, Service, load
from libs.ble_connect import ble
from libs.ble_repl import ble_repl
from libs.net_manager import NetworkManager
from modules.switches_demo_c3 import SwitchesBoard_demo_c3  # переключатели
from web.webserver import WebServer
from web.files import Files  # Файловый менеджер 
from web.web_switches import WebSwitches 
from web.web_standard import WebStandard
from web.web_cron import WebCron
from web.net_configure import NetConfig 
from modules.cron import CronScheduler
from modules.GPIO_board import GPIO_board

#import webrepl
#webrepl.start()  #port 8266

net = None
sw = None
cron = None
pins = None

list_devs =[11,22]

h = "reset(), net.sta.scan(), net.connect(lan,psw), net.status, ..."

class init( ):
    #def __init__(self):
        global net, sw, cron, pins
        #self.os_kernel = Kernel()

        # Инициализация сетевого менеджера
        net = NetworkManager(name='NET_MANAGER', timezone_offset=7)
        os_kernel.add_task(net)

        sw = SwitchesBoard_demo_c3(name="SwitchesBoard_demo_c3")
        os_kernel.add_task(sw)

        pins = GPIO_board([
          #(0, Pin.IN, Pin.PULL_UP),
          (8, Pin.OUT),
          (9, Pin.IN)
        ], name="GPIO_board", group=3)
        os_kernel.add_task(pins)

        pins2 = GPIO_board([
          #(0, Pin.IN, Pin.PULL_UP),
          (8, Pin.OUT),
          (9, Pin.IN)
        ], name="GPIO_board2", label="GPIO_board-2", group=3)
        os_kernel.add_task(pins2)

        # Инициализация веб-интерфейса
        web = WebServer(name="WebServer", kernel=os_kernel)
        #self.web.devs = self.devs
        os_kernel.add_task(web)

        # Инициализация файлового веб-интерфейса
        _ = Files(name="Web file manager", web=web)

        # Инициализация web-интерфейса переключателей
        _ = WebSwitches(name="Web switches", web=web)

        # Инициализация web-интерфейса стандартного управления
        _ = WebStandard(name="Web standard", web=web)


        # Инициализация web-интерфейса конфигуратора сети
        _ = NetConfig(name="Network Manager", web=web, net_manager=net)

        _ = WebCron(name="Web cron", web=web)


        cron = CronScheduler()
        os_kernel.add_task(cron)

        cron.append_command( 22,  sw.set_value, 'Включить выход', (8, 1))
        cron.append_command( 11,  sw.set_value, 'Отключить выход', {"id":7, "value":0} )

        #print("Starting OS Kernel")
        os_kernel.start()


if __name__ == "__main__":
    init()
    print('type h for help')
    print('free_mem: ',gc.mem_free())
