import json

from threading import Thread
from connection.redis_connection import Connection
from typing import Any

connection = Connection()

my_username = ''


while True:
    # Getting chat user name and generate your unique identifier
    my_username = input('Please, enter your name: ').strip().lower()

    is_available = connection.is_available_chat_username(my_username)
    
    if is_available:
        break
    
    print(f'Username {my_username} is unavailable, please try again\n')


def on_failure(_: Any, redis_pubsub: Any, chat_thread: Thread):
    """Manipulate exceptions on receive message process

    Args:
        _ (str): An empty value (iscard value)
        redis_pubsub (Any): The PubSub connection object
        chat_thread (Thread): The chat thread object
    """
    pass    

def on_new_message(message: dict):
    """Receive a new message

    Args:
        message (dict): New received message
    """
    if message:
        message_type = message['type']
        
        if message_type == 'pmessage':
            message = message['data'].decode('utf-8')  # Retrieve string from byte array
            message = json.loads(message)  # Parse string to dict
            
            username = message.get('username', '')
            message = message.get('message', '').strip()
            
            if message and username and username != my_username:
                print(f'\n{username.upper()}: {message}')
                raise Exception
        else:
            print(f'Event: {message_type}') 


chat_name = input('\nEnter the chat name: ').strip().lower()
connection.join_in_chat(on_new_message_callback=on_new_message, on_failure_callback=on_failure, chat_name=chat_name)


# Getting user message to publish
while True:
    message = input('Please, enter a message: ')
    connection.send_message_to_chat(username=my_username, chat_name=chat_name, message=message)
