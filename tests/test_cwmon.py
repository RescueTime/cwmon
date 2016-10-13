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


def test_free_space_without_arguments():
    """Test the free space metric."""
    result = _run_metric('free_space')
    assert result.exit_code == 0
    assert '%' in result.output


def test_free_space_defaults_to_root_volume():
    """Test the defaults for the free space metric."""
    fs_metric = functools.partial(_run_metric, 'free_space')
    result = fs_metric()
    default_output = result.output
    result = fs_metric('/')
    explicit_root_vol_output = result.output
    assert default_output == explicit_root_vol_output


def test_free_space_rejects_nonexistent_paths():
    """Test free space metric's rejection of non-existent paths."""
    totally_made_up_path = "/cwmon/{0}".format(uuid.uuid4())
    result = _run_metric('free_space', totally_made_up_path)
    # 2 is the exit code for a UsageError, which includes bad parameters.
    assert result.exit_code == 2
    # Is this too fragile?
    assert 'Invalid value' in result.output


def test_free_space_rejects_file_arguments():
    """Test free space metric's rejection of files (instead of dirs)."""
    result = _run_metric('free_space', '/etc/hosts')
    # 2 is the exit code for a UsageError, which includes bad parameters.
    assert result.exit_code == 2
    # Is this too fragile?
    assert 'Invalid value' in result.output


def test_free_inodes_without_arguments():
    """Test the free inodes metric."""
    result = _run_metric('free_inodes')
    assert result.exit_code == 0
    assert '%' in result.output


def test_free_inodes_defaults_to_root_volume():
    """Test the defaults for the free inodes metric."""
    fi_metric = functools.partial(_run_metric, 'free_inodes')
    result = fi_metric()
    default_output = result.output
    result = fi_metric('/')
    explicit_root_vol_output = result.output
    assert default_output == explicit_root_vol_output


def test_free_inodes_rejects_nonexistent_paths():
    """Test free inodes metric's rejection of non-existent paths."""
    totally_made_up_path = "/cwmon/{0}".format(uuid.uuid4())
    result = _run_metric('free_inodes', totally_made_up_path)
    # 2 is the exit code for a UsageError, which includes bad parameters.
    assert result.exit_code == 2
    # Is this too fragile?
    assert 'Invalid value' in result.output


def test_free_inodes_rejects_file_arguments():
    """Test free inodes metric's rejection of files (instead of dirs)."""
    result = _run_metric('free_inodes', '/etc/hosts')
    # 2 is the exit code for a UsageError, which includes bad parameters.
    assert result.exit_code == 2
    # Is this too fragile?
    assert 'Invalid value' in result.output

def test_total_procs():
    """Test total processes metric's happy path."""
    result = _run_metric('total_procs')
    assert result.exit_code == 0

def test_zombie_procs():
    """Test zombie processes metric's happy path."""
    result = _run_metric('zombie_procs')
    assert result.exit_code == 0


def test_load_avg_1():
    """Test happy path for 1-min load avg metric."""
    result = _run_metric('load_avg_1')
    assert result.exit_code == 0


def test_load_avg_5():
    """Test happy path for 5-min load avg metric."""
    result = _run_metric('load_avg_5')
    assert result.exit_code == 0


def test_load_avg_15():
    """Test happy path for 15-min load avg metric."""
    result = _run_metric('load_avg_15')
    assert result.exit_code == 0


def test_cpu_percentage():
    """Test happy path for CPU Percentage metric."""
    result = _run_metric('cpu_percent')
    assert result.exit_code == 0


def test_cpu_ctx_switches():
    """Test happy path for CPU context switches metric."""
    result = _run_metric('cpu_ctx_switches')
    assert result.exit_code == 0


def test_mem_available():
    """Test happy path for 'RAM available' metric."""
    result = _run_metric('mem_available')
    assert result.exit_code == 0


def test_mem_available_percent():
    """Test happy path for 'RAM available' metric."""
    result = _run_metric('mem_available_percent')
    assert result.exit_code == 0
