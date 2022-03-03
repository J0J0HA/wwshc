import threading


class _GS:
    val = None
    def set(self, val): self.val = val
    def get(self): return self.val


class Events:
    def __init__(self):
        self.handlers = {}

    def on(self, event):
        func_gs = _GS()

        def wrapper(func):
            func_gs.set(func)
            return func

        self.on_event(event, func_gs.get())
        return wrapper

    def on_event(self, event, func):
        if event in self.handlers.keys():
            self.handlers[event].append(func)
        else:
            self.handlers.update({event: [func]})

    def cause(self, event, *args, **kwargs):
        threading.Thread(target=self._cause, args=(event,)+args, kwargs=kwargs).start()

    def _cause(self, event, *args, **kwargs):
        if event in self.handlers.keys():
            for func in self.handlers[event]:
                threading.Thread(target=func, args=args, kwargs=kwargs).start()
        if self.All in self.handlers.keys():
            for func in self.handlers[self.All]:
                threading.Thread(target=func, args=args, kwargs=kwargs).start()

    class All: pass
