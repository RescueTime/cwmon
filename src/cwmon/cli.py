"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mcwmon` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``cwmon.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``cwmon.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import click
from click_plugins import with_plugins
from pkg_resources import iter_entry_points

from cwmon.metrics import CpuContextSwitchesMetric
from cwmon.metrics import CpuPercentageMetric
from cwmon.metrics import DiskPercentFreeInodesMetric
from cwmon.metrics import DiskPercentFreeSpaceMetric
from cwmon.metrics import FifteenMinuteLoadAvgMetric
from cwmon.metrics import FiveMinuteLoadAvgMetric
from cwmon.metrics import MemoryAvailableMetric
from cwmon.metrics import MemoryAvailablePercentageMetric
from cwmon.metrics import OneMinuteLoadAvgMetric
from cwmon.metrics import TotalProcessesMetric
from cwmon.metrics import ZombieProcessesMetric


class _MonitoringOptions:
    def __init__(self, dry_run):
        self.dry_run = dry_run

    def __repr__(self):
        return "Options: %s".format(self.__dict__)


#: You're going to want to read the docs for `Complex Applications`_
#: to understand ``@click.pass_context`` and ``@click.pass_obj`` and
#: how/why we're using them to propagate options from the top-level
#: command (the one tagged with ``@click.group()``) down to subcommands
#: (the ones tagged with ``@cwmon.command()``).
#:
#: .. _Complex Applications: http://click.pocoo.org/6/complex/


@with_plugins(iter_entry_points('cwmon.plugins'))
@click.group()
@click.option('--dry-run/--no-dry-run', default=False, help="Don't submit metric data to AWS.")
@click.pass_context
def cwmon(ctx, dry_run):
    """CloudWatch-based monitoring for RescueTime."""
    ctx.obj = _MonitoringOptions(dry_run)


@cwmon.command()
@click.argument('paths', nargs=-1,
                type=click.Path(exists=True, file_okay=False))
@click.pass_obj
def free_space(options, paths):
    """Calculate the percentage of each device that is free."""
    if not paths:
        paths = ["/"]

    for p in paths:
        m = DiskPercentFreeSpaceMetric(p)
        if options.dry_run:
            click.echo(str(m))
        else:
            m.put()


@cwmon.command()
@click.argument('paths', nargs=-1,
                type=click.Path(exists=True, file_okay=False))
@click.pass_obj
def free_inodes(options, paths):
    """Calculate the percentage of inodes on each device that are free."""
    if not paths:
        paths = ["/"]

    for p in paths:
        m = DiskPercentFreeInodesMetric(p)
        if options.dry_run:
            click.echo(str(m))
        else:
            m.put()


@cwmon.command()
@click.pass_obj
def total_procs(options):
    """Count the total number of processes."""
    m = TotalProcessesMetric()
    if options.dry_run:
        click.echo(str(m))
    else:
        m.put()


@cwmon.command()
@click.pass_obj
def zombie_procs(options):
    """Count the number of zombie processes."""
    m = ZombieProcessesMetric()
    if options.dry_run:
        click.echo(str(m))
    else:
        m.put()


@cwmon.command()
@click.pass_obj
def load_avg_1(options):
    """Get the 1-minute load average."""
    m = OneMinuteLoadAvgMetric()
    if options.dry_run:
        click.echo(str(m))
    else:
        m.put()


@cwmon.command()
@click.pass_obj
def load_avg_5(options):
    """Get the 5-minute load average."""
    m = FiveMinuteLoadAvgMetric()
    if options.dry_run:
        click.echo(str(m))
    else:
        m.put()


@cwmon.command()
@click.pass_obj
def load_avg_15(options):
    """Get the 15-minute load average."""
    m = FifteenMinuteLoadAvgMetric()
    if options.dry_run:
        click.echo(str(m))
    else:
        m.put()


@cwmon.command()
@click.pass_obj
def cpu_percent(options):
    """Get the percentage utilization of the CPU.

    ..note:: This is across all CPUs, not per-CPU.
    """
    m = CpuPercentageMetric()
    if options.dry_run:
        click.echo(str(m))
    else:
        m.put()


@cwmon.command()
@click.pass_obj
def cpu_ctx_switches(options):
    """Get the number of CPU context switches since boot.

    ..note:: This is across all CPUs, not per-CPU.
    """
    m = CpuContextSwitchesMetric()
    if options.dry_run:
        click.echo(str(m))
    else:
        m.put()


@cwmon.command()
@click.pass_obj
def mem_available(options):
    """Get amount of RAM that is 'available'."""
    m = MemoryAvailableMetric()
    if options.dry_run:
        click.echo(str(m))
    else:
        m.put()


@cwmon.command()
@click.pass_obj
def mem_available_percent(options):
    """Get amount of RAM that is 'available' as a percentage of total RAM."""
    m = MemoryAvailablePercentageMetric()
    if options.dry_run:
        click.echo(str(m))
    else:
        m.put()
