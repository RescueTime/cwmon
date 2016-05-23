# -*- encoding: utf-8 -*-
"""The home of the various metrics we gather."""
import logging
import os
import socket
from abc import ABCMeta
from abc import abstractmethod
from datetime import datetime
from datetime import timezone

import boto3
import psutil


class Metric(metaclass=ABCMeta):
    """ABC for metrics we track in CloudWatch.

    Usage::

        class FooMetric(Metric):
            def __init__(self, **kwargs):
                super().__init__('Foo', **kwargs)
                self.unit = "foos"

            def _capture(self):
                self.value = 1

        FooMetric().put()
    """

    def __init__(self, name, cw_client=None, **kwargs):
        """Initialize a new ``Metric``.

        :param name: the name of the new ``Metric``
        :type name: :class:`str`
        :param cw_client: the CloudWatch client to use to push this ``Metric``
                          up to AWS. If you do not provide one, a new one will
                          be created.
        :type cw_client: :class:`~botocore.client.CloudWatch` or `None`

        .. note:: This *will* trigger whatever capturing logic is required to
                  gather the relevant data.
        .. note:: The ``Namespace`` of the metric defaults to the hostname.
        """
        self.cloudwatch = (cw_client or
                           boto3.client('cloudwatch', 'us-east-1'))
        self.namespace = socket.gethostname()
        self.name = name
        self.value = None
        self.unit = None
        self.timestamp = datetime.now(timezone.utc)
        self._capture()

    @abstractmethod
    def _capture(self):
        """Capture the actual value to be saved."""
        pass

    def put(self):
        """Push the info represented by this ``Metric`` to CloudWatch."""
        try:
            self.cloudwatch.put_metric_data(
                    Namespace=self.namespace,
                    MetricData=[{
                        'MetricName': self.name,
                        'Value': self.value,
                    }],
                    Timestamp=self.timestamp)
        except Exception:
            logging.exception("Error pushing {0} to CloudWatch.".format(str(self)))

    def __str__(self):
        """A human-readable representation of this ``Metric``."""
        return "{0} - {1}: {2} {3}".format(self.namespace, self.name,
                                           self.value, self.unit)


class DiskFreeSpaceMetric(Metric):
    """Information about the free space on a device."""

    _UNITS = ('bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB')

    def __init__(self, mountpoint):
        """Create a new free space metric."""
        self.mountpoint = mountpoint
        super().__init__("Disk Free Space")
        self.name = "{0} ({1})".format(self.name, self.mountpoint)

    def _capture(self):
        self.value = psutil.disk_usage(self.mountpoint).free
        unit_index = 0
        while self.value >= 1024:
            self.value = self.value / 1024
            unit_index += 1
        self.unit = DiskFreeSpaceMetric._UNITS[unit_index]


class DiskPercentFreeSpaceMetric(Metric):
    """Information about the percent of free space on a device."""

    def __init__(self, mountpoint):
        """Create a new free space metric."""
        self.mountpoint = mountpoint
        super().__init__("Disk Percent Free Space")
        self.name = "{0} ({1})".format(self.name, self.mountpoint)

    def _capture(self):
        self.value = 100 - psutil.disk_usage(self.mountpoint).percent
        self.unit = "%"


class DiskFreeInodesMetric(Metric):
    """Information about the free inodes on a device."""

    def __init__(self, mountpoint):
        """Create a new free space metric."""
        self.mountpoint = mountpoint
        super().__init__("Disk Free Inodes")
        self.name = "{0} ({1})".format(self.name, self.mountpoint)

    def _capture(self):
        self.value = os.statvfs(self.mountpoint).f_ffree
        self.unit = "inodes"


class DiskPercentFreeInodesMetric(Metric):
    """Information about the percent of free inodes on a device."""

    def __init__(self, mountpoint):
        """Create a new % of inodes that are freee metric."""
        self.mountpoint = mountpoint
        super().__init__("Disk Percent Free Inodes")
        self.name = "{0} ({1})".format(self.name, self.mountpoint)

    def _capture(self):
        free = os.statvfs(self.mountpoint).f_ffree
        total = os.statvfs(self.mountpoint).f_files
        self.value = round(100 * (free / total), 1)
        self.unit = "%"


class TotalProcessesMetric(Metric):
    """Information about the total number of processes."""

    def __init__(self):
        """Create a new metric for the number of total processes."""
        super().__init__("Total Processes Metric")

    def _capture(self):
        self.value = len(psutil.pids())
        self.unit = "processes"


class ZombieProcessesMetric(Metric):
    """Information about the number of zombie processes."""

    def __init__(self):
        """Create a new metric for the number of zombie processes."""
        super().__init__("Zombie Processes Metric")

    def _capture(self):
        zombies = [p for p in psutil.process_iter()
                   if p.status() == psutil.STATUS_ZOMBIE]
        self.value = len(zombies)
        self.unit = "zombie processes"


class OneMinuteLoadAvgMetric(Metric):
    """The 1-minute load average."""

    def __init__(self):
        """Create a new metric for the 1-minute load avg."""
        super().__init__("1-Minute Load Avg")

    def _capture(self):
        self.value = os.getloadavg()[0]


class FiveMinuteLoadAvgMetric(Metric):
    """The 5-minute load average."""

    def __init__(self):
        """Create a new metric for the 5-minute load avg."""
        super().__init__("5-Minute Load Avg")

    def _capture(self):
        self.value = os.getloadavg()[1]


class FifteenMinuteLoadAvgMetric(Metric):
    """The 15-minute load average."""

    def __init__(self):
        """Create a new metric for the 15-minute load avg."""
        super().__init__("15-Minute Load Avg")

    def _capture(self):
        self.value = os.getloadavg()[2]


class CpuPercentageMetric(Metric):
    """The percent of the CPU currently being used."""

    def __init__(self):
        """Create a new metric for the percent of the CPU being used."""
        super().__init__("CPU Percentage")

    def _capture(self):
        self.value = psutil.cpu_percent(interval=.1)


class CpuContextSwitchesMetric(Metric):
    """The number of CPU context switches since boot."""

    def __init__(self):
        """Create a new metric for the number of CPU context switches since boot."""
        super().__init__("CPU Context Switches")

    def _capture(self):
        self.value = psutil.cpu_stats().ctx_switches


class MemoryAvailableMetric(Metric):
    """The amount of memory 'available'.

    This number is calculated different ways depending on platform, and
    is likely not the same as physically unallocated memory, thanks to
    virtual memory.
    """

    _UNITS = ('bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB')

    def __init__(self):
        """Create a new metric for the amount of RAM available."""
        super().__init__("Available Memory")

    def _capture(self):
        self.value = psutil.virtual_memory().available
        unit_index = 0
        while self.value >= 1024:
            self.value = self.value / 1024
            unit_index += 1
        self.unit = MemoryAvailableMetric._UNITS[unit_index]


class MemoryAvailablePercentageMetric(Metric):
    """The amount of memory 'available' as a percentage of total memory.

    This number is calculated different ways depending on platform, and
    is likely not the same as physically unallocated memory, thanks to
    virtual memory.
    """

    def __init__(self):
        """Create a new metric for the amount of RAM available."""
        super().__init__("Available Memory Percentage")

    def _capture(self):
        self.value = round(100 - psutil.virtual_memory().percent, 1)
        self.unit = '%'
