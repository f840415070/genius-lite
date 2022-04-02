import traceback
from collections.abc import Iterable
from genius_lite.utils.logger import Logger


class SeedBasket:
    basket = []
    current = None

    def put(self, seeds):
        if not isinstance(seeds, Iterable):
            return
        self.basket.append(seeds)

    def seed(self):
        if self.current is None:
            self.current = self.basket.pop()
        try:
            seed = self.current.__next__()
            return seed
        except StopIteration:
            self.current = None
            return None
        except:
            Logger.instance().error(f'\n{traceback.format_exc()}')
            return None

    @property
    def has_seeds(self):
        return len(self.basket) or self.current is not None
