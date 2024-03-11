from fuzz_main import *

def main():
    # 函数映射
    function_mapping = {
        1: telnet_main,
        2: http_main,
        3: modbus_main,
        4: ssh_main,
        5: mqtt_main,
        6: echo_main,
        7: ftp_main,
    }

    while True:
        try:
            # 提示用户输入数字组合或"exit"退出程序
            user_input = input("请输入要fuzz的协议（1: telnet, 2: http, 3: modbus, 4: ssh, 5: mqtt, 6: echo, 7: ftp）,数字组合（用逗号分隔，例如1,2,3），或输入 'exit' 退出：")

            if user_input.lower() == 'exit':
                print("程序已退出。")
                break

            # 将用户输入的数字拆分成列表
            numbers = [int(num) for num in user_input.split(",")]

            # 执行相应的函数
            for number in numbers:
                if number in function_mapping:
                    function_mapping[number]()
                else:
                    print(f"数字 {number} 没有对应的函数。")
        except ValueError:
            print("请输入有效的数字组合。")
        except KeyboardInterrupt:
            print("程序已终止。")
            break

if __name__ == "__main__":
    main()