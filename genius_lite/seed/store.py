import traceback
from collections.abc import Iterable
from genius_lite.log.logger import Logger


class Store:
    _store = []
    current_generator = None

    def put(self, seed_generator):
        if not isinstance(seed_generator, Iterable):
            return
        self._store.append(seed_generator)

    def fetch(self):
        if self.current_generator is None:
            self.current_generator = self._store.pop()
        try:
            seed = self.current_generator.__next__()
            return seed
        except StopIteration:
            self.current_generator = None
            return None
        except:
            Logger.instance().error('\n%s' % traceback.format_exc())
            return None

    @property
    def not_empty(self):
        return self.length or self.current_generator is not None

    @property
    def length(self):
        return len(self._store)
