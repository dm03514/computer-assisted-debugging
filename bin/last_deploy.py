import os
from datetime import datetime, timedelta

from cad.datasources.jenkins import api
from cad.datasources.jenkins.queries import JenkinsLastSuccessfulParameterizedBuildQuery
from cad.engine.executor import Executor
from cad.heuristics.deploy import Deploy
from cad.heuristics.evaulators import SingleValueThresholdEvaluator

deploy_playbook = Deploy(
    last_deploy=SingleValueThresholdEvaluator(
        name='LastDeploy < 24 hours!',
        query=JenkinsLastSuccessfulParameterizedBuildQuery(
            client=api.Client(
                username=os.environ['JENKINS_USERNAME'],
                password=os.environ['JENKINS_PASSWORD'],
                job_build_url=os.environ['JENKINS_JOB_BUILD_URL']
            ),
            match={
                'ENV': os.environ['DEPLOY_ENV'],
                'REGION': os.environ['DEPLOY_REGION'],
                'SERVICE': os.environ['DEPLOY_SERVICE']
            },
        ),
        comparator=lambda x: x >= datetime.now() - timedelta(hours=24)
    )
)

if __name__ == '__main__':
    import logging
    import sys

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

    Executor(deploy_playbook).run()
