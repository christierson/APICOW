import time
from machine import Pin, PWM
from dht import DHT22


class Types:
    NONE = None
    INP = "inp"
    OUT = "out"
    PWM = "pwm"
    DHT = "dht"


class Component:
    def __init__(self, pin_number, name="Empty") -> None:
        self.pin_number = pin_number
        self.available = True
        self.type = Types.NONE
        self.name = name
        self.pin = Pin(pin_number)
        self.value = 0
        self.init_pin()

    def init_pin(self):
        print(f"Initialized pin {self.pin_number}")

    def read(self):
        return "This pin cannot be read"

    def write(self, value):
        return "This pin cannot be written to"

    def serialize(self):
        return {
            "pin": self.pin_number,
            "type": self.type,
            "name": self.name,
            "value": self.value,
        }

    def __str__(self) -> str:
        return f"{self.pin_number}: {self.name} ({self.type})"


class DHTComponent(Component):

    def init_pin(self) -> None:
        self.pin = DHT22(self.pin)
        self.type = Types.DHT
        self.available = False
        print(f"Created DHT component on pin {self.pin_number}")

    def read(self):
        self.pin.measure()
        temp = self.pin.temperature()
        hum = self.pin.humidity()
        self.value = {"temperature": temp, "humidity": hum}
        print(f"Reading {self.value} from pin {self.pin_number}")
        return self.value


class PWMComponent(Component):

    def init_pin(self) -> None:
        self.available = False
        self.type = Types.PWM
        self.freq = 20000
        self.max = 65535
        self.min = 0
        self.value = 0
        self.pin = PWM(self.pin)
        self.pin.freq(self.freq)
        self.pin.duty_u16(self.value)
        print(
            f"Created PWM component on pin {self.pin_number} (value: 0-1023)")

    def write(self, value):
        if not (0 <= value <= 1):
            return f"Invalid value, please enter value 0-1, i.e. 0.5"
        self.value = value
        self.pin.duty_u16(round(value*self.max))
        print(f"Wrote {value} to pin {self.pin_number}")
        return f"Wrote {value} to pin {self.pin_number}"

    def read(self):
        print(f"Reading {self.value} from pin {self.pin_number}")
        return self.value


class GPIComponent(Component):
    def init_pin(self) -> None:
        self.available = False
        self.type = Types.INP
        self.pin = Pin(self.pin_number, Pin.IN)
        print(
            f"Created input component on pin {self.pin_number} (value: 0 or 1)")

    def read(self):
        return self.pin.value()


class GPOComponent(Component):
    def init_pin(self) -> None:
        self.available = False
        self.type = Types.OUT
        self.pin = Pin(self.pin_number, Pin.OUT)
        print(f"Created output component on pin {self.pin_number}")

    def write(self, value):
        self.value = value
        self.pin.value(value)
        print(f"Wrote {value} to pin {self.pin_number}")
        return f"Wrote {value} to pin {self.pin_number}"

    def read(self):
        print(f"Reading {self.value} from pin {self.pin_number}")
        return self.value


COMPONENTS = {
    Types.NONE: Component,
    Types.PWM: PWMComponent,
    Types.DHT: DHTComponent,
    Types.OUT: GPOComponent,
    Types.INP: GPIComponent,
}
