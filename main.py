import time, threading, os, clr, sys
from core import live_cams, schema
from signal import pause
from queue import Queue, PriorityQueue
import display.forms.main as display
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import Application, FormWindowState

io_queue = PriorityQueue()

def getState(text_result = False):
    # o estado do sistema
    # 0 - desarme, 1 - armado, 2 - parcial
    # 3 - countdown (armar / para sair)
    # 4 - countdown (para desarmar)
    # 5 - DISPARAR !
    conn = schema.mysql_db()
    state = conn.FetchOneElement("SELECT `value` FROM settings WHERE `label` LIKE 'status'")
    if not text_result: return state
    else:
        # Retornar a legenda correspondente
        labels = ("Desarmado","Armado","Parcial","Contagem (Armar)","Contagem (Desarme)","A TOCAR")
        return labels[int(state)]




# def checkUp(): pass
#
# def swap(args):
#     args[0].Close()
#     threading.Thread(target=app_run, args=(args[1],), daemon=True).start()

def check_internet():
    while True:
        if sys.platform.startswith('win'):
            param = '-n'
            null = 'NUL'
        else:
            null = '/dev/null'
            param = '-c'
        hostname = "google.com"  # example
        response = os.system(f"ping {param} 1 {hostname} > {null} 2>&1")
        #return response
        #print(response)
        if response == 0: pass # acender led
        else: pass # apagar o led
        time.sleep(3)


# def app_run(screen):
#     if isinstance(screen, tuple):
#         Application.Run(screen[0])
#     else:
#         Application.Run(screen)

def reboot_app(screen, args = None):
    screen.Close()
    Application.Run(screen)
    screen.WindowState = FormWindowState.Normal

if __name__ == "__main__":
    threading.Thread(target=live_cams.run, daemon=True).start()
    #flask_thread.start()

    check_net = threading.Thread(target=check_internet, daemon=True).start()
    threading.Thread(target=display.deploy_lock, daemon=True).start()
    pause()


