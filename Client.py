from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

from kivy.clock import Clock

import socket
import threading
import json

import faker
fake = faker.Faker()

HOST, PORT = "127.0.0.1", 666

class DiceApp(App):
    def build(self):
        self.sock = socket.socket()
        self.sock.connect((HOST, PORT))

        self.player_name = fake.first_name()

        msg = {"name":self.player_name}

        self.sock.sendall(json.dumps(msg).encode())

        self.layout = BoxLayout(orientation = "vertical")

        self.log = Label(text = "log:\n", font_size = 24, size_hint_y = 0.8)
        self.btn = Button(text = "roll dice", font_size = 24, on_press = self.roll, size_hint_y = 0.2)

        self.layout.add_widget(self.log)
        self.layout.add_widget(self.btn)

        #start thread !!!
        threading.Thread(target=self.listen_server, daemon=True).start()

        return self.layout
    
    def roll(self, btn):
        try:
            msg = {"cmd":"roll"}
            self.sock.sendall(json.dumps(msg).encode())
        except:
            return

    def listen_server(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if not data:
                    break
                msg = json.loads(data.decode()).get("msg")

                Clock.schedule_once(lambda dt: self.update_log(msg))
            except:
                break
    
    def update_log(self, msg):
        self.log.text += msg+"\n"

DiceApp().run()