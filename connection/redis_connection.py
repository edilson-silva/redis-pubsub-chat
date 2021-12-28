import json

from redis import Redis
from exception.invalid_chat_username_exception import InvalidChatUsername
from exception.invalid_chat_name_exception import InvalidChatName
from types import FunctionType

class Connection:
    
    __PUBLIC_CHAT_WITH_ALL_USERS = 'all'
    
    def __init__(self, host: str = 'localhost', port: int = 6379) -> None:
        """Start a new Redis connection

        Args:
            host (str, optional): The host connection URL. Defaults to 'localhost'.
            port (int, optional): The host connection PORT. Defaults to 6379.
        1"""
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

    def join_in_chat(self, on_new_message_callback: FunctionType, on_failure_callback: FunctionType, chat_name: str = __PUBLIC_CHAT_WITH_ALL_USERS):
        """Join in specific chat based on chat name

        Args:
            on_new_message_callback (FunctionType): A function to hanle new messages that will be receive an unique dict parameter as a message
            on_failure_callback (FunctionType): A function to handle any exception on receive message process
            chat_name (str, optional): The chat name to join. Defaults to __PUBLIC_CHAT_WITH_ALL_USERS
        """
        self.__pubsub_client.psubscribe(**{chat_name: on_new_message_callback})
        chat_thread = self.__pubsub_client.run_in_thread(sleep_time=0.001, daemon=True, exception_handler=on_failure_callback)
        self.__my_chats.append(chat_name)

    def send_message_to_chat(self, username: str, message: str, chat_name: str = __PUBLIC_CHAT_WITH_ALL_USERS):
        """Send message to specific chat based on your name

        Args:
            username (str): Name of user that will be publish message
            message (str): The message content
            chat_name (str, optional): Publish message chat name. Defaults to __PUBLIC_CHAT_WITH_ALL_USERS.
        """        
        username = username.strip()
        
        if not username:
            raise InvalidChatUsername('Please, send username')
        
        chat_name = chat_name.strip()
        
        if not chat_name:
            raise InvalidChatName('Please, send chat name')
        
        message = message.strip()
        
        if message:
            data = json.dumps({
                'username': username,
                'message': message
            })

            self.__connection.publish(chat_name, data)
