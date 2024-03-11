from boofuzz_telnet import *
from boofuzz_http import *
from boofuzz_modbus import *
from boofuzz_ssh import *
from boofuzz_mqtt import *
from boofuzz_echo import *
from boofuzz_ftp import *

#重构fuzz_telnet至telnet_main
def telnet_main():
    telnet()

#重构fuzz_http至http_main
def http_main():
    http()

#重构fuzz_modbus至modbus_main
def modbus_main():
    modbus()

#重构fuzz_ssh至ssh_main
def ssh_main():
    ssh()

#重构fuzz_mqtt至mqtt_main
def mqtt_main():
    mqtt()

#重构fuzz_echo至echo_main
def echo_main():
    echo()

#重构fuzz_ftp至ftp_main
def ftp_main():
    ftp()
