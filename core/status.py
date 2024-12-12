#!D:\tomas\Nextcloud\Projetos\Python_Pi_final\raspberry_proj\.venv\Scripts\python.exe

import subprocess, sys, threading, os
from time import time, sleep
#import main

if __name__ == "__main__":
    path = os.path.join(os.getcwd(),'..')
    sys.path.append(os.path.normpath(path))

from core import logs, trigger, schema
# except ModuleNotFoundError: import schema, logs, trigger


__db = schema.mysql_db()

__status = int(__db.FetchOneElement("SELECT value FROM settings WHERE name = 'status'"))
__remote = False


def updateStatus():
    global __db
    __status = int(__db.FetchOneElement("SELECT value FROM settings WHERE name = 'status'"))

def change_status(new_stat):
    __db = schema.mysql_db()
    __db.Execute("UPDATE settings SET value = %s WHERE name = %s", (new_stat, 'status'))

def getStatus():
    global __status
    return __status

def fetch_status():
    sch = schema.mysql_db()
    return int(sch.FetchOneElement("SELECT value FROM settings WHERE name LIKE 'status'"))

def arm(id, remote):
    change_status(1)
    logs.user_interaction_log(id, "Armar", remote)

def delayArming(id, remote):
    print("Arming...")
    change_status(3)
    logs.user_interaction_log(id, "Armar (Delay)", remote)
    threading.Thread(target=trigger.trigger_timer, args=("arm",), daemon=True).start()
def disarm(id, remote):
    change_status(0)
    logs.user_interaction_log(id, "Desarme", remote)
   # __db.Execute("UPDATE settings SET value = '0' WHERE name = 'status'")
  #  main.reboot_app(slb)
def part(id, remote):
    change_status(2)
    logs.user_interaction_log(id, "Armar (parcial)", remote)
    #__db.Execute("UPDATE settings SET value = %s WHERE name = %s", (2,'status'))
def delay_enter(type, remote = False):
    change_status(4)
    logs.intrusion_log(type, False)
    #__db.Execute("UPDATE settings SET value = 4 WHERE name = 'status'")
    trigger.trigger_timer('disarm')

def panic(type = None, id = None):
    global __db
    __db.Execute("UPDATE settings SET value = 5 WHERE name = 'status'")
    if id is None and type is not None: logs.intrusion_log(type)
    else: logs.user_interaction_log(id, "Disparar! (acionado pelo utilizador)", True)


if __name__ == "__main__": # Acionado pelo PHP
    __remote = True
    id = int(sys.argv[1])
    action = int(sys.argv[2])
    if action == 1: arm(id, True)
    elif action == 0: disarm(id, True)
    elif action == 2: part(id, True)
    elif action == 4: delay_enter("Teste", True)
    elif action == 5: panic(None, id)