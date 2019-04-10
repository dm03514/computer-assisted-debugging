from datetime import datetime

import requests


BUILD_SUCCESS = 'SUCCESS'
PARAMETERS_ACTION = 'hudson.model.ParametersAction'


class Build:
    def __init__(self, data):
        self.data = data

    def is_success(self):
        return self.data['result'] == BUILD_SUCCESS

    def params(self):
        # can a job have multiple params????
        for action in self.data.get('actions', []):
            if action['_class'] == PARAMETERS_ACTION:
                return {p['name']:p['value'] for p in action.get('parameters', [])}
        return {}

    def datetime(self):
        return datetime.fromtimestamp(self.data['timestamp'] / 1000)


class Client:
    def __init__(self, username, password, job_build_url, requests=None):
        self.username = username
        self.password = password
        self.job_build_url = job_build_url
        self.requests = requests if requests is None else requests

    def builds(self):
        query = {
            'tree': 'builds[actions[parameters[name,value]],number,status,timestamp,id,result,parameter]'
        }
        resp = requests.get(
            self.job_build_url,
            params=query,
            auth=(self.username, self.password)
        )
        assert resp.status_code == 200, resp.status_code
        return [Build(b) for b in resp.json().get('builds')]
