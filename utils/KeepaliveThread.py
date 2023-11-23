from threading import Thread, Event

from utils.Utils import print_debug


class KeepaliveThread(Thread):
    def __init__(self, target=None, args=None, kwargs=None):
        super().__init__(target=target, args=args, kwargs=kwargs)
        self._target = target
        self._args = args if args is not None else ()
        self._kwargs = kwargs if kwargs is not None else {}

    def start(self):
        print_debug("Starting keepalive thread...")
        super().start()
        print_debug("Started keepalive thread")

    def run(self):
        # Modified run to use the stop event
        while True:
            try:
                if self._target is not None:
                    print_debug("Running keepalive thread target...")
                    self._target(*self._args, **self._kwargs)
            except Exception as e:
                print_debug(e, color="orange")

    def stop(self):
        print_debug("Stopping keepalive thread...")

        if hasattr(self, '_tstate_lock'):
            try:
                self._tstate_lock.release()
                if hasattr(self, '_stop'):
                    self._stop()
                self.join()
            except Exception as e:
                print_debug("Could not stop keepalive thread", color="orange")
                print_debug(e, color="orange")
                return


        print_debug("Stopped keepalive thread")

