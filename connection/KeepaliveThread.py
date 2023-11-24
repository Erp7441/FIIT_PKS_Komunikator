from threading import Thread, Event

from utils.Utils import print_debug


class KeepaliveThread(Thread):
    def __init__(self, target=None, args=None, kwargs=None):
        super().__init__(target=target, args=args, kwargs=kwargs)
        self._target = target
        self._args = args if args is not None else ()
        self._kwargs = kwargs if kwargs is not None else {}
        self._stop_event = Event()  # TODO:: Do I need this? (Needed it in the past from server side)

    def start(self):
        print_debug("Starting keepalive thread...")
        super().start()
        print_debug("Started keepalive thread")

    def run(self):
        # Modified run
        while not self.is_stopped():
            try:
                if self._target is not None:
                    print_debug("Running keepalive thread target...")
                    self._target(*self._args, **self._kwargs)
            except Exception as e:
                # Running target function failed
                print_debug(e, color="orange")

    def stop(self):
        print_debug("Stopping keepalive thread...")
        self._stop_event.set()
        self.join(timeout=0)
        print_debug("Stopped keepalive thread")

    def is_stopped(self):
        return self._stop_event.is_set()
