def format(string, *args):
    formatted_string = string
    for arg in args:
        formatted_string = formatted_string.replace("{}", str(arg), 1)
    return formatted_string
