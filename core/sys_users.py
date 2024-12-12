import subprocess, sys, json
from typing import Union

def new_user(name:str , pwd:str, admin: bool):
    # 1 - criar o utilizador
    subprocess.Popen(["useradd", name])

    # 2 - criar password ( utilizador e SMB)
    for command in (["passwd", name],["smbpasswd", "-a", name]):
        passwd = subprocess.Popen(command,
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        # tal como num comando, coloca-se "passwd com o nome"
        # depois, a password e enter ( e outra vez para confirmar )
        passwd.stdin.write(f'{pwd}\n'.encode())
        passwd.stdin.write(f'{pwd}\n'.encode())
        passwd.stdin.flush()

    # 3 - o grupo
    group = "secure-admins" if admin else "secure-members"
    subprocess.Popen(["usermod","-aG",group,name], check=True)

def edit_user(name:str, pwd:Union[str, None] = None, admin:Union[bool,None] = None):

    # Mudar administração
    if admin is not None:
        group = "secure-admins" if admin == True else "secure-members"
        subprocess.Popen(["usermod", "-G", name, group])

    if pwd is not None:
        for command in (["passwd", name], ["smbpasswd", name]):
            passwd = subprocess.Popen(command,
                                      stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
            # tal como num comando, coloca-se "passwd com o nome"
            # depois, a password e enter ( e outra vez para confirmar )
            passwd.stdin.write(f'{pwd}\n'.encode())
            passwd.stdin.write(f'{pwd}\n'.encode())
            passwd.stdin.flush()

def del_user(name:str):
    subprocess.Popen(["deluser", name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if __name__ == "__main__":
    action = sys.argv[1] # a ação
    # Converter o dicionário
    args_str = sys.argv[2]
    if args_str[0] == '\"' and args_str[len(args_str) - 1] == '\"':
        args_str = args_str[1:-1]

    args:dict = json.loads(args_str)
    args_list = [None, None, None]
    keys = args.keys()
    valid_names = ("name","pwd","admin")
    places = {"name":0, "pwd":1, "admin":2}
    for i in range(0,3):
        if keys[i] in valid_names:
            args_list[places[keys[i]]] = args[keys[i]]

    if action == "create": new_user(*args_list)
    elif action == "edit": edit_user(*args_list)
    elif action == "del": del_user(args_list[0]) # Só precisamos do nome



