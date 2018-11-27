# -*- coding: utf-8 -*-
# Copyright 2018 New Vector Ltd.

import logging
import re

from synapse.api.errors import NotFoundError
from synapse.http.servlet import RestServlet

logger = logging.getLogger(__name__)


class WellKnownBuilder(object):
    """Utility to construct the well-known response

    Args:
        hs (synapse.server.HomeServer):
    """
    def __init__(self, hs):
        self._public_baseurl = hs.config.public_baseurl
        self._default_identity_server = hs.config.default_identity_server

    def get_well_known(self):
        # if we don't have a public_base_url, we can't help much here.
        if self._public_baseurl is None:
            return None

        result = {
            "m.homeserver": {
                "base_url": self._public_baseurl,
            },
        }

        if self._default_identity_server:
            result["m.identity_server"] = {
                "base_url": self._default_identity_server,
            }

        return result


class WellKnownRestServlet(RestServlet):
    PATTERNS = [re.compile("^/.well-known/matrix/client$")]

    def __init__(self, hs):
        self._well_known_builder = WellKnownBuilder(hs)

    def on_GET(self, request):
        r = self._well_known_builder.get_well_known()
        if not r:
            raise NotFoundError()

        logger.error("returning: %s", r)
        return 200, r


def register_servlets(hs, http_server):
    WellKnownRestServlet(hs).register(http_server)
