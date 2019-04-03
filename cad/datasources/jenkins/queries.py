

class JenkinsLastSuccessfulParameterizedBuildQuery:
    def __init__(self, client, match={}):
        self.c = client
        self.match = match

    def result(self):
        builds = self.c.builds()
        for build in builds:
            if build.is_success():
                # check to see if this build matches the match dict
                # get all keys from match
                build_params = build.params()
                params_to_check = {k:build_params[k] for k in self.match.keys()}
                if self.match == params_to_check:
                    return [build.datetime()]

        return []

