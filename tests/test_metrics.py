# -*- encoding: utf-8 -*-
"""Tests for the various metrics reported by the monitoring CLI."""
from unittest import mock
import pytest

from cwmon import metrics


class AbstractTestMetric(metrics.Metric):
    """:class:`~cwmon.metrics.Metric` subclass you can't instantiate."""

    def __init__(self, **kwargs):
        """Chain to super."""
        super().__init__('Abstract', **kwargs)


class ConcreteTestMetric(metrics.Metric):
    """:class:`~cwmon.metrics.Metric` subclass you can instantiate."""

    def __init__(self, **kwargs):
        """Chain to super."""
        super().__init__('Concrete', mock.Mock(), **kwargs)

    def _capture(self):
        self.value = 1
        self.unit = str(self)


def test_cant_instantiate_Metric():
    """Ensure you can't instantiate :class:`~cwmon.metrics.Metric`."""
    with pytest.raises(TypeError):
        metrics.Metric()


def test_cant_instantiate_AbstractTestMetric():
    """Ensure you can't instantiate a subclass of :class:`~cwmon.metrics.Metric` that doesn't override :method:`~cwmon.metrics.Metric#_capture`."""
    with pytest.raises(TypeError):
        AbstractTestMetric()


def test_can_instantiate_ConcreteTestMetric():
    """Ensure you can instantiate a subclass of :class:`~cwmon.metrics.Metric` if it overrides :method:`~cwmon.metrics.Metric#_capture`."""
    ConcreteTestMetric()


def test_put_hits_the_cw_client():
    """Make sure :method:`~cwmon.metrics.Metric.put` hits CloudWatch."""
    c = ConcreteTestMetric()
    c.put()
    assert c.cloudwatch.put_metric_data.called


def test_put_swallows_exceptions():
    """Make sure :method:`~cwmon.metrics.Metric.put` doesn't propagate exceptions."""
    c = ConcreteTestMetric()
    # Make the CloudWatch client have a hissy when someone calls ``put_metric_data``.
    attrs = {'put_metric_data.side_effect': Exception}
    c.cloudwatch = mock.Mock(**attrs)
    # Now let's watch the magic happen.
    c.put()
    # If you want to verify that an Exception did get swallowed, you
    # can look at the coverage report to verify that the logging of the
    # exception was executed.
    assert c.cloudwatch.put_metric_data.called
