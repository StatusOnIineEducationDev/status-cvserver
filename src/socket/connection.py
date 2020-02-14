from src.socket.handleRecvFunction import *


def connect():
    # 建立与主服务器的连接
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((HOST, PORT))

    request_data = {
        "command": TransportCmd.CreateCVServerConnection
    }
    # 在c++客户端那里写入长度时会多出4字节，为保持接口统一，这里人为多加4字节（发送两次头部）
    connection.send(struct.pack("!i", len(json.dumps(request_data))))
    connection.send(struct.pack("!i", len(json.dumps(request_data))))
    connection.send(json.dumps(request_data).encode())

    recv(connection)


def recv(connection):
    recv_bytes = bytes()
    pack_len = -1

    while True:
        recv_bytes += connection.recv(1024)
        while True:
            if len(recv_bytes) >= 4 and pack_len == -1:
                pack_len_bytes = recv_bytes[:4]
                pack_len = int.from_bytes(pack_len_bytes, 'big')
                recv_bytes = recv_bytes[4:]

            if len(recv_bytes) >= pack_len != -1:
                json_obj_bytes = recv_bytes[:pack_len]
                json_obj = json.loads(json_obj_bytes)
                recv_bytes = recv_bytes[pack_len:]
                pack_len = -1

                handleRecvData(connection, json_obj)

            if len(recv_bytes) < 4 or pack_len != -1:
                break


def reply(connection, data):
    # 在c++客户端那里写入长度时会多出4字节，为保持接口统一，这里人为多加4字节（发送两次头部）
    connection.send(struct.pack("!i", len(json.dumps(data))))
    connection.send(struct.pack("!i", len(json.dumps(data))))
    connection.send(json.dumps(data).encode())


def handleRecvData(connection, json_obj):
    command = json_obj["command"]

    if command is TransportCmd.StudentCameraFrameData:
        studentCameraFrameData(connection, json_obj)



