

class StubQuery:
    def __init__(self, result):
        self._result = result

    def result(self):
        return self._result
