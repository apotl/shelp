class Queue():
    def __init__(self):
        self.d = []

    def push(self, e):
        self.d += [e]

    def pop(self):
        to_ret = self.d[0]
        self.d.pop(0)
        return to_ret
