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
