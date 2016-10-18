# -*- encoding: utf-8 -*-
"""The home of the various metrics we gather."""
import logging
import socket
from abc import ABCMeta
from abc import abstractmethod
from datetime import datetime
from datetime import timezone

import boto3


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
                        'Timestamp': self.timestamp
                    }]
            )
        except Exception:
            logging.exception("Error pushing {0} to CloudWatch.".format(str(self)))

    def __str__(self):
        """A human-readable representation of this ``Metric``."""
        return "{0} - {1}: {2} {3}".format(self.namespace, self.name,
                                           self.value, self.unit)
