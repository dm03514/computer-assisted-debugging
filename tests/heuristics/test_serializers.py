import unittest

from cad.heuristics.deploy import Deploy
from cad.heuristics.evaulators import SingleValueThresholdEvaluator
from cad.heuristics.serializers import Markdown
from cad.heuristics.testing import StubQuery


class MarkdownTableTestCase(unittest.TestCase):

    def test_table_single_row(self):
        deploy = Deploy(
            last_deploy=SingleValueThresholdEvaluator(
                'LastDeploy < X hours',
                StubQuery(result=False),
            )
        )

        self.assertEqual(
            '''| Node Name | Evaluator | Query Source | Yes Threshold |
| ------- | --------- | -------- | ----------- |
|LastDeploy < X hours|SingleValueThresholdEvaluator|StubQuery|LastDeploy < X hours|''',
            Markdown(deploy).state_table()
        )

