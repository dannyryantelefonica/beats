import jinja2
import os
import platform
import sys
import time
import unittest

from auditbeat_xpack import *

COMMON_FIELDS = ["@timestamp", "host.name", "event.module", "event.dataset"]


class Test(AuditbeatXPackTest):

    def test_metricset_host(self):
        """
        host metricset collects general information about a server.
        """

        fields = ["system.audit.host.uptime", "system.audit.host.ip", "system.audit.host.os.name"]

        # Metricset is experimental and that generates a warning, TODO: remove later
        self.check_metricset("system", "host", COMMON_FIELDS + fields, warnings_allowed=True)

    @unittest.skipIf(sys.platform == "win32", "Not implemented for Windows")
    @unittest.skipIf(sys.platform == "linux2" and platform.linux_distribution()[0] != "debian",
                     "Only implemented for Debian")
    def test_metricset_package(self):
        """
        package metricset collects information about installed packages on a system.
        """

        fields = ["system.audit.package.name", "system.audit.package.version", "system.audit.package.installtime"]

        # Metricset is experimental and that generates a warning, TODO: remove later
        self.check_metricset("system", "package", COMMON_FIELDS + fields, warnings_allowed=True)

    def test_metricset_process(self):
        """
        process metricset collects information about processes running on a system.
        """

        fields = ["process.pid", "process.ppid", "process.name", "process.executable", "process.args",
                  "process.start", "process.working_directory", "user.id", "user.group.id", "user.group.name"]

        # Windows does not have effective and saved IDs, and user.name is not always filled for system processes.
        if sys.platform != "win32":
            fields.extend(["user.effective.id", "user.saved.id", "user.effective.group.id", "user.saved.group.id",
                           "user.name"])

        # Metricset is experimental and that generates a warning, TODO: remove later
        self.check_metricset("system", "process", COMMON_FIELDS + fields, warnings_allowed=True)

    @unittest.skipUnless(sys.platform == "linux2", "Only implemented for Linux")
    def test_metricset_socket(self):
        """
        socket metricset collects information about open sockets on a system.
        """

        fields = ["destination.port"]

        # errors_allowed=True - The socket metricset fills the `error` field if the process enrichment fails
        # (e.g. process has exited). This should not fail the test.
        # warnings_allowed=True - Metricset is experimental and that generates a warning, TODO: remove later
        self.check_metricset("system", "socket", COMMON_FIELDS + fields, errors_allowed=True, warnings_allowed=True)

    @unittest.skipUnless(sys.platform == "linux2", "Only implemented for Linux")
    def test_metricset_user(self):
        """
        user metricset collects information about users on a server.
        """

        fields = ["system.audit.user.name"]

        # Metricset is experimental and that generates a warning, TODO: remove later
        self.check_metricset("system", "user", COMMON_FIELDS + fields, warnings_allowed=True)
