import unittest

from cad.datasources.jenkins.api import Build


class APIClientTestCase(unittest.TestCase):

    def test_client_invalid_status_code(self):
        self.fail()

    def test_client_returns_builds(self):
        self.fail()


class BuildTestCase(unittest.TestCase):

    def test_is_success_success(self):
        self.assertTrue(
            Build(
                data={
                    'id': '34',
                    'number': 34,
                    'result': 'SUCCESS',
                    'timestamp': 1536267817556
                }
            )
        )

    def test_build_params_no_actions(self):
        self.fail()

    def test_build_params_no_parameters(self):
        self.fail()

    def test_build_params_has_params(self):
        self.assertEqual(
            {
                'AMI': '',
                'ENV': 'staging',
                'REGION': 'us-west-2',
                'SERVICE': 'my-service'
            },
            Build(
                data={
                    '_class': 'org.jenkinsci.plugins.workflow.job.WorkflowRun',
                    'actions': [
                        {
                            '_class': 'hudson.model.ParametersAction',
                            'parameters': [
                                {
                                    '_class': 'hudson.model.StringParameterValue',
                                    'name': 'ENV',
                                    'value': 'staging'
                                },
                                {
                                    '_class': 'hudson.model.StringParameterValue',
                                    'name': 'REGION',
                                    'value': 'us-west-2'
                                },
                                {
                                    '_class': 'hudson.model.StringParameterValue',
                                    'name': 'SERVICE',
                                    'value': 'my-service'
                                },
                                {
                                    '_class': 'hudson.model.StringParameterValue',
                                    'name': 'AMI',
                                    'value': ''
                                }
                            ]
                        }
                    ]
                }
            ).params()
        )
