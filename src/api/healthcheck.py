import datetime

from src import utils
from src.utils import make_response


class HealthCheckResource(object):

    def on_get(self, resp):
        make_response(resp, {'status': 'ok', "message": "Hello, world!"})


class VersionResource(object):
    auth = {"auth_disabled": True}

    def on_get(self, req, resp):
        """
        print version as `git describe`; also to print 02 most recent logs `git log -n2`
        """
        logs = req.params.get('logs', '2')
        cmdGetVersion = 'git describe --always'
        cmdGetLog = f"git log --abbrev-commit -n{logs} " \
                    f"--pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset'"
        cmdGetBranch = 'git symbolic-ref --short HEAD'
        cmdwhoami = 'whoami'
        version, _ = utils.run_bash(cmdGetVersion)
        version = version.strip('\n')
        logs, _logs = utils.run_bash_complex(cmdGetLog)
        logs = logs.split('\n')
        logs = [x for x in logs if x]
        branch, _ = utils.run_bash(cmdGetBranch)
        branch = branch.strip('\n')
        whoami, _ = utils.run_bash(cmdwhoami)
        whoami = whoami.strip('\n')

        r = {
            'version': version,
            'logs': logs,
            'branch': branch,
            'who': whoami,
            'misc': {
                'now': {
                    'utc': datetime.datetime.utcnow().isoformat(),
                },
            },
        }
        make_response(resp, r)
