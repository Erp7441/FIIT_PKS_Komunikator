from threading import Thread, Event

from utils.Utils import print_debug


class KeepaliveThread(Thread):
    def __init__(self, target=None, args=None, kwargs=None):
        super().__init__(target=target, args=args, kwargs=kwargs)
        self._target = target
        self._args = args if args is not None else None
        self._kwargs = kwargs if kwargs is not None else None
        self._stop_event = Event()

    def start(self):
        super().start()

    def run(self):
        # Modified run to use the stop event
        while not self._stop_event.is_set():
            try:
                if self._target is not None:
                    self._target(*self._args, **self._kwargs)
            except Exception as e:
                print_debug(e, color="orange")

    def stop(self):
        self._stop_event.set()

