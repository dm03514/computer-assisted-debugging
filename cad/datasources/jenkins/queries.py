import logging

logger = logging.getLogger(__name__)


class JenkinsLastSuccessfulParameterizedBuildQuery:
    def __init__(self, client, match={}):
        self.c = client
        self.match = match

    def result(self):
        builds = self.c.builds()
        result = []
        for build in builds:
            if build.is_success():
                # check to see if this build matches the match dict
                # get all keys from match
                build_params = build.params()
                params_to_check = {k:build_params[k] for k in self.match.keys()}
                if self.match == params_to_check:
                    logger.debug({'match': params_to_check})
                    result = [build.datetime()]
                    break

        logger.debug({'result': result})
        return result

