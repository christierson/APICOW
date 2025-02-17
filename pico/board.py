from component import Component, COMPONENTS
from machine import Pin
from utime import sleep
import json
# NON_GP = [3, 8, 13, 18, 23, 28, 30, 33, 35, 36, 37, 38, 39, 40]
IDK1 = 23
IDK2 = 24
IDK3 = 25
LED = 0
NON_GPIO = [IDK1, IDK2, IDK3, LED]
GPIO = [pin for pin in range(29) if pin not in NON_GPIO]


class Board:
    def __init__(self) -> None:
        self.load_default()
        self.led = Pin(LED, Pin.OUT)
        print("Created board")
        for component in self.board.values():
            print(str(component))
        self.blink()

    def available_pins(self):
        return [key for key, value in self.board.items() if value.available]
    
    def blink(self):
        self.led.value(1)
        sleep(0.2)
        self.led.value(0)

    
    def get_default(self):
        try:
            with open("boardconfig.json", "r") as fp:
                default = json.loads(fp.read())
                for pin, component in default.items():
                    if int(pin) not in GPIO:
                        raise Exception("Invalid pin in config file.")
        except Exception as e:
            print("CREATING NEW DEFAULT FILE -", e)
            default = {pin: {
                "pin": pin,
                "type": None,
                "name": "Empty",
                "value": 0,
                } for pin in GPIO}
            with open("boardconfig.json", "w") as fp:
                fp.write(json.dumps(default))
        return default
    
    def load_default(self):
        self.board = {}
        default = self.get_default()
        for c in default.values():
            C = COMPONENTS[c["type"]]
            instance = C(c["pin"], c["name"])
            self.board[c["pin"]] = instance
        return "Loaded default board"

    def save_default(self):
        with open("boardconfig.json", "w") as fp:
            fp.write(json.dumps(self.serialize()))
        return "Saved current board as default"

    def get_board(self):
        return self.serialize()

    def serialize(self):
        d = {n: pin.serialize() for n, pin in self.board.items()}
        print("Serialized:", d)
        return d

    def recieve(self, data):
        print(data)
        self.blink()
        command = data.get('command')
        if not command:
            raise ValueError("No command provided in the data")
        command_method = getattr(self, command, None)
        if not command_method:
            raise ValueError(f"Command '{command}' not found")
        args = data.get('args', [])
        kwargs = data.get('kwargs', {})
        self.blink()
        return command_method(*args, **kwargs)

    def read(self, pin):
        pin = self.board.get(pin)
        if not pin:
            return f"Invalid pin - valid pins: {list(self.board.keys())}"
        return pin.read()

    def write(self, pin, value):
        pin = self.board.get(pin)
        if not pin:
            return f"Invalid pin - valid pins: {list(self.board.keys())}"
        return pin.write(value)
    
    def set_board(self, data):
        result = ""
        for component_data in data.values():
            pin = component_data["pin"]
            name = component_data["name"]
            mode = component_data["type"] 
            result +=f"{pin}: {set_pin(pin, name, mode)}\n" 
        return result
        
    def set_pin(self, pin, name, mode):
        if pin not in self.board:
            return f"Invalid pin - valid pins: {list(self.board.keys())}"
        mode = COMPONENTS.get(mode)
        if not mode:
            return f"Unknown mode - valid modes: {list(COMPONENTS.keys())}"
        component = mode(pin, name)

        self.board[pin] = component
        return f"Created {str(component)}"

    def help(self):
        return {"Commands": {
            "load_default": {
                "action": "Loads board config from file, creates one if needed"
            },
            "save_default": {
                "action": "Saves the current board setup into config file"
            },
            "help": {
                "returns": "This message"
            },
            "get_board": {
                "returns": "The current state of the board config"
            },
            "read": {
                "returns": "The value of a pin",
                "required arguments": {
                    "pin": "The pin number for the pin you want to read"
                }
            },
            "write": {
                "action": "Sets the value of a pin",
                "returns": "The value of a pin",
                "required arguments": {
                    "pin": "The pin number for the pin you want to write to",
                    "value": "The value you want to write"
                }
            },
            "pin": {
                "action": "Sets the name and type for a pin",
                "returns": "The resulting state of the board",
                "required arguments": {
                    "pin": "The number of the pin",
                    "name": "Pin name for later reference",
                    "mode": "Desired component type: {\"INP\": 1, \"OUT\": 2, \"DHT\": 3, \"PWM\": 4}"
                }
            }
        }
        }


class Routine:
    def __init__(self):
        self.counter = -1
        self.data = {}
        
    def store(self, key, value):
        self.data[key] = value
        
    def load(self, key):
        return self.data[key]
    
    def run(self):
        counter += 1
        return self._run()
        
    def _run(self):
        raise NotImplementedError