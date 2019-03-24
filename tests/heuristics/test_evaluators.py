import unittest

from cad.heuristics.evaulators import SingleValueThresholdEvaluator
from cad.heuristics.testing import StubQuery


class SingleValueThresholdEvaluatorTestCase(unittest.TestCase):

    def test_result_assertion_error_invalid_query_result(self):
        with self.assertRaises(AssertionError):
            SingleValueThresholdEvaluator(
                name='test',
                query=StubQuery(
                    result=[1, 2]
                )
            ).result()

    def test_result_compares_successfully(self):
        self.assertTrue(
            SingleValueThresholdEvaluator(
                name='test',
                query=StubQuery(
                    result=[2]
                ),
                comparator=lambda x: x > 1
            ).result()
        )


class ManyValuesThresholdEvaluatorTestCase(unittest.TestCase):
    def test_single_query_value_results_false(self):
        self.fail()

    def test_multi_query_values_filter_multi_returns_true(self):
        self.fail()

    def test_multi_query_values_filter_false_returns_false(self):
        self.fail()


class OneOfManyValuesThresholdEvaluatorTestCase(unittest.TestCase):
    def test_assertion_error_single_result(self):
        self.fail()

    def test_result_false_when_more_than_one_filtered(self):
        self.fail()

    def test_result_true_when_one_result_filtered(self):
        self.fail()
