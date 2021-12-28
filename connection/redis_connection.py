from redis import Redis

class Connection:
    
    def __init__(self, host: str = 'localhost', port: int = 6379) -> None:
        self.__connection = Redis(host=host, port=port)
        print(f'Redis connected on port {port}')
