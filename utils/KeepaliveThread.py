from threading import Thread, Event


class KeepaliveThread(Thread):
    def __init__(self, target=None, args=(), kwargs=None):
        super().__init__(target=target, args=args, kwargs=kwargs)
        self._target = target
        self._args = args
        self._kwargs = kwargs
        self._stop_event = Event()

    def start(self):
        super().start()

    def run(self):
        # Modified run to use the stop event
        while not self._stop_event.is_set():
            try:
                if self._target is not None:
                    self._target(*self._args, **self._kwargs)
            except Exception:
                pass

    def stop(self):
        self._stop_event.set()

