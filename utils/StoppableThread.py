from threading import Thread, Event

from utils.Utils import print_debug


class StoppableThread(Thread):
    def __init__(self, target=None, args=None, kwargs=None):
        super().__init__(target=target, args=args, kwargs=kwargs)
        self._target = target
        self._args = args if args is not None else ()
        self._kwargs = kwargs if kwargs is not None else {}
        self._stop_event = Event()

    def start(self):
        print_debug("Starting stoppable thread...")
        super().start()
        print_debug("Started stoppable thread")

    def run(self):
        # Modified run
        while not self.is_stopped():
            try:
                if self._target is not None:
                    print_debug("Running stoppable thread target...")
                    self._target(*self._args, **self._kwargs)
            except Exception as e:
                # Running target function failed
                print_debug(e, color="orange")

    def stop(self):
        print_debug("Stopping stoppable thread...")
        self._stop_event.set()
        print_debug("Stopped stoppable thread")

    def is_stopped(self):
        return self._stop_event.is_set()
