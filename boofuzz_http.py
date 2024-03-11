from boofuzz import *
import subprocess
import threading

def wire():
    # 定义要监视的网络接口
    interface = "以太网 4"

    # 定义要保存捕获数据的文件名
    output_file = "http1.pcap"

    # 提供Wireshark可执行文件的完整路径
    wireshark_path = r"D:\wireshark\Wireshark.exe"

    # 使用subprocess启动Wireshark并捕获数据
    command = [wireshark_path, "-i", interface, "-k", "-w", output_file]
    subprocess.run(command)

def http_fuzz():
    session = Session(
        target=Target(
            connection=TCPSocketConnection("192.168.81.130", 80)
        ),
    )

    s_initialize(name="Request")
    with s_block("Request-Line"):
        s_group("Method", ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE'])
        s_delim(" ", name='space-1')
        s_string("/index.html", name='Request-URI')
        s_delim(" ", name='space-2')
        s_string('HTTP/1.1', name='HTTP-Version')
        s_static("\r\n", name="Request-Line-CRLF")
    s_static("\r\n", "Request-CRLF")

    session.connect(s_get("Request"))

    session.fuzz()

def http():
    # 创建两个线程，一个运行wire函数，一个运行http_fuzz函数
    wire_thread = threading.Thread(target=wire)
    fuzz_thread = threading.Thread(target=http_fuzz)

    # 启动线程
    wire_thread.start()
    fuzz_thread.start()

    # 等待线程结束
    wire_thread.join()
    fuzz_thread.join()
