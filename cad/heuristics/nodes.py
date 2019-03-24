

class Alert:
    def __repr__(self):
        return 'alert'


class Start:
    def __repr__(self):
        return 'start'


class End:
    def __repr__(self):
        return 'end'


class Yes:
    def evaluate(self, against):
        return against


class No:
    def evaluate(self, against):
        return not against
