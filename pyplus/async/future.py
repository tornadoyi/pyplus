

import asyncio

_base_set_result = asyncio.Future.set_result

def _set_result(self, result):
    if self.done() or self.cancelled(): return
    _base_set_result(self, result)

asyncio.Future.set_result = _set_result


_base_set_exception = asyncio.Future.set_exception

def _set_exception(self, exception):
    if self.done() or self.cancelled(): return
    _base_set_exception(self, exception)

asyncio.Future.set_exception = _set_exception