import time
import pyautogui

def tab_manager_function(context):
    while True:
        # Mudar para a próxima aba
        pyautogui.hotkey('ctrl', 'tab')
        time.sleep(90)  # Esperar 90 segundos antes de mudar para a próxima aba
