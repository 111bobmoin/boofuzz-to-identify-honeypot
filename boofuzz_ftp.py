#!/usr/bin/env python3
"""Demo FTP fuzzer as a standalone script."""

from boofuzz import *
import subprocess
import threading

def wire():
    # 定义要监视的网络接口
    interface = "以太网 4"

    # 定义要保存捕获数据的文件名
    output_file = "ftp.pcap"

    # 提供Wireshark可执行文件的完整路径
    wireshark_path = r"D:\wireshark\Wireshark.exe"

    # 使用subprocess启动Wireshark并捕获数据
    command = [wireshark_path, "-i", interface, "-k", "-w", output_file]
    subprocess.run(command)

def main():
    """
    这个示例是一个非常简单的FTP模糊测试工具。它不使用进程监视（procmon），并假设FTP服务器已经在运行。
    """
    session = Session(target=Target(connection=TCPSocketConnection("192.168.81.129", 21)))

    ftp_fuzz(session=session)

    session.fuzz()


def ftp_fuzz(session):
    # disable Black formatting to keep custom indentation
    # fmt: off
    user = Request("user", children=(
        String(name="key", default_value="USER"),
        Delim(name="space", default_value=" "),
        String(name="val", default_value="anonymous"),
        Static(name="end", default_value="\r\n"),
    ))

    passw = Request("pass", children=(
        String(name="key", default_value="PASS"),
        Delim(name="space", default_value=" "),
        String(name="val", default_value="james"),
        Static(name="end", default_value="\r\n"),
    ))

    stor = Request("stor", children=(
        String(name="key", default_value="STOR"),
        Delim(name="space", default_value=" "),
        String(name="val", default_value="AAAA"),
        Static(name="end", default_value="\r\n"),
    ))

    retr = Request("retr", children=(
        String(name="key", default_value="RETR"),
        Delim(name="space", default_value=" "),
        String(name="val", default_value="AAAA"),
        Static(name="end", default_value="\r\n"),
    ))
    # fmt: on

    session.connect(user)
    session.connect(user, passw)
    session.connect(passw, stor)
    session.connect(passw, retr)


def ftp_fuzz_static(session):
    """相同的协议，使用静态定义风格。"""
    s_initialize("user")
    s_string("USER")
    s_delim(" ")
    s_string("anonymous")
    s_static("\r\n")

    s_initialize("pass")
    s_string("PASS")
    s_delim(" ")
    s_string("james")
    s_static("\r\n")

    s_initialize("stor")
    s_string("STOR")
    s_delim(" ")
    s_string("AAAA")
    s_static("\r\n")

    s_initialize("retr")
    s_string("RETR")
    s_delim(" ")
    s_string("AAAA")
    s_static("\r\n")

    session.connect(s_get("user"))
    session.connect(s_get("user"), s_get("pass"))
    session.connect(s_get("pass"), s_get("stor"))
    session.connect(s_get("pass"), s_get("retr"))


def ftp():
    # 创建两个线程，一个运行wire函数，一个运行mqtt_fuzz(main)函数
    wire_thread = threading.Thread(target=wire)
    fuzz_thread = threading.Thread(target=main)

    # 启动线程
    wire_thread.start()
    fuzz_thread.start()

    # 等待线程结束
    wire_thread.join()
    fuzz_thread.join()
    # 运行时可以在http://127.0.0.1:26000/ 查看过程