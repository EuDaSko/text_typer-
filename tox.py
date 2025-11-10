import time
import threading
import random
from pynput import keyboard
from pynput.keyboard import Key, Listener

class TextTyper:
    def __init__(self, filename, mode="normal", random_mode=False):
        self.filename = filename
        self.is_typing = False
        self.lines = []
        self.current_line = 0
        self.keyboard = keyboard.Controller()
        self.mode = mode
        self.random_mode = random_mode
        self.delay = 0.1 if mode == "normal" else 0.5
        self.last_random_line = None  
        
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.lines = [line.strip() for line in f.readlines()]
            print(f"Загружено {len(self.lines)} строк из файла {filename}")
            print(f"Режим: {mode}, Рандом: {random_mode}")
        except Exception as e:
            print(f"Нету брат файла, название проверь и формат: {e}")

    def toggle_typing(self):
        self.is_typing = not self.is_typing
        if self.is_typing:
            print("Начинаем брат макан...")
            threading.Thread(target=self.type_lines, daemon=True).start()
        else:
            print("Стоп")

    def get_next_line(self):
        if self.random_mode:

            if len(self.lines) > 1:
                available_lines = [line for line in self.lines if line != self.last_random_line]
                line = random.choice(available_lines)
            else:
                line = self.lines[0] if self.lines else ""
            self.last_random_line = line
            return line
        else:
            line = self.lines[self.current_line]
            self.current_line = (self.current_line + 1) % len(self.lines)
            return line

    def type_lines(self):
        while self.is_typing and self.lines:
            line = self.get_next_line()
            
            for char in line:
                self.keyboard.type(char)
                time.sleep(0.01)  
            
            time.sleep(0.05)
            self.keyboard.press(Key.enter)
            time.sleep(0.05)
            self.keyboard.release(Key.enter)
            time.sleep(self.delay)

def main():
    print("Заходим на сервак делевопера братья!! - https://discord.gg/gbyfwpyCmQ")
    print("Ес чо используем библиотеку pynput для эмуляции ввода, это не просто использование буфера обмена для вставки")
    print("Выбери режим брат, медленный чтобы кд не мешало в дс и можно было афк сидеть в войсе:")
    print("1 - дефолт тайпинг (быстро для ТГ и тд)")
    print("2 - медленный тайпинг (для дискорда)")
    print("потом все равно можно будет менять конфиг ес чо")

    mode_choice = input("Чо надо брат? (1 или 2): ").strip()
    mode = "normal" if mode_choice == "1" else "slow"
    
    random_choice = input("В случайном порядке будем писать брат? (да(y)/нет(n)): ").strip().lower()
    random_mode = random_choice in ['y', 'да', 'yes']
    
    typer = TextTyper("tox.txt", mode=mode, random_mode=random_mode) 
    
    def on_press(key):
        if key == Key.f3:
            typer.toggle_typing()
        elif key == Key.f4:
            typer.mode = "slow" if typer.mode == "normal" else "normal"
            typer.delay = 0.5 if typer.mode == "slow" else 0.1
            print(f"Поменяли режим брат: {typer.mode}")
        elif key == Key.f5:
            typer.random_mode = not typer.random_mode
            print(f"Рандом: {'вкл' if typer.random_mode else 'выкл'}")
    
    print("\nГорячие клавиши братик:")
    print("F3 - старт/стоп")
    print("F4 - переключение скорости тайпинга")
    print("F5 - вкл/выкл рандом")
    print("Выход из коммандной строки ес чо: ctrl+c")
    
    with Listener(on_press=on_press) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            print("\nСтоп брат")

if __name__ == "__main__":
    main()
