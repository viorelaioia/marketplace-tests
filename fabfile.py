import os

from datetime import datetime
from fabric.api import lcd
from fabric.api import local
from fabric.api import settings


def push_results():
    project_dir = os.path.dirname(os.path.abspath(__file__))

    with lcd(project_dir):
        local('python cron.py > status.json')
        local('git checkout gh-pages')
        local('git add status.json')
        with settings(warn_only=True):
            local('git commit -m "status update at %s"' %
                  datetime.now().strftime("%B %d, %Y at %H:%M:%S"))
        local('git push origin gh-pages')
