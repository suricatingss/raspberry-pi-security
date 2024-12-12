import time
try: from core import schema
except: import schema
import mysql.connector as mysql

#
#  ID(auto) Tipo-de-Interação User Data&Hora
#

def intrusion_log(type, premade = True):
    __db = schema.mysql_db()

    query = "INSERT INTO logs (event, event_time) VALUES (%s, %s)"

    if type == "mov": type = "Movimento"
    elif type == "door": type = "Porta"
    elif type == "win": type = "Janela"
    elif type == "enter-door": type = "Entrada pela porta(timer iniciado)"
    elif type == "enter-mov": type = "Entrada (movimento detetado) (timer iniciado)"
    elif type == "time-up": type = "Entrada (O tempo de desarme esgotou)"
    elif type == "wrong": type = "Entrada (PIN incorreto demasiadas vezes)"

    if premade == True: args = (f"Intrusão: ({type})", time.strftime("%y-%m-%d %H:%M:%S", time.localtime(time.time())))
    else: args = (type, time.strftime("%y-%m-%d %H:%M:%S", time.localtime(time.time())))

    __db.Execute(query, args)
    __db.Close()


def user_interaction_log(user, type, remote):
    conn = schema.mysql_db()

    # Adaptar do Python para MySQL
    if remote: remote = 1
    else: remote = 0

    query = "INSERT INTO logs (event,user_id,`remote?`) VALUES (%s,%s,%s)"
    args = (type, user, remote)
   # print(args)

    conn.Execute(query, args)

if __name__ == "__main__":
    pass