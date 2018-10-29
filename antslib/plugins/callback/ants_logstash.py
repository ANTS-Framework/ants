# (C) 2016, Ievgen Khmelenko <ujenmr@gmail.com>
# (C) 2017 Ansible Project
# (C) 2018 University of Basel
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
import copy
__metaclass__ = type

DOCUMENTATION = '''
    callback: ants_logstash
    type: notification
    short_description: Sends events to Logstash
    description:
      - This callback will report facts and task events to Logstash https://www.elastic.co/products/logstash
    version_added: "2.3"
    requirements:
      - whitelisting in configuration
      - logstash (python library)
    options:
      server:
        description: Address of the Logstash server
        env:
          - name: LOGSTASH_SERVER
        default: localhost
      port:
        description: Port on which logstash is listening
        env:
            - name: LOGSTASH_PORT
        default: 5000
      type:
        description: Message type
        env:
          - name: LOGSTASH_TYPE
        default: ants
'''

import os
import json
import socket
import uuid
from datetime import datetime

import logging

try:
    import logstash
    HAS_LOGSTASH = True
except ImportError:
    HAS_LOGSTASH = False

from ansible.plugins.callback import CallbackBase


class CallbackModule(CallbackBase):
    """
    ansible logstash callback plugin
    ansible.cfg:
        callback_plugins   = <path_to_callback_plugins_folder>
        callback_whitelist = logstash
    and put the plugin in <path_to_callback_plugins_folder>

    logstash config:
        input {
            tcp {
                port => 5000
                codec => json
            }
        }

    Requires:
        python-logstash

    This plugin makes use of the following environment variables:
        LOGSTASH_SERVER   (optional): defaults to localhost
        LOGSTASH_PORT     (optional): defaults to 5000
        LOGSTASH_TYPE     (optional): defaults to ants
    """

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'aggregate'
    CALLBACK_NAME = 'logstash'
    CALLBACK_NEEDS_WHITELIST = True

    def __init__(self):
        super(CallbackModule, self).__init__()

        if not HAS_LOGSTASH:
            self.disabled = True
            self._display.warning("The required python-logstash is not installed. "
                                  "pip install python-logstash")
        else:
            self.logger = logging.getLogger('python-logstash-logger')
            self.logger.setLevel(logging.DEBUG)

            self.handler = logstash.TCPLogstashHandler(
                os.getenv('LOGSTASH_SERVER', 'localhost'),
                int(os.getenv('LOGSTASH_PORT', 5000)),
                version=1,
                message_type=os.getenv('LOGSTASH_TYPE', 'ants')
            )

            self.logger.addHandler(self.handler)
            self.fqdn = socket.getfqdn()
            self.hostname = socket.gethostname()
            self.session = str(uuid.uuid1())
            self.errors = 0

        self.start_time = datetime.utcnow()
        self.base_data = {
                '@host': self.fqdn,
                '@host_short': self.hostname,
                'session': self.session,
        }

    def recurse_results(self, results_dict, data, prefix='ansible_results'):
        for key, value in results_dict.iteritems():
            if type(value) is dict:
                data = self.recurse_results(value, data)
            else:
                data['%s_%s' % (prefix, key)] = value
        return data


    def v2_playbook_on_start(self, playbook):
        self.playbook = playbook._file_name
        data = copy.deepcopy(self.base_data)
        data['status'] = 'OK'
        data['ansible_type'] = 'start'
        data['ansible_playbook'] = self.playbook
        self.logger.info("ansible start", extra=data)

    def v2_playbook_on_stats(self, stats):
        end_time = datetime.utcnow()
        runtime = end_time - self.start_time
        summarize_stat = {}
        for host in stats.processed.keys():
            summarize_stat[host] = stats.summarize(host)

        if self.errors == 0:
            status = "OK"
        else:
            status = "FAILED"

        data = copy.deepcopy(self.base_data)
        data['status'] = status
        data['ansible_type'] = "finish"
        data['ansible_playbook_duration'] = runtime.total_seconds()
        data['ansible_playbook'] = self.playbook

        try:
            data['ansible_result_skipped'] = summarize_stat[self.fqdn]['skipped']
            data['ansible_result_ok'] = summarize_stat[self.fqdn]['ok']
            data['ansible_result_failures'] = summarize_stat[self.fqdn]['failures']
        except KeyError as err:
            data['ansible_logstash_error'] = err
            data['ansible_result'] = json.dumps(summarize_stat)

        self.logger.info("ansible stats", extra=data)

    def v2_runner_on_ok(self, result, **kwargs):
        data = copy.deepcopy(self.base_data)
        data['status'] = "OK"
        data['ansible_type'] = "task"
        data['ansible_task'] = result._task
        data['ansible_playbook'] = self.playbook

        results = self._dump_results(result._result)
        try:
            results_dict = json.loads(results)
            data = self.recurse_results(results_dict, data)
        except KeyError as err:
            data['ansible_logstash_error'] = err
            data['ansible_result'] = results

        self.logger.info("ansible ok", extra=data)

    def v2_runner_on_skipped(self, result, **kwargs):
        data = copy.deepcopy(self.base_data)
        data['status'] = "SKIPPED"
        data['ansible_type'] = "task"
        data['ansible_task'] = result._task
        data['ansible_playbook'] = self.playbook
        self.logger.info("ansible skipped", extra=data)

    def v2_playbook_on_import_for_host(self, result, imported_file):
        data = copy.deepcopy(self.base_data)
        data['status'] = "IMPORTED"
        data['ansible_type'] = "import"
        data['imported_file'] = imported_file
        data['ansible_playbook'] = self.playbook
        self.logger.info("ansible import", extra=data)

    def v2_playbook_on_not_import_for_host(self, result, missing_file):
        data = copy.deepcopy(self.base_data)
        data['status'] = "NOT IMPORTED"
        data['ansible_type'] = "import"
        data['missing_file'] = missing_file
        data['ansible_playbook'] = self.playbook
        self.logger.info("ansible import", extra=data)

    def v2_runner_on_failed(self, result, **kwargs):
        data = copy.deepcopy(self.base_data)
        data['status'] = "FAILED"
        data['ansible_type'] = "task"
        data['ansible_task'] = result._task
        data['ansible_playbook'] = self.playbook
        self.errors += 1

        results = self._dump_results(result._result)
        try:
            results_dict = json.loads(results)
            data = self.recurse_results(results_dict, data)
        except KeyError as err:
            data['ansible_logstash_error'] = err
            data['ansible_result'] = results

        self.logger.error("ansible failed", extra=data)
