import subprocess
import os
import asyncio
import sys
import requests
import json
import threading
cmd_limit = 15
version = "1.0"
block_vbs = True
conf_file = "SimpleAntivirus.conf"
worker_task = None
loop = None
def load_config():
    with open(conf_file,"r",encoding="utf-8") as f:
        global cmd_limit,block_vbs
        lines = f.readlines()
        cmd_limit = int(lines[0].strip())
        block_vbs = StringToBool(lines[1].strip())
def boolToString(trueorfalse):
    if trueorfalse == True:
        return "true"
    else:
        return "false"
def StringToBool(trueorfalse):
    if trueorfalse == "true":
        return True
    else:
        return False
def write_config():
    global cmd_limit,block_vbs
    with open(conf_file,"w") as f:
        f.write(str(cmd_limit) +  "\n" + boolToString(block_vbs))


if os.path.exists(conf_file):
    load_config()
else:
    with open(conf_file,"w") as f:
        f.write("15\ntrue")
async def worker():
    global event,cmd_limit,block_vbs
    while True:
        
        if subprocess.run(["tasklist"],capture_output=True,text=True).stdout.count("cmd.exe") >= cmd_limit:
            subprocess.run(["taskkill","/f","/im","cmd.exe"],capture_output=True,text=True)
            subprocess.run(["taskkill","/f","/im","cmd.exe"],capture_output=True,text=True)
            subprocess.run(["taskkill","/f","/im","cmd.exe"],capture_output=True,text=True)
            subprocess.run(["taskkill","/f","/im","cmd.exe"],capture_output=True,text=True)
            subprocess.run(["taskkill","/f","/im","cmd.exe"],capture_output=True,text=True)
            subprocess.run(["taskkill","/f","/im","cmd.exe"],capture_output=True,text=True)
            subprocess.run(["taskkill","/f","/im","cmd.exe"],capture_output=True,text=True)
            subprocess.run(["taskkill","/f","/im","cmd.exe"],capture_output=True,text=True)
            
            print("Обнаружена угроза, cmd завершен")
            if block_vbs == True:
                subprocess.run(["taskkill","/f","/im","wscript.exe"],capture_output=True,text=True)
                subprocess.run(["taskkill","/f","/im","cscript.exe"],capture_output=True,text=True)
                print("вместе с cmd завершили .vbs")
        await asyncio.sleep(0.2)
def start_worker():
    global worker_task,loop
    os.system("cls")
    loop = asyncio.new_event_loop()
    def run_loop():
        asyncio.set_event_loop(loop)
        loop.run_forever()
    threading.Thread(target=run_loop, daemon=True).start()
    worker_task = asyncio.run_coroutine_threadsafe(worker(),loop)
    print("""
Защита активна
напишите 1, чтобы остановить защиту


""")
    while True:
        if input() == "1":
            worker_task.cancel()
            worker_task = None
            loop.call_soon_threadsafe(loop.stop)
            loop = None
            main()
            break
def config():
    global cmd_limit,block_vbs
    os.system("cls")
    print("""
Настройки:
текущий конфиг:
лимит cmd: """ + str(cmd_limit) + """
останавливать .vbs вместе с cmd: """ + boolToString(block_vbs))
    cmd_limit = int(input("Введите новый лимит cmd: "))
    block_vbs = StringToBool(input("Блокировать .vbs(true или false)?: "))
    write_config()
    main()
def main():
    #global version
    os.system("cls")
    """try:
        if json.loads(requests.get("https://raw.githubusercontent.com/unknowncircle13/SimpleAntivirus/refs/heads/main/latest_version.json").text)["latest_ver"] == "1.0":
            print("Установлена последняя версия")
        else:
            print("Доступна новая версия, скачать по ссылке https://github.com/unknowncircle13/SimpleAntivirus")
    except e:
        print("Ошибка проверки версии")
        print(e)
        """
    print("""
SimpleAntivirus 1.0
Автор: unknowncircle13
Конфиг:
лимит cmd: """ + str(cmd_limit) + """
останавливать .vbs вместе с cmd: """ + boolToString(block_vbs))
    print("""
Функции:
1 - активировать защиту
2 - настройки
3 - выйти""")
    func = input("Выберите действие: ")
    if func == "1":
        start_worker()
    elif func == "2":
        config()
    elif func == "3":
        sys.exit()
main()
