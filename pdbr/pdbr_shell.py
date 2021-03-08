import sys
from functools import partial

from pdbr.__main__ import pdbr as pdbr_klass


def shell():
    try:
        from IPython.terminal.interactiveshell import TerminalInteractiveShell
        from IPython.terminal.ipapp import TerminalIPythonApp
        from traitlets import Type
    except ModuleNotFoundError as error:
        raise type(error)(
            "In order to use pdbr shell, install IPython with pdbr[ipython]"
        ) from error

    class PdbrTerminalInteractiveShell(TerminalInteractiveShell):
        @property
        def debugger_cls(self):
            return partial(pdbr_klass)

    class PdbrTerminalIPythonApp(TerminalIPythonApp):
        interactive_shell_class = Type(
            klass=object,  # use default_value otherwise which only allow subclasses.
            default_value=PdbrTerminalInteractiveShell,
            help=(
                "Class to use to instantiate the TerminalInteractiveShell object. "
                "Useful for custom Frontends"
            ),
        ).tag(config=True)

    app = PdbrTerminalIPythonApp.instance()
    app.initialize()
    sys.exit(app.start())
