import threading
from redis import Redis
from exception.invalid_chat_username_exception import InvalidChatUsername
from exception.invalid_chat_name_exception import InvalidChatName
from types import FunctionType

class Connection:
    
    __PUBLIC_CHAT_WITH_ALL_USERS = 'all'
    
    def __init__(self, host: str = 'localhost', port: int = 6379) -> None:
        self.__users_list_control = 'users'
        self.__connection = Redis(host=host, port=port)
        self.__pubsub_client = self.__connection.pubsub()
        self.__my_chats = []
        print(f'Redis connected on port {port}\n')

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

    def join_in_chat(self, on_new_message_callback: FunctionType, on_failure_callback: FunctionType, name: str = __PUBLIC_CHAT_WITH_ALL_USERS):
        """Join in specific chat based on chat name

        Args:
            on_new_message_callback (FunctionType): A function to hanle new messages that will be receive an unique dict parameter as a message
            on_failure_callback (FunctionType): [description]
            name (str, optional): The chat name to join. Defaults to __PUBLIC_CHAT_WITH_ALL_USERS.
        """
        self.__pubsub_client.psubscribe(**{name: on_new_message_callback})
        chat_thread = self.__pubsub_client.run_in_thread(sleep_time=0.001, daemon=True, exception_handler=on_failure_callback)
        self.__my_chats.append(chat_thread)
