# -*- encoding: utf-8 -*-
"""Tests for the monitoring CLI.

.. danger:: You **must** pass the `--dry-run` flag in all tests. Failure to do
            so will result in flooding AWS CloudWatch with bogus stats.
"""
import functools
import uuid
from click.testing import CliRunner

from cwmon.cli import cwmon


def _run_metric(name, *args):
    """Run the named metric, passing ``args``, and return the results."""
    runner = CliRunner()
    my_args = ['--dry-run', name]
    my_args.extend(args)
    return runner.invoke(cwmon, my_args)


def test_cwmon():
    """Test the primary entrypoint of the CLI."""
    runner = CliRunner()
    result = runner.invoke(cwmon, [])

    assert result.output.startswith('Usage')
    assert result.exit_code == 0
