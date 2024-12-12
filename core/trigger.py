import subprocess, time
import threading, os, sys
# import gpiozero

from core import status, schema, logs

__db = schema.mysql_db()

movementPins = ()
doorPins = ()
windowPins = ()

entryDoorPins = ()
entryMovementPins = ()

soundBuzz = 18
#lockedPin = gpiozero.LED(2)
#partialPin = gpiozero.LED(3)
#triggerPin = gpiozero.LED(4)


def readPin(pin):
    pass
# Esta função foi criada porque não consigo usar o GPIO aqui no Windows

def checkPins(PinGroup):
    pinsTriggered = []
    #if not isintance(PinGroup, tuple): return # se não for uma tupla, algo está errado

    for Pin in (PinGroup):
        if readPin(Pin): pinsTriggered.append(Pin)  # adicionar o Pin à lista

    if len(pinsTriggered) == 0: return None # não foi acionado nada
    else: return pinsTriggered

def check_pins_loop():
    while True:
        now_stat = status.fetch_status()
        if now_stat == 1:
            pins = checkPins(movementPins,doorPins,windowPins,entryDoorPins,entryMovementPins)
        elif now_stat == 2:
            pins = checkPins(doorPins, windowPins, entryDoorPins) # excluir movimento
        else: pass
        if now_stat == 1 or now_stat == 2:
            if pins in movementPins: status.panic("mov")
            elif pins in windowPins: status.panic("win")
            elif pins in doorPins: status.panic("door")
            elif pins in entryDoorPins:
                status.delay_enter("enter-door", False)

            elif pins in entryMovementPins:
                status.delay_enter("enter-mov", False)

        time.sleep(2)

def alarm_trigger(type):

    logs.intrusion_log(type)
    while True:
        status.updateStatus()
        __status = status.getStatus()
        if __status == 5: pass
            # Tocar alarme
        else:
            # Parar o alarme
            return


# Esta função é suposto ser em background
def trigger_timer(type, args = None):
    __db = schema.mysql_db()
    type2 = type[0] if isinstance(type, tuple) else type

    if type2 == 'arm':
        seconds = int(__db.FetchOneElement("SELECT value FROM settings WHERE name = 'leaveCooldown'"))
    elif type2 == 'disarm':
        seconds = int(__db.FetchOneElement("SELECT value FROM settings WHERE name = 'entryCooldown'"))
    while True:
        status.updateStatus()
        __status = status.getStatus()
        # Verificar se o estado foi alterado
        if (__status == 3 or __status == 4) and seconds >= 0:
            if seconds > 10:
                # produzir efeito 'beep'
                time.sleep(0.5)
                # desligar 'beep'
                time.sleep(0.5)
                seconds -= 1
            else:
                # ligar 'beep'
                time.sleep(0.25)
                # desligar 'beep'
                time.sleep(0.25)
                # ligar 'beep' outra vez
                time.sleep(0.25)
                # desligar 'beep' vez
                time.sleep(0.25)
                seconds -= 1
            print(seconds)
        elif __status == 3 and seconds < 0:
            __db.Execute("UPDATE settings SET value = %s WHERE name = 'status'", (1,))
            print("Sistema armado!")
            return
        elif __status == 4 and seconds < 0:
            __db.Execute("UPDATE settings SET value = %s WHERE name = 'status'", (5,))
            threading.Thread(target=alarm_trigger, args=("time-up",), daemon=True).start()
            print("PANIC!")
            return
        else: return # O estado foi alterado !


# tocar alarme
# tirar fotos (e/ou gravar videos)
# fazer um registo

