import threading

lock = threading.Lock()


class Singleton(type):
    _instances = {}

    # Changed to using thread safe Singleton
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super(
                        Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
