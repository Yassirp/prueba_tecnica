# src/app/command/config/base.py

import argparse
import asyncio
import inspect

class BaseCommand:
    help = ""

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        raise NotImplementedError

    def run_from_argv(self):
        parser = argparse.ArgumentParser(description=self.help)
        self.add_arguments(parser)
        args = parser.parse_args()
        options = vars(args)
        result = self.handle(**options)
        # Si handle es coroutine, debería usar BaseCommandAsync en lugar de esta clase.
        if inspect.iscoroutine(result):
            raise RuntimeError("handle returned coroutine, but BaseCommand is sync. Use BaseCommandAsync instead.")


class BaseCommandAsync(BaseCommand):
    async def handle(self, *args, **options):
        raise NotImplementedError

    def run_from_argv(self):
        parser = argparse.ArgumentParser(description=self.help)
        self.add_arguments(parser)
        args = parser.parse_args()
        options = vars(args)
        asyncio.run(self.handle(**options))
