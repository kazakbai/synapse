# -*- coding: utf-8 -*-
# Copyright 2018 New Vector
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from synapse.rest import well_known

from tests import unittest


class WellKnownTests(unittest.HomeserverTestCase):

    servlets = [
        well_known.register_servlets,
    ]

    def make_homeserver(self, reactor, clock):
        config = self.default_config()
        config.public_baseurl = "https://tesths"
        config.default_identity_server = "https://testis"
        hs = self.setup_test_homeserver(config=config)
        return hs

    def test_well_known(self):
        request, channel = self.make_request(
            "GET",
            "/.well-known/matrix/client",
            shorthand=False,
        )
        self.render(request)

        self.assertEqual(request.code, 200)
        self.assertEqual(
            channel.json_body, {
                "m.homeserver": {"base_url": "https://tesths"},
                "m.identity_server": {"base_url": "https://testis"},
            }
        )
