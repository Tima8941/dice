from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

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

        self.logbox = BoxLayout(orientation="vertical")
        self.input_login = TextInput()
        self.input_password = TextInput()
        self.btn_signup = Button(text = "sign up")

        self.logbox.add_widget(self.input_login)
        self.logbox.add_widget(self.input_password)
        self.logbox.add_widget(self.btn_signup)


        self.login_win = Popup()
        self.login_win.open()
        #start thread !!!
        threading.Thread(target=self.listen_server, daemon=True).start()

        return self.layout
    
    def signup(self, btn):
        login, password = self.input_login.text, self.input_password.text

        msg = json.dumps({"cmd":"add_user", "login":login, "password":password})

        try:
            self.sock.sendall(msg.encode())
        except:
            pass

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