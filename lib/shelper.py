import re

class Shelper():
    REGEX = None

    def check(self, m):
        if not self.REGEX:
            raise NotImplementedError
        if re.match(self.REGEX, m) != None:
            return self.run(m)
        else:
            return []

    def run(self, m):
        raise NotImplementedError
        return []
