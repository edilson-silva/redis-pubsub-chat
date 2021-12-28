from threading import Thread
from connection.redis_connection import Connection
from typing import Any

connection = Connection()

my_user_name = ''


while True:
    # Getting chat user name and generate your unique identifier
    my_user_name = input('Please, enter your name: ').strip().lower()

    is_available = connection.is_available_chat_username(my_user_name)
    
    if is_available:
        break
    
    print(f'Username {my_user_name} is unavailable, please try again\n')


def on_failure(_: Any, redis_pubsub: Any, chat_thread: Thread):
    """Manipulate exceptions on receive message process

    Args:
        _ (str): An empty value (iscard value)
        redis_pubsub (Any): The PubSub connection object
        chat_thread (Thread): The chat thread object
    """
    pass    

def on_new_message(message):
    print(message)

chat_name = input('\nEnter the chat name: ').strip().lower()
connection.join_in_chat(on_new_message_callback=on_new_message, on_failure_callback=on_failure, chat_name=chat_name)


# Getting user message to publish
while True:
    message = input('Please, enter a message: ')
    connection.send_message_to_chat(username=my_user_name, chat_name=chat_name, message=message)
