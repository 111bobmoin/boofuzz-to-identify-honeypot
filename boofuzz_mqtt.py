from boofuzz import *
import subprocess
import threading

def wire():
    # 定义要监视的网络接口
    interface = "以太网 4"

    # 定义要保存捕获数据的文件名
    output_file = "mqtt.pcap"

    # 提供Wireshark可执行文件的完整路径
    wireshark_path = r"D:\wireshark\Wireshark.exe"

    # 使用subprocess启动Wireshark并捕获数据
    command = [wireshark_path, "-i", interface, "-k", "-w", output_file]
    subprocess.run(command)

def mqtt_fuzz():
    session = Session(
        target=Target(
            connection=TCPSocketConnection("192.168.81.130", 1883)
        ),
    )

    s_initialize("MQTTConnect")
    s_static("MQTT")  # MQTT Protocol Name
    s_byte(4, "ProtocolLevel")
    s_bit_field(0, 4, "Flags")
    s_byte(0, "KeepAlive")
    s_string("ClientID", max_len=23)
    s_string("WillTopic", max_len=23)
    s_string("WillMessage", max_len=23)
    s_string("Username", max_len=23)
    s_string("Password", max_len=23)

    s_initialize("MQTTSubscribe")
    s_byte(0x82, "PacketType")
    s_word(0, "PacketID")
    s_string("Topic", max_len=23)
    s_byte(0, "QoS")

    s_initialize("MQTTPublish")
    s_byte(0x30, "PacketType")
    s_string("Topic", max_len=23)
    s_string("Message", max_len=50)

    session.connect(s_get("MQTTConnect"))
    session.connect(s_get("MQTTConnect"), s_get("MQTTSubscribe"))
    session.connect(s_get("MQTTConnect"), s_get("MQTTPublish"))
    session.fuzz()


def mqtt():
    # 创建两个线程，一个运行wire函数，一个运行mqtt_fuzz函数
    wire_thread = threading.Thread(target=wire)
    fuzz_thread = threading.Thread(target=mqtt_fuzz)

    # 启动线程
    wire_thread.start()
    fuzz_thread.start()

    # 等待线程结束
    wire_thread.join()
    fuzz_thread.join()
    # 运行时可以在http://127.0.0.1:26000/ 查看过程
