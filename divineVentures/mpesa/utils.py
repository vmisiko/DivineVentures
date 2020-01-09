from datetime import datetime

def formatted_time():
    unformated_time = datetime.now()
    formated_time = unformated_time.strftime("%Y%m%d%H%M%S")
    # print(formated_time, " this is formatted time")

    return formated_time