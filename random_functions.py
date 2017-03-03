# random_functions.py
def get_chatbot_response(message):
    
    if message[:2] == '!!':
        return 'Woosh'
    else:
        return 'Not a command'