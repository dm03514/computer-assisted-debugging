import unittest

from cad.engine.executor import Executor
from cad.heuristics.deploy import Deploy
from cad.heuristics.testing import StubQuery


class ExecutorTestCase(unittest.TestCase):
    def test_run(self):
        ex = Executor(
            Deploy(
                last_deploy=StubQuery(
                    result=False
                )
            )
        )
        self.assertTrue(ex.run())
