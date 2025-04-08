"""Этот скрипт я сделал для прогонки тестовых файлов на stepik.org
функцию log()" использую для отладки всех своих программ """


import traceback
import os
import io
import sys

def log(*args, pause=False):
    info = traceback.extract_stack()[-2]
    print("\033[93m" + f"Файл: {info.filename.split('/')[-1]}, Строка: {info.lineno} {args}" + "\033[0m", file=sys.stderr)
    if pause:
        input()
        print('Нажми Enter для продолжения', file=sys.stderr)
    # print(f"Файл: {__file__}, Строка: {traceback.extract_stack()[-2].filename} {args}")

def recviz(func):
    tab = 0
    def wrapper(*args, **kwargs):
        nonlocal tab
        st = ", ".join([str(repr(i)) for i in args] + [f"{k}={repr(v)}" for k, v in kwargs.items()])
        print(f"{'    ' * tab}-> {func.__name__}({st})")
        tab += 1
        res = func(*args, **kwargs)
        tab -= 1
        print(f"{'    ' * tab}<- {repr(res)}")        
        return res
    return wrapper




import os
import io

class DualOutput:
    def __init__(self):
        # Сохраняем оригинальный stdout
        self.original_stdout = sys.stdout
        # Создаем объект StringIO для захвата вывода
        self.captured_output = io.StringIO()

    def write(self, text):
        # Записываем текст в оригинальный stdout (то есть выводим на экран)
        self.original_stdout.write(text)
        # Записываем текст в StringIO для дальнейшего использования
        self.captured_output.write(text)

    def flush(self):
        # Этот метод необходим для корректной работы с буферизированными потоками
        self.original_stdout.flush()

def gotest():
    f = 1
    original_stdout = sys.stdout
    dual_output = DualOutput()
    sys.stdout = dual_output
    while os.path.isfile(f"tests/{f}"):
        with open(f'tests/{f}', 'r', encoding='utf-8') as file:
            test = file.read()
        print(f"=======Тестовый код № {f}===================")
        print(test)
        print("=======Ввод/Вывод если требуется=============")
        dual_output.captured_output.truncate(0)
        exec(test, globals(), locals())
        captured_output = dual_output.captured_output.getvalue()
        with open(f"tests/{f}.clue", 'r', encoding='utf-8') as file:
            clue = file.read()
        if captured_output != clue:
            print("=======Ответ должен быть=====================")
            print(clue)
            sys.stdout = dual_output
            break
        print(f"=======Конец теста №{f}=====================\n\n\n")
        f += 1
    sys.stdout = dual_output
