import clr, threading, sys, os, bcrypt, subprocess, requests
from datetime import datetime
from time import sleep
from core import status, schema
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import main

__screen_id = 2
__user_id = 0
def change_screen(sc): __screen_id = sc
def get_screen_id(): return __screen_id
def change_id(id): __user_id = id
from enum import Enum

# Load .NET System.Drawing classes
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
from System import Action
from System.Windows.Forms import Label, Form, PictureBox, Application, FormBorderStyle, FormStartPosition, Padding, \
    PictureBoxSizeMode, FormWindowState, DockStyle
from System.Drawing import Font, Color, Point, Size, SizeF, GraphicsUnit, FontStyle, Image, ContentAlignment


class Locked(Form):

    def __init__(self):
        super().__init__()
        self.AutoScaleDimensions = SizeF(7.0, 15.0)  # Auto scaling dimensions
        self.AutoScaleMode = self.AutoScaleMode.Font  # Font scaling (1 = AutoScaleMode.Font)
        self.BackColor = Color.FromArgb(19, 19, 19)  # Background color
        self.ClientSize = Size(480, 320)  # Client size of the form
        self.FormBorderStyle = FormBorderStyle(0)  # No border (0 = FormBorderStyle.None)
        self.MaximizeBox = False  # Disable maximize button
        self.MinimizeBox = False  # Disable minimize button
        self.__Name = "Locked"  # Name of the form
        self.StartPosition = FormStartPosition.CenterScreen  # Center screen (2 = FormStartPosition.CenterScreen)
        self.__Text = "Locked"  # Title of the form


        self.__time = Label()

        self.__time.AutoSize = False
        self.__time.BackColor = Color.Transparent
        self.__time.Font = Font("7 SEGMENTAL DIGITAL DISPLAY", 71.99999, FontStyle.Regular, GraphicsUnit.Point, 0)
        self.__time.ForeColor = Color.White
        self.__time.Location = Point(12, 97)
        self.__time.Name = "time"
        self.__time.Size = Size(456, 103)
        self.__time.TabIndex = 1
        self.__time.TextAlign = ContentAlignment.MiddleCenter
        self.__time.Text = "12:34"
        self.__time.Visible = True
        self.__time.Click += self.leave

        threading.Thread(target=self.update_time_loop, daemon=True).start()

        self.Controls.Add(self.__time)

    def leave(self, sender = None, e = None):
        threading.Thread(target=deploy_numpad, daemon=True).start()
        self.Close()

    def panic_screen(self):
        while True:
            self.BackColor = Color.FromArgb(255, 0, 0)
            sleep(0.125)
            self.BackColor = Color.FromArgb(19, 19, 19)
            sleep(0.125)

    #def get_lock_status(self): return self.__locked_out

    def update_time_loop(self, loop=True):
        while True:
            now = datetime.now()
            secs = now.second
            self.__time.Text = now.strftime("%H:%M")
            if not loop:
                break  # Se 'loop' for false, correr só uma vez
            else:
                sleep(61 - secs)  # Dormir até aos 60 secs

    # def status_updater(self):
    #     while True:
    #         status.updateStatus()
    #         stat = status.getStatus()
    #         if self.__status_num != stat:
    #             self.Hide()
    #             self.Close()
    #         sleep(2)



    def unlock(self):
        if self.__locked_out:
            self.__locked.Visible = False
            if self.__status_num > 0:
                self.__status.Location = Point(181, 142)
                sleep(0.2)
                self.__status.Visible = True
            else:
                self.__time.Visible = False
                self.__time.Location = Point(12, 97)
                self.__time.Visible = True


class HomeScreen(Form):

    def __init__(self, userID):
        super().__init__()
        self.Width = 480
        self.Height = 320

        self.__timeout = 0
        self.__user_ID = userID

        # Form properties
        self.AutoScaleDimensions = SizeF(7.0, 15.0)  # Auto scaling dimensions
        self.AutoScaleMode = self.AutoScaleMode.Font  # Font scaling (1 = AutoScaleMode.Font)
        self.BackColor = Color.FromArgb(19, 19, 19)  # Background color
        self.ClientSize = Size(480, 320)  # Client size of the form
        self.FormBorderStyle = FormBorderStyle(0)  # No border (0 = FormBorderStyle.None)
        self.MaximizeBox = False  # Disable maximize button
        self.MinimizeBox = False  # Disable minimize button
        self.__Name = "Main"  # Name of the form
        self.StartPosition = FormStartPosition.CenterScreen  # Center screen (2 = FormStartPosition.CenterScreen)
        self.__Text = "Home"  # Title of the form

        # Atribuit os elementos
        self.label1 = Label()
        self.arm = PictureBox()
        self.disarm = PictureBox()
        self.part = PictureBox()
        self.pictureBox2 = PictureBox()
        self.pictureBox3 = PictureBox()
        self.pictureBox4 = PictureBox()
        self.settings = PictureBox()
        self.pictureBox6 = PictureBox()

        #
        #  Label 1 - Propriedades
        #
        self.label1.AutoSize = True
        self.label1.Font = Font("Xolonium", 21.75, FontStyle.Bold, GraphicsUnit.Point)
        self.label1.ForeColor = Color.White
        self.label1.Location = Point(349, 9)
        self.label1.Name = "label1"
        self.label1.Size = Size(119, 32)
        self.label1.TabIndex = 0
        self.label1.Text = "12:34"
        #
        #  Arm - Properties
        #
        self.arm.Image = Image.FromFile(
            getImgDir("locked.png"))  # Voltar uma pasta atrás, e ir a 'resized' buscar a imagem
        self.arm.Location = Point(41, 131)
        self.arm.Name = "arm"
        self.arm.Size = Size(51, 56)
        self.arm.TabIndex = 1
        self.arm.TabStop = False
        self.arm.Tag = 1
        self.arm.Click += self.change_stat
        # self.arm.Click += self.arm_Click
        #
        #  Disarm - Properties
        #
        self.disarm.Image = Image.FromFile(getImgDir("unlock.png"))
        self.disarm.Location = Point(146, 131)
        self.disarm.Name = "disarm"
        self.disarm.Size = Size(51, 56)
        self.disarm.TabIndex = 2
        self.disarm.TabStop = False
        self.disarm.Tag = 0
        self.disarm.Click += self.change_stat
        #
        #  Part - Properties
        #
        self.part.Image = Image.FromFile(getImgDir("inside.png"))
        self.part.Location = Point(256, 131)
        self.part.Name = "part"
        self.part.Size = Size(51, 56)
        self.part.TabIndex = 3
        self.part.TabStop = False
        self.part.Tag = 2
        self.part.Click += self.change_stat
        #
        # Settings - Properties
        #
        self.settings.Image = Image.FromFile(getImgDir("settings.png"))
        self.settings.Location = Point(366, 131)
        self.settings.Name = "settings"
        self.settings.Size = Size(55, 56)
        self.settings.TabIndex = 8
        self.settings.TabStop = False
        #
        # Red Cover
        #
        self.pictureBox2.BackColor = Color.Red
        self.pictureBox2.Location = Point(31, 122)
        self.pictureBox2.Name = "pictureBox2"
        self.pictureBox2.Size = Size(72, 75)
        self.pictureBox2.TabIndex = 5
        self.pictureBox2.TabStop = False
        #
        # Green Cover
        #
        self.pictureBox3.BackColor = Color.LimeGreen
        self.pictureBox3.Location = Point(135, 121)
        self.pictureBox3.Name = "pictureBox3"
        self.pictureBox3.Size = Size(72, 75)
        self.pictureBox3.TabIndex = 6
        self.pictureBox3.TabStop = False
        #
        # Orange Cover
        #
        self.pictureBox4.BackColor = Color.FromArgb(255, 128, 0)
        self.pictureBox4.Location = Point(245, 121)
        self.pictureBox4.Name = "pictureBox4"
        self.pictureBox4.Size = Size(72, 75)
        self.pictureBox4.TabIndex = 7
        self.pictureBox4.TabStop = False
        #pictureBox4.Click += pictureBox4_Click;
        #
        # Purple Cover
        #
        self.pictureBox6.BackColor = Color.FromArgb(78, 3, 252)
        self.pictureBox6.Location = Point(356, 121)
        self.pictureBox6.Name = "pictureBox6"
        self.pictureBox6.Size = Size(75, 75)
        self.pictureBox6.TabIndex = 9
        self.pictureBox6.TabStop = False

        # Initialize controls (these would be your previously defined controls)
        self.Controls.Add(self.settings)
        self.Controls.Add(self.arm)
        self.Controls.Add(self.pictureBox2)
        self.Controls.Add(self.disarm)
        self.Controls.Add(self.part)
        self.Controls.Add(self.label1)
        self.Controls.Add(self.pictureBox3)
        self.Controls.Add(self.pictureBox4)
        self.Controls.Add(self.pictureBox6)

        # Atualizar a hora automaticamente
        threading.Thread(target=self.update_time_loop, daemon=True).start()

    def change_stat(self, sender = None, e = None):
        action = sender.Tag
        if action == 0: status.disarm(self.__user_ID, False)
        elif action == 1: status.delayArming(self.__user_ID, False)
        elif action == 2: status.part(self.__user_ID, False)
        threading.Thread(target=deploy_lock, daemon=True).start()
        self.Close()
    def update_time_loop(self, loop=True):
        while True:
            now = datetime.now()
            secs = now.second
            self.label1.Text = now.strftime("%H:%M")
            if not loop:
                break  # Se 'loop' for false, correr só uma vez
            else:
                sleep(61 - secs)  # Dormir até aos 60 secs


class numpad(Form):

    def __init__(self):
        super().__init__()
        self.__Width = 480
        self.__Height = 320


        # Variável que tem o PIN
        self.__PinEntered = ""

        self.__wrongAttempts = 0
        self.__timeouts = 0
        self.__timers = (1, 2, 4, 8, 10)
        self.__timeout = 0

        # Array de botões
        self.__buttons = []
        # Declarar os elementos
        self.__b1 = Label()
        self.__bt2 = Label()
        self.__bt3 = Label()
        self.__bt5 = Label()
        self.__b8 = Label()
        self.__b0 = Label()
        self.__bt6 = Label()
        self.__bt4 = Label()
        self.__bt7 = Label()
        self.__bt9 = Label()
        self.__label1 = Label()
        self.submit = PictureBox()
        self.__delete = PictureBox()

        # bt1
        self.__b1.AutoSize = True
        self.__b1.Font = Font("Xolonium", 27.75, FontStyle.Bold | FontStyle.Italic, GraphicsUnit.Point, 0)
        self.__b1.ForeColor = Color.White
        self.__b1.Location = Point(76, 45)
        self.__b1.Name = "b1"
        self.__b1.Padding = Padding(25, 15, 25, 15)
        self.__b1.Size = Size(99, 71)
        self.__b1.TabIndex = 0
        self.__b1.Text = "1"
        self.__b1.Tag = '1'
        self.__b1.TextAlign = ContentAlignment.MiddleCenter
        self.__b1.Click += self.__add_num

        # bt2
        self.__bt2.AutoSize = True
        self.__bt2.Font = Font("Xolonium", 27.75, FontStyle.Bold | FontStyle.Italic, GraphicsUnit.Point, 0)
        self.__bt2.ForeColor = Color.White
        self.__bt2.Location = Point(190, 45)
        self.__bt2.Name = "bt2"
        self.__bt2.Padding = Padding(25, 15, 25, 15)
        self.__bt2.Size = Size(99, 71)
        self.__bt2.TabIndex = 1
        self.__bt2.Text = "2"
        self.__bt2.Tag = '2'
        self.__bt2.TextAlign = ContentAlignment.MiddleCenter
        self.__bt2.Click += self.__add_num

        # bt3
        self.__bt3.AutoSize = True
        self.__bt3.Font = Font("Xolonium", 27.75, FontStyle.Bold | FontStyle.Italic, GraphicsUnit.Point, 0)
        self.__bt3.ForeColor = Color.White
        self.__bt3.Location = Point(295, 45)
        self.__bt3.Name = "bt3"
        self.__bt3.Padding = Padding(25, 15, 25, 15)
        self.__bt3.Size = Size(99, 71)
        self.__bt3.TabIndex = 7
        self.__bt3.Text = "3"
        self.__bt3.Tag = '3'
        self.__bt3.TextAlign = ContentAlignment.MiddleCenter
        self.__bt3.Click += self.__add_num

        # bt4
        self.__bt4.AutoSize = True
        self.__bt4.Font = Font("Xolonium", 27.75, FontStyle.Bold | FontStyle.Italic, GraphicsUnit.Point, 0)
        self.__bt4.ForeColor = Color.White
        self.__bt4.Location = Point(76, 105)
        self.__bt4.Name = "bt4"
        self.__bt4.Padding = Padding(25, 15, 25, 15)
        self.__bt4.Size = Size(99, 71)
        self.__bt4.TabIndex = 12
        self.__bt4.Text = "4"
        self.__bt4.Tag = '4'
        self.__bt4.TextAlign = ContentAlignment.MiddleCenter
        self.__bt4.Click += self.__add_num

        # bt5
        self.__bt5.AutoSize = True
        self.__bt5.Font = Font("Xolonium", 27.75, FontStyle.Bold | FontStyle.Italic, GraphicsUnit.Point, 0)
        self.__bt5.ForeColor = Color.White
        self.__bt5.Location = Point(190, 105)
        self.__bt5.Name = "bt5"
        self.__bt5.Padding = Padding(25, 15, 25, 15)
        self.__bt5.Size = Size(99, 71)
        self.__bt5.TabIndex = 8
        self.__bt5.Text = "5"
        self.__bt5.Tag = '5'
        self.__bt5.TextAlign = ContentAlignment.MiddleCenter
        self.__bt5.Click += self.__add_num

        # bt6
        self.__bt6.AutoSize = True
        self.__bt6.Font = Font("Xolonium", 27.75, FontStyle.Bold | FontStyle.Italic, GraphicsUnit.Point, 0)
        self.__bt6.ForeColor = Color.White
        self.__bt6.Location = Point(295, 105)
        self.__bt6.Name = "bt6"
        self.__bt6.Padding = Padding(25, 15, 25, 15)
        self.__bt6.Size = Size(99, 71)
        self.__bt6.TabIndex = 11
        self.__bt6.Text = "6"
        self.__bt6.Tag = '6'
        self.__bt6.TextAlign = ContentAlignment.MiddleCenter
        self.__bt6.Click += self.__add_num

        # bt7
        self.__bt7.AutoSize = True
        self.__bt7.Font = Font("Xolonium", 27.75, FontStyle.Bold | FontStyle.Italic, GraphicsUnit.Point, 0)
        self.__bt7.ForeColor = Color.White
        self.__bt7.Location = Point(76, 176)
        self.__bt7.Name = "bt7"
        self.__bt7.Padding = Padding(25, 15, 25, 15)
        self.__bt7.Size = Size(99, 71)
        self.__bt7.TabIndex = 13
        self.__bt7.Text = "7"
        self.__bt7.Tag = '7'
        self.__bt7.TextAlign = ContentAlignment.MiddleCenter
        self.__bt7.Click += self.__add_num

        #  bt8
        self.__b8.AutoSize = True
        self.__b8.Font = Font("Xolonium", 27.75, FontStyle.Bold | FontStyle.Italic, GraphicsUnit.Point, 0)
        self.__b8.ForeColor = Color.White
        self.__b8.Location = Point(190, 176)
        self.__b8.Name = "b8"
        self.__b8.Padding = Padding(25, 15, 25, 15)
        self.__b8.Size = Size(99, 71)
        #  self.__b8.TabIndex = 9
        self.__b8.Text = "8"
        self.__b8.Tag = '8'
        self.__b8.TextAlign = ContentAlignment.MiddleCenter
        self.__b8.Click += self.__add_num

        # bt9
        self.__bt9.AutoSize = True
        self.__bt9.Font = Font("Xolonium", 27.75, FontStyle.Bold | FontStyle.Italic, GraphicsUnit.Point, 0)
        self.__bt9.ForeColor = Color.White
        self.__bt9.Location = Point(295, 176)
        self.__bt9.Name = "bt9"
        self.__bt9.Padding = Padding(25, 15, 25, 15)
        self.__bt9.Size = Size(99, 71)
        # self.__bt9.TabIndex = 14
        self.__bt9.Text = "9"
        self.__bt9.Tag = '9'
        self.__bt9.TextAlign = ContentAlignment.MiddleCenter
        self.__bt9.Click += self.__add_num
        # bt0
        self.__b0.AutoSize = True
        self.__b0.Font = Font("Xolonium", 27.75, FontStyle.Bold | FontStyle.Italic, GraphicsUnit.Point, 0)
        self.__b0.ForeColor = Color.White
        self.__b0.Location = Point(190, 247)
        self.__b0.Name = "b0"
        self.__b0.Padding = Padding(25, 15, 25, 15)
        self.__b0.Size = Size(99, 71)
        self.__b0.TabIndex = 10
        self.__b0.Text = "0"
        self.__b0.Tag = '0'
        self.__b0.TextAlign = ContentAlignment.MiddleCenter
        self.__b0.Click += self.__add_num

        #label1 (Pin *****)
        self.__label1.AutoSize = False
        self.__label1.Font = Font("Xolonium", 20.2499981, FontStyle.Regular, GraphicsUnit.Point, 0)
        self.__label1.ForeColor = Color.White
        self.__label1.Location = Point(12, 9)
        self.__label1.Name = "label1"
        self.__label1.Size = Size(456, 30)
        self.__label1.TabIndex = 15
        self.__label1.Text = ""
        self.__label1.TextAlign = ContentAlignment.TopCenter

        # delete
        self.__delete.Image = Image.FromFile(getImgDir("backspace.png"))
        self.__delete.Location = Point(95, 250)
        self.__delete.Name = "delete"
        self.__delete.Size = Size(60, 60)
        self.__delete.TabIndex = 20
        self.__delete.TabStop = False
        self.__delete.Click += self.__del_last

        # submit
        self.submit.Image = Image.FromFile(getImgDir("apply.png"))
        self.submit.Location = Point(314, 250)
        self.submit.Name = "submit"
        self.submit.Size = Size(60, 60)
        self.submit.TabIndex = 18
        self.submit.TabStop = False
        self.submit.Click += self.__submit

        # Propriedades do ecrã
        self.AutoScaleDimensions = SizeF(7.0, 15.0)
        self.AutoScaleMode = self.AutoScaleMode.Font
        self.BackColor = Color.FromArgb(19, 19, 19)
        self.ClientSize = Size(480, 320)
        self.StartPosition = FormStartPosition.CenterScreen
        self.Controls.Add(self.__delete)
        self.Controls.Add(self.submit)
        self.Controls.Add(self.__label1)
        self.Controls.Add(self.__bt9)
        self.Controls.Add(self.__bt7)
        self.Controls.Add(self.__bt4)
        self.Controls.Add(self.__bt6)
        self.Controls.Add(self.__b0)
        self.Controls.Add(self.__b8)
        self.Controls.Add(self.__bt5)
        self.Controls.Add(self.__bt3)
        self.Controls.Add(self.__bt2)
        self.Controls.Add(self.__b1)
        self.FormBorderStyle = FormBorderStyle(0)
        self.__Name = "numpad"
        self.__Text = "numpad"

        self.__stop_idle = False
        self.__idle_checker = threading.Thread(target=self.__idle, daemon=True).start()


    def __add_num(self, sender, e):
        # Adicionar
        self.__timeout = 0
        self.__PinEntered += sender.Tag
        self.__update_label()

    def __del_last(self, sender, e):
        # Remover o último, se tiver algum caracter
        self.__timeout = 0
        if self.__PinEntered != "":
            self.__PinEntered = self.__PinEntered[:-1]
            self.__update_label()

    # retornar em *
    # ex .: 1234 --> ****
    # 12345678 --> ********
    def __update_label(self):
        if set(self.__label1.Text) - {'*'}: self.__label1.Text = ''
        self.__label1.Text = '*' * len(self.__PinEntered) if self.__PinEntered != '' else ''
        # print(f'PIN --> {self.__PinEntered}')

    # Para outras classes / funções pedirem o PIN
    def getPin(self): return self.__PinEntered

    def __submit(self, sender ,e):

        if len(self.__label1.Text) >= 4:
            url = "http://localhost:8080/pin_checker.php"
            payload = {
                "pin": self.__PinEntered
            }
            try:
                response = requests.post(url, data=payload)
                print("Response Status Code:", response.status_code)
                print("Response Body:", response.text)

            except requests.exceptions.RequestException as e:
                print(f"Error occurred: {e}")

            if response.text == '-1':
                self.__label1.Text = "Incorreto!"
                self.__PinEntered = ''
            else:
                self.__stop_idle = True
                stat = status.fetch_status()
                print(stat)
                if stat == 1 or stat >= 3: # Desligar de imediato
                    status.disarm(int(response.text), False)
                    threading.Thread(target=deploy_lock, daemon=True).start()
                else:
                    threading.Thread(target=deploy_hs, args=(int(response.text),), daemon=True).start()
                self.Close()
        else:
            self.__label1.Text = "Mín. 4 dígitos!"
            self.__PinEntered = ''


    def __idle(self):
        while True:
            if self.__stop_idle: return
            self.__timeout += 1
            if self.__timeout > 20:
                self.swap_back()
                return # Parar a execução
            else: sleep(1)

    def swap_back(self):
        threading.Thread(target=deploy_lock, daemon=True).start()
        self.Close()

def deploy_hs(id):
    if isinstance(id, tuple): hs = HomeScreen(id[0])
    else: hs = HomeScreen(id)
    Application.Run(hs)

def deploy_numpad():
    hs = numpad()
    Application.Run(hs)

def deploy_lock():
    hs = Locked()
    Application.Run(hs)

def getImgDir(picName):
    if __name__ == "__main__":
        return f"../resized/{picName}"
    else:
        return f"display/resized/{picName}"


if __name__ == "__main__": pass
    #screen = numpad()
    #threading.Thread(target=run, daemon=True).start()
    # threading.Thread(target=screen.update_time_loop, daemon=True).start()

    # app_run_loop()
