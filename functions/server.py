
class Server:
    name = None

    def __str__(self):
        return f'Server: {self.name_cn}, {self.id}'

    def __init__(self, name: str, name_cn: str, name_short: str, server_id: int, ip: str, port: int, channel_id: int):
        self.name = name
        self.name_cn = name_cn
        self.name_short = name_short
        self.id = server_id
        self.ip = ip
        self.port = port
        self.channel_id = channel_id


if __name__ == '__main__':
    pass
