# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import octoprint.plugin
import flask
import time


class AutoConnectPlugin(octoprint.plugin.EventHandlerPlugin, 
                                octoprint.plugin.RestartNeedingPlugin):

    def on_event(self, event, payload):
        if event == octoprint.events.Events.UPLOAD:
            self._logger.info(
                "Uploaded file detected, connecting and printing...")
            self._auto_connect(payload["path"])

    def _auto_connect(self, file_path):
        printer = self._printer

        if not printer.is_operational():
            printer.connect()

        self._logger.info("Waiting for printer to connect...")
        timeout = 120  # 2 minutes in seconds
        start_time = time.time()

        while not printer.is_operational() and time.time() - start_time < timeout:
            time.sleep(1)
    
        if printer.is_operational():
            self._logger.error("Printer connection OK.")
        else:
            self._logger.error("Printer connection timed out after 2 minutes.")


    def get_update_information(self):
        return dict(
            connectandprint=dict(
                displayName=self._plugin_name,
                displayVersion=self._plugin_version,

                # Version check: github repository
                type="github_release",
                user="lordzurp",
                repo="octoprint_auto-connect",
                current=self._plugin_version,

                # Update method: pip
                pip="https://raw.githubusercontent.com/lordzurp/octoprint_auto-connect/{target_version}/auto-connect.py"
            )
        )

__plugin_name__ = "Auto Connect"
__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_version__ = "1.0.0"
__plugin_description__='Automatically connect to your printer on file upload'
__plugin_author__="lordzurp"
__plugin_url__="https://github.com/lordzurp/octoprint_auto-connect"
__plugin_license__="AGPLv3"
__plugin_implementation__ = AutoConnectPlugin()
__plugin_hooks__ = {
    "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
}