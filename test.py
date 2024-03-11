from fuzz_main import *

def main():

    flag = int(input("请输入要fuzz的协议（1: telnet, 2: http, 3: modbus, 4: ssh, 5: mqtt, 6: echo, 7: ftp）："))
    if flag == 1:
        telnet_main() # 开启telnet fuzz，并记录response
    elif flag == 2:
        http_main() # 开启http fuzz，并记录response
    elif flag == 3:
        modbus_main() # 开启modbus fuzz，并记录response
    elif flag == 4:
        ssh_main() # 开启ssh fuzz，并记录response
    elif flag == 5:
        mqtt_main() # 开启mqtt fuzz，并记录response
    elif flag == 6:
        echo_main() # 开启echo fuzz，并记录response
    elif flag == 7:
        ftp_main() # 开启ftp fuzz，并记录response
    else:
        print("无效的选项。")

if __name__ == "__main__":
    main()