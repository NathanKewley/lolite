from lolite.lib.hooks.hook_base import HookBase


class Hook(HookBase):


    def __init__(self, logger, arguments):
        super().__init__(logger, arguments)

    def execute_hook(self):
        self._logger.debug(f"Running Bash Hook: {self._arguments}")
        if not self._subproc.run_command_exit_code(f"sh {self._arguments}") == 0:
            raise Exception(f"Bash Hook Retuned non 0 result ({self._arguments})")
