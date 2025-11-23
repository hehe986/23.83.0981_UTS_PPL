import time, sys, os, datetime, threading
from threading import Thread

# Muhammad Ardita Hilmi (23.83.0981)

class AnimationController:
    def __init__(self):
        self.paused = False
        self.pause_lock = threading.Lock()
        
    def toggle_pause(self):
        with self.pause_lock:
            self.paused = not self.paused
        status = "PAUSED" if self.paused else "RESUMED"
        print(f"\nAnimation {status}! Press SPACE to {'resume' if self.paused else 'pause'}")

def get_terminal_size():
    try:
        columns = os.get_terminal_size().columns
        return max(10, columns - 10)
    except:
        return 20

def get_smart_pattern():
    patterns = [
        '********',
        '########', 
        '========',
        '++++++++',
        '--------',
        '////////',
        '\\\\\\\\'
    ]
    time_index = int(time.time()) // 5 % len(patterns)
    return patterns[time_index]

def input_handler(controller):
    while True:
        try:
            if sys.platform == 'win32':
                import msvcrt
                if msvcrt.kbhit():
                    key = msvcrt.getch().decode('utf-8', errors='ignore')
                    if key == ' ':
                        controller.toggle_pause()
                    elif key == 'q':
                        print("\nExiting...")
                        sys.exit()
            else:
                import select
                if select.select([sys.stdin], [], [], 0.1)[0]:
                    key = sys.stdin.read(1)
                    if key == ' ':
                        controller.toggle_pause()
                    elif key == 'q':
                        print("\nExiting...")
                        sys.exit()
        except:
            pass
        time.sleep(0.1)

def main():
    # ⚠️ PINDAHKAN VARIABEL KE DALAM MAIN FUNCTION
    indent = 0
    indentIncreasing = True
    
    controller = AnimationController()
    
    # Start input thread
    input_thread = Thread(target=input_handler, args=(controller,), daemon=True)
    input_thread.start()
    
    print("ZigZag Animation Started!")
    print("Controls: SPACE = Pause/Resume, Q = Quit")
    print("Terminal responsive size: ON")
    print("Smart patterns: ON")
    
    try:
        while True:
            with controller.pause_lock:
                if controller.paused:
                    time.sleep(0.1)
                    continue
            
            # Auto-size responsive
            max_indent = get_terminal_size()
            
            # Smart pattern
            pattern = get_smart_pattern()
            
            print(' ' * indent + pattern)
            time.sleep(0.1)

            if indentIncreasing:
                indent += 1
                if indent >= max_indent:
                    indentIncreasing = False
            else:
                indent -= 1
                if indent <= 0:
                    indentIncreasing = True
                    
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit()

if __name__ == "__main__":
    main()