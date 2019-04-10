import unittest
from datetime import datetime
from unittest.mock import MagicMock

from cad.datasources.jenkins.api import Build
from cad.datasources.jenkins.queries import JenkinsLastSuccessfulParameterizedBuildQuery


class JenkinsLastSuccessfulParameterizedBuildQueryTestCase(unittest.TestCase):
    def test_result_builds_no_success(self):
        self.fail()

    def test_result_builds_no_match(self):
        self.fail()

    def test_result_builds_match(self):
        client = MagicMock()
        client.builds.return_value = [
            Build(
                data={
                    'id': '34',
                    'number': 34,
                    'result': 'SUCCESS',
                    'timestamp': 1536267817556,
                    '_class': 'org.jenkinsci.plugins.workflow.job.WorkflowRun',
                    'actions': [
                        {
                            '_class': 'hudson.model.ParametersAction',
                            'parameters': [
                                {
                                    '_class': 'hudson.model.StringParameterValue',
                                    'name': 'SERVICE',
                                    'value': 'test-service'
                                },
                            ]
                        }
                    ]

                }
            )
        ]
        self.assertEqual(
            [datetime(2018, 9, 6, 17, 3, 37, 556000)],
            JenkinsLastSuccessfulParameterizedBuildQuery(
                client=client,
                match={
                    'SERVICE': 'test-service'
                }
            ).result()
        )
