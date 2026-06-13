import time

class HoldFilter:
    def __init__(self, hold_time=2.0):
        self.hold_time = hold_time
        self.current_char = None
        self.start_time = None
        self.confirmed = None

    def update(self, char):
        if char is None:
            self.current_char = None
            self.start_time = None
            return None

        if char != self.current_char:
            self.current_char = char
            self.start_time = time.time()
            self.confirmed = None
            return None

        elapsed = time.time() - self.start_time

        if elapsed >= self.hold_time and self.confirmed != char:
            self.confirmed = char
            # 확정 후 리셋해서 같은 글자 다시 인식 가능
            self.current_char = None
            self.start_time = None
            return char

        return None

    def get_progress(self):
        if self.start_time is None:
            return 0.0
        elapsed = time.time() - self.start_time
        return min(elapsed / self.hold_time, 2.0)

    def reset(self):
        self.current_char = None
        self.start_time = None
        self.confirmed = None