from threading import Thread
def async_call(fn):
    def wrapper(*args, **kwargs):
        th = Thread(target=fn, args=args, kwargs=kwargs)
        th.start()
    return wrapper