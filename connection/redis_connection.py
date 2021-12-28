from redis import Redis
from exception.invalid_chat_username_exception import InvalidChatUsername

class Connection:

    def __init__(self, host: str = 'localhost', port: int = 6379) -> None:
        self.__users_list_control = 'users'
        self.__connection = Redis(host=host, port=port)
        print(f'Redis connected on port {port}')

    def is_available_chat_username(self, username: str) -> bool:
        """Verify if username is available to join in the chat

        Args:
            username (str): Username to verify

        Returns:
            bool: True if available and false otherwise
        """
        if not username.strip():
            raise InvalidChatUsername('Please, send username')
        
        index = self.__connection.lpos(self.__users_list_control, username)
        return index is None
