import time
import threading
from pynput import keyboard
from pynput.keyboard import Key, Listener

class TextTyper:
    def __init__(self, filename):
        self.filename = filename
        self.is_typing = False
        self.lines = []
        self.current_line = 0
        self.keyboard = keyboard.Controller()
        
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.lines = [line.strip() for line in f.readlines()]
            print(f"Загружено {len(self.lines)} строк из файла {filename}")
        except Exception as e:
            print(f"нету брат файла: {e}")

    def toggle_typing(self):
        self.is_typing = not self.is_typing
        if self.is_typing:
            print("начинаем брат макан...")
            threading.Thread(target=self.type_lines, daemon=True).start()
        else:
            print("стоп")

    def type_lines(self):
        while self.is_typing and self.current_line < len(self.lines):
            line = self.lines[self.current_line]
            
            self.keyboard.type(line)
            
            self.keyboard.press(Key.enter)
            self.keyboard.release(Key.enter)
            
            self.current_line += 1
            if self.current_line >= len(self.lines):
                self.current_line = 0  
                
            time.sleep(0.1)  

def main():
    typer = TextTyper("tox.txt")
    
    def on_press(key):
        if key == Key.f3:
            typer.toggle_typing()
    
    print("F3")
    print("выход Ctrl+C")
    
    with Listener(on_press=on_press) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            print("\nстоп брат")

if __name__ == "__main__":
    main()
