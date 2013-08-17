import json
import grequests
import requests

from datetime import datetime

JENKINS = [
    'marketplace.dev',
    'marketplace.prod'
]


def get_jenkins(jobs):
    reqs = []
    for job in jobs:
        url = ('http://qa-selenium.mv.mozilla.com:8080/job/{0}/'
               'lastCompletedBuild/api/json'.format(job))
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
    print json.dumps(get_jenkins(JENKINS))
