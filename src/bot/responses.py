# Get responses will take in a string and then return a string.
def get_responses(message: str) -> str:
    p_message = message.lower()

    if p_message == 'hello':
        return "Hey there!"
    
    if p_message == "!help":
        return "`This is a help message that you can modify.`"
    
    return "I didn't understand what you wrote. Try typing '!help'."