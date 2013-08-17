import json
import grequests
import requests

from datetime import datetime

JENKINS = [
    # Payments Dev
    'b2g.unagi.mozril.gaia.v1-train.ui.marketplace_payment',

    # Marketplace Dev on B2G
    'b2g.unagi.mozril.gaia.v1-train.ui.marketplace',

    # Dev Jobs
    'marketplace.dev',
    'marketplace.dev.saucelabs',
    'marketplace.dev.developer_hub',
    'marketplace.dev.developer_hub.saucelabs',
    'marketplace.dev.mobile.saucelabs',

    # Prod Jobs
    'marketplace.prod',
    'marketplace.prod.saucelabs',
    'marketplace.prod.mobile.saucelabs',

    # Stage Jobs
    'marketplace.stage.saucelabs',
    'marketplace.stage.mobile.saucelabs',
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
    print json.dumps(get_jenkins(JENKINS), indent=2)
