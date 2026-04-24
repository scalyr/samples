# Copyright 2014 Scalyr Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------
#
# An example ScalyrMonitor plugin to demonstrate how they can be written.
#
# Note, this can be run in standalone mode by:
#     python -m scalyr_agent.run_monitor -c "{"powerquery": "serverHost=*|group c = count() by serverHost", "token":"read-log-key"}" scalyr_agent.builtin_monitors.test_monitor
#
# author:  Steven Czerwinski <czerwin@scalyr.com>
from __future__ import absolute_import
__author__ = "joelm@sentinelone.com"

import random
import json
import requests

from scalyr_agent import ScalyrMonitor


class RandomMonitor(ScalyrMonitor):
    """
    A Scalyr agent monitor that perfroms a powerquery, converts it to Pandas for further processing, and writes the response back to dataset.
    """
    def _initialize(self):
        """Performs monitor-specific initialization."""
        self.__counter = 0
        self.__powerquery = self._config.get(
            "powerquery",
            convert_to=str,
            default= "serverHost = * | group count() by serverHost",
            required_field=True
        )
        self.__url = self._config.get(
            "url",
            convert_to=str,
            default= "https://app.scalyr.com/api/powerQuery"
        )
        self.__startTime = self._config.get(
            "startTime",
            convert_to=str,
            default= "4h",
        )
        self.__endTime = self._config.get(
            "endTime",
            convert_to=str,
            default= "0h",
        )
        self.__token = self._config.get(
            "token",
            convert_to=str,
            default= "null",
            required_field=True
        )

    def gather_sample(self):
        url = self.__url
        payload = json.dumps({
          "token": self.__token,
          "query": self.__powerquery,
          "startTime": self.__startTime,
          "endTime": self.__endTime
        })
        headers = {
          'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        input_dict = json.loads(response.text)
        values = input_dict['values']
        columns = input_dict['columns']
        columns_array = []
        for column in columns:
            columns_array.append(column['name'])
        columns = columns_array
        
        self.__counter += 1
        
        # Loop through each row and emit back into dataset
        for row in values:
            row_dict = dict(zip(columns, row))
            self._logger.emit_value(
                "-",
                str(row_dict)
            )
