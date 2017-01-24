import re

class Shelper():
    REGEX = None

    def check(self, m):
        if not self.REGEX:
            raise NotImplementedError
        if re.match(self.REGEX, m) != None:
            return self.run(m)

    def run(self, m):
        raise NotImplementedError
        return []
