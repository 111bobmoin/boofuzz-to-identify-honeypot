from boofuzz import *
import subprocess
import threading

def wire():
    # 定义要监视的网络接口
    interface = "以太网 4"

    # 定义要保存捕获数据的文件名
    output_file = "ssh.pcap"

    # 提供Wireshark可执行文件的完整路径
    wireshark_path = r"D:\wireshark\Wireshark.exe"

    # 使用subprocess启动Wireshark并捕获数据
    command = [wireshark_path, "-i", interface, "-k", "-w", output_file]
    subprocess.run(command)

def ssh_fuzz():
    # 创建一个Boofuzz会话
    session = Session(
        target=Target(
            connection=TCPSocketConnection(
                "192.168.81.130",  # SSH服务器的IP地址
                22            # SSH服务器的端口
            )
        ),
    )

    # 定义SSH协议模糊测试
    s_initialize(name="SSH_Version")
    s_string("SSH-2.0-Boofuzz\r\n")


    # 定义SSH会话协议
    with s_block("SSH_KEX_Init"):
        s_string("SSH-2.0-Boofuzz\r\n")
        s_string("cookie")
        s_static("\x00\x00\x00\x13")  # 消息长度
        s_string("ssh-rsa")  # 支持的加密算法
        s_string("diffie-hellman-group-exchange-sha1")
        s_string("ssh-dss")
        s_string("ssh-rsa")

        # 发送消息
        s_block_start("SSH_Version")
        s_block_end()
        s_block_start("SSH_KEX_Init")
        s_block_end()

    s_initialize(name="SSH_Auth")

    # 定义SSH认证
    with s_block("SSH_Auth"):
        s_string("xiaowang")  # 替换为实际用户名
        s_static("\x00\x00\x00\x08")  # 预期的用户名长度
        s_string("030717")  # 替换为实际密码
        s_static("\x00\x00\x00\x08")  # 预期的密码长度

    s_initialize(name="SSH_Execute_Command")

    # 定义SSH执行命令
    with s_block("SSH_Execute_Command"):
        s_string("ls")  # 替换为要执行的命令
        s_static("\x00\x00\x00\x02")  # 预期的命令长度
        s_string("ps")
        s_static("\x00\x00\x00\x02")
        s_string("mkdir ls")
        s_static("\x00\x00\x00\x0A")

    # 增加更多的边界情况和SSH细节

    s_initialize(name="SSH_KEX_DH_Init")

    with s_block("SSH_KEX_DH_Init"):
        s_string("ssh-rsa")  # 替换为支持的密钥交换算法
        s_string("ssh-dss")
        s_string("ssh-rsa")
        s_static("\x00\x00\x00\x08")  # 预期的密钥交换参数长度

    s_initialize(name="SSH_Channel_Request")

    with s_block("SSH_Channel_Request"):
        s_string("session")
        s_static("\x00\x00\x00\x01")  # 预期的通道类型长度
        s_string("exec")
        s_static("\x00\x00\x00\x03")  # 预期的子通道请求类型长度
        s_string("ls")  # 替换为要执行的命令
        s_static("\x00\x00\x00\x02")  # 预期的命令长度

    # 执行模糊测试
    session.connect(s_get("SSH_Version"))
    session.connect(s_get("SSH_Auth"), s_get("SSH_Execute_Command"))
    session.connect(s_get("SSH_Version"), s_get("SSH_KEX_DH_Init"))
    session.connect(s_get("SSH_Execute_Command"), s_get("SSH_Channel_Request"))
    session.fuzz()

def ssh():
    # 创建两个线程，一个运行wire函数，一个运行ssh_fuzz函数
    wire_thread = threading.Thread(target=wire)
    fuzz_thread = threading.Thread(target=ssh_fuzz)

    # 启动线程
    wire_thread.start()
    fuzz_thread.start()

    # 等待线程结束
    wire_thread.join()
    fuzz_thread.join()
    # 运行时可以在http://127.0.0.1:26000/ 查看过程
