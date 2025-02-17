import network
import usocket as socket
import json
import re
from secrets import SSID, PASSWORD

class API:
    def __init__(self, func):
        self.connect_wifi()
        self.host = "0.0.0.0"
        self.func = func
        self.port = 8080
        self.server = socket.socket(socket.AF_INET)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print("Server listening on", self.host, "port", self.port)

    def recv(self):
        print("Waiting for client")
        self.client_socket, addr = self.server.accept()
        print("Client connected from", addr)
        return self.client_socket.recv(1024)

    def error_response(self, error):
        try:
            response = json.dumps(error)
            self.client_socket.send("HTTP/1.1 500 Internal Server Error\r\n")
            self.client_socket.send("Content-Type: application/json\r\n")
            self.client_socket.send(
                "Content-Length: {}\r\n\r\n".format(len(response)))
            self.client_socket.send(response.encode('utf-8'))
        except Exception as e:
            print(e)
        finally:
            self.client_socket.close()

    def response(self, data={}):
        try:
            response = json.dumps(data)
            self.client_socket.send("HTTP/1.1 200 OK\r\n")
            self.client_socket.send("Content-Type: application/json\r\n")
            self.client_socket.send(
                "Content-Length: {}\r\n\r\n".format(len(response)))
            self.client_socket.send(response.encode('utf-8'))
        except Exception as e:
            print(e)
        finally:
            self.client_socket.close()

    def run(self):
        try:
            while True:
                try:
                    request = self.recv()
                    data = self.handle_request(request)
                except Exception as e:
                    self.error_response(f"Error recieving request: {e}")
                try:
                    response_data = self.func(data)
                    self.response(response_data)
                except Exception as e:
                    self.error_response(f"Error processing request: {e}")
        except Exception as e:
            print(e)
            self.server.close()

    def handle_request(self, request):
        request = request.decode()
        data = request.split("\n")[-1]
        data = json.loads(data)
        return data

    def connect_wifi(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            print("Connecting to WiFi...")
            wlan.connect(SSID, PASSWORD)
            while not wlan.isconnected():
                pass
        print("Connected to WiFi:", SSID)
        print("IP Address:", wlan.ifconfig()[0])
