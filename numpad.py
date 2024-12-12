import requests, gpiozero, threading, main, time
from typing import Union
from signal import pause
from core import status, trigger

leds = {
    'red': gpiozero.LED(14),
    'green': gpiozero.LED(15),
    'yellow': gpiozero.LED(16)
}

entered_pin:str = ''
user_id:Union[int,None] = None
timeout:int = 7
buzzPin:int = trigger.soundBuzz

def led_blink(led:gpiozero.LED, timeout:int):
    main.io_queue.put(1, block=True)
    led.on()
    time.sleep(timeout)
    led.off()
    main.io_queue.task_done()

def session_timeout():
    time.sleep(timeout)
    logout()

def logout(auto:bool = True):
    global entered_pin, user_id
    user_id = None
    main.io_queue.put(1, block=True)
    leds['green'].off()
    entered_pin = ''
    if not auto:
        buzz = gpiozero.Buzzer(buzzPin).on()
        time.sleep(0.1)
        buzz.off()
        buzz.close()

def pressed():
    row:Union[int,None] = None
    col:Union[int,None] = None
    global rows, columns, entered_pin
    # Analizar qual tecla foi premida
    for c in range(columns):
        for r in range(rows):
            if rows[r].is_pressed and columns[c].is_pressed:
                row = r
                col = c
                break

        if row is not None \
        or col is not None: break # quebrar se o outro loop quebrar também

    key = keys_map[col][row]
    if user_id is not None: # Executar ação
        if key == 'a': # Arme total
            status.delayArming(user_id, False)
        elif key == 'b': # Parcial
            main.io_queue.put(1, block=True)
            leds['yellow'].on()
            time.sleep(1.5)
            leds['yellow'].off()
            main.io_queue.task_done()


    if key == 'a': # limpar
        entered_pin = ""
    elif key == 'b': # Submitir
        pin_dict = {"pin":entered_pin}
        check = requests.post(
            url="http://127.0.0.1/pin_checker.php",
            data= pin_dict
        )
        main.io_queue.put(1, block=True)
        response = check.text
        if response == "-1":  # Pin Incorreto
            led_blink(leds['red'], 1)
        else: # Correto
            leds['green'].on()
            if status.fetch_status() != 0: # Desarme imediato
                status.disarm(user_id, False)
                time.sleep(1)
                logout(False)
            else: # Iniciar sessão
                threading.Thread(target=session_timeout,daemon=True).start()
    else:
        entered_pin += key




main.io_queue.put(1, False)
rows = (gpiozero.Button(i) for i in (1,2,3))
columns = (gpiozero.Button(i) for i in (4,5,6))
keys_map = (('1','2','3'),
            ('4','5','6'),
            ('7','8','9'),
            ('a','0','b'))

for btn in (rows, columns): btn.when_pressed = pressed

if __name__ == "__main__": pause()



