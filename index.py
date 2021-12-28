from connection.redis_connection import Connection

connection = Connection()

my_user_name = ''


while True:
    # Getting chat user name and generate your unique identifier
    my_user_name = input('Please, enter your name: ').strip().lower()

    is_available = connection.is_available_chat_username(my_user_name)
    
    if is_available:
        break
    
    print(f'Username {my_user_name} is unavailable, please try again\n')
