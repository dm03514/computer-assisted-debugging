from abc import ABC, abstractmethod


class TransitionEvaluator(ABC):
    def __init__(self, name, query, comparator=lambda x: x):
        self.query = query
        self.comparator = comparator
        self.name = name

    def __repr__(self):
        return self.name

    @abstractmethod
    def result(self):
        """
        :return: bool
        """
        pass


class SingleValueThresholdEvaluator(TransitionEvaluator):

    def result(self):
        qr = self.query.result()
        assert len(qr) == 1
        return self.comparator(qr[0])


class ManyValuesThresholdEvaluator(TransitionEvaluator):

    def result(self):
        req = self.query.result()
        vs = filter(self.comparator, req)
        return len(vs) > 1


class OneOfManyValuesThresholdEvaluator(TransitionEvaluator):

    def result(self):
        req = self.query.result()
        assert len(req) > 1
        vs = filter(self.comparator, req)
        return len(vs) == 1
