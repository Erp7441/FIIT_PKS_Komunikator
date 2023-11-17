from threading import Thread, Event


class KeepaliveThread(Thread):
    def __init__(self, target):
        super().__init__(target=target)
        self._stop_event = Event()

    def start(self):
        super().start()

    def run(self):
        while not self._stop_event.is_set():
            super().run()

    def stop(self):
        self._stop_event.set()

