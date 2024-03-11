from boofuzz import *
import subprocess
import threading

def wire():
    # 定义要监视的网络接口
    interface = "以太网 4"

    # 定义要保存捕获数据的文件名
    output_file = "echo.pcap"

    # 提供Wireshark可执行文件的完整路径
    wireshark_path = r"D:\wireshark\Wireshark.exe"

    # 使用subprocess启动Wireshark并捕获数据
    command = [wireshark_path, "-i", interface, "-k", "-w", output_file]
    subprocess.run(command)

def echo_fuzz():
    target = "192.168.81.130"  # 目标 Telnet 服务器的 IP 地址
    port = 7  # Telnet 服务器的端口
    session = Session(
        target=Target(connection=TCPSocketConnection(target, port)),
        sleep_time=1
    )

    # 定义协议模糊测试请求
    s_initialize(name="EchoRequest")
    s_string("ECHO", name="EchoCommand")
    s_delim(" ", name="Space1")
    s_string("Hello, ", name="EchoData")
    s_static("\r\n", name="CRLF")

    # 定义目标
    session.connect(s_get("EchoRequest"))

    # 设置模糊测试参数
    session.fuzz()

    # 启动模糊测试
    session.loop()

def echo():
    # 创建两个线程，一个运行wire函数，一个运行echo_fuzz函数
    wire_thread = threading.Thread(target=wire)
    fuzz_thread = threading.Thread(target=echo_fuzz)

    # 启动线程
    wire_thread.start()
    fuzz_thread.start()

    # 等待线程结束
    wire_thread.join()
    fuzz_thread.join()
