import json
import grequests
import requests
import sys

from datetime import datetime
from localsettings import *


def get_jenkins(jobs):
    reqs = []
    for job in jobs:
        url = ('http://{0}/job/{1}/'
               'lastCompletedBuild/api/json'.format(JENKINS_SERVER, job))
        reqs.append(grequests.get(url, headers={'Accept': 'application/json'}))

    resps = grequests.map(reqs)
    results = {}
    for key, resp in zip(jobs, resps):
        job_time = datetime.strptime(resp.json()['id'], '%Y-%m-%d_%H-%M-%S')
        results[key] = {
            'status': resp.json()['result'] == 'SUCCESS',
            'last_run': job_time.strftime('%s'),
        }

    return results


if __name__ == '__main__':
    result = json.dumps(get_jenkins(JENKINS_JOBS), indent=2)
    status_file = open('status.json', 'w')
    status_file.write(result)
    status_file.close()
