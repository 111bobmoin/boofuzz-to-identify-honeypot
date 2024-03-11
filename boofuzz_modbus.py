from boofuzz import *
import subprocess
import threading

def wire():
    # 定义要监视的网络接口
    interface = "以太网 4"

    # 定义要保存捕获数据的文件名
    output_file = "modbus.pcap"

    # 提供Wireshark可执行文件的完整路径
    wireshark_path = r"D:\wireshark\Wireshark.exe"

    # 使用subprocess启动Wireshark并捕获数据
    command = [wireshark_path, "-i", interface, "-k", "-w", output_file]
    subprocess.run(command)

def modbus_fuzz():
    # 创建一个会话
    session = Session(
        target=Target(
            connection=TCPSocketConnection("192.168.81.130", 502)  # Modbus默认端口
        ),
    )

    # 定义Modbus协议的测试用例
    s_initialize("ModbusTransaction")

    # 添加更多功能码
    for func_code in ["01", "02", "03", "04", "05", "06", "0F", "10"]:
        s_string("00", fuzzable=True)  # Modbus事务标识符
        s_string("00", fuzzable=True)  # 协议标识符
        s_string("0006", fuzzable=True)  # 长度字段
        s_string("01", fuzzable=True)  # 单元标识符
        s_string(func_code, fuzzable=True)  # 不同功能码
        s_string("0000", fuzzable=True)  # 起始地址
        s_string("0001", fuzzable=True)  # 读取数量

    # 添加多单元标识符
    for unit_id in ["01", "02", "03"]:
        s_string("00", fuzzable=True)  # Modbus事务标识符
        s_string("00", fuzzable=True)  # 协议标识符
        s_string("0006", fuzzable=True)  # 长度字段
        s_string(unit_id, fuzzable=True)  # 不同单元标识符
        s_string("01", fuzzable=True)  # 功能码 01 (读线圈)
        s_string("0000", fuzzable=True)  # 起始地址
        s_string("0001", fuzzable=True)  # 读取数量

    # 添加不同数据长度
    for data_length in ["0001", "0003", "0008"]:
        s_string("00", fuzzable=True)  # Modbus事务标识符
        s_string("00", fuzzable=True)  # 协议标识符
        s_string(data_length, fuzzable=True)  # 不同数据长度
        s_string("01", fuzzable=True)  # 单元标识符
        s_string("01", fuzzable=True)  # 功能码 01 (读线圈)
        s_string("0000", fuzzable=True)  # 起始地址
        s_string("0001", fuzzable=True)  # 读取数量

    # 添加不同地址范围和边界情况
    s_string("00", fuzzable=True)  # Modbus事务标识符
    s_string("00", fuzzable=True)  # 协议标识符
    s_string("0006", fuzzable=True)  # 长度字段
    s_string("01", fuzzable=True)  # 单元标识符
    s_string("01", fuzzable=True)  # 功能码 01 (读线圈)
    s_string("0000", fuzzable=True)  # 起始地址（边界情况）
    s_string("FFFF", fuzzable=True)  # 读取数量（最大值）

    # 错误处理
    s_string("00", fuzzable=True)  # Modbus事务标识符
    s_string("00", fuzzable=True)  # 协议标识符
    s_string("0006", fuzzable=True)  # 长度字段
    s_string("01", fuzzable=True)  # 单元标识符
    s_string("01", fuzzable=True)  # 功能码 01 (读线圈)
    s_string("0000", fuzzable=True)  # 起始地址
    s_string("FFFF", fuzzable=True)  # 读取数量（错误的数量）

    #  数据类型和异常响应
    s_string("00", fuzzable=True)  # Modbus事务标识符
    s_string("00", fuzzable=True)  # 协议标识符
    s_string("0006", fuzzable=True)  # 长度字段
    s_string("01", fuzzable=True)  # 单元标识符
    s_string("01", fuzzable=True)  # 功能码 01 (读线圈)
    s_string("0000", fuzzable=True)  # 起始地址
    s_string("0001", fuzzable=True)  # 读取数量
    s_string("01", fuzzable=True)  # 异常响应功能码

    # 交互序列
    s_string("00", fuzzable=True)  # Modbus事务标识符
    s_string("00", fuzzable=True)  # 协议标识符
    s_string("0006", fuzzable=True)  # 长度字段
    s_string("01", fuzzable=True)  # 单元标识符
    s_string("05", fuzzable=True)  # 功能码 05 (写单个线圈)
    s_string("0000", fuzzable=True)  # 起始地址
    s_string("0001", fuzzable=True)  # 写入数量
    s_string("01", fuzzable=True)  # 写入字节计数
    s_string("01", fuzzable=True)  # 写入值

    # 发送测试用例
    session.connect(s_get("ModbusTransaction"))

    # 执行模糊测试
    session.fuzz()

def modbus():
    # 创建两个线程，一个运行wire函数，一个运行modbus_fuzz函数
    wire_thread = threading.Thread(target=wire)
    fuzz_thread = threading.Thread(target=modbus_fuzz)

    # 启动线程
    wire_thread.start()
    fuzz_thread.start()

    # 等待线程结束
    wire_thread.join()
    fuzz_thread.join()
    # 运行时可以在http://127.0.0.1:26000/ 查看过程
