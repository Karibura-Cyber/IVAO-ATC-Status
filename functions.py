RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"
msg_id = {}
class log(object):
    def success(msg:str):
        print(f"[{GREEN}SUCCESS{RESET}] {msg}")

    def danger(msg:str):
        print(f"[{RED}DANGER{RESET}] {msg}")

    def warning(msg:str):
        print(f"[{YELLOW}WARNING{RESET}] {msg}")

    def error(msg:str):
        print(f"[{RED}ERROR{RESET}] {msg}")

class message(object):
    def add_id(icao:str, id:int):
        msg_id[icao] = id
    
    def get_id():
        return msg_id