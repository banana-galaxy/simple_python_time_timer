import time


class Timer:
    def __init__(self):
        self.start_time = 0
        self.total_time = 3600/4

    def start(self, set_time):
        self.start_time = time.time()
        self.total_time = set_time

    def get_time(self):
        time_left = self.total_time - int(time.time() - self.start_time)
        return time_left if time_left > 0 else 0

if __name__ == "__main__":
    timer = Timer()
    timer.start()
    print(timer.get_time())
    time.sleep(2)
    print(timer.get_time())