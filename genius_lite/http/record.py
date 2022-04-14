from genius_lite.log.logger import Logger


class Record:
    def __init__(self):
        self.successes = 0
        self.failures = 0
        self.duplicates = 0
        self.succeeded_map = {}
        self.total_time = 0
        self.logger = Logger.instance()

    def is_duplicate(self, seed_id):
        return self.succeeded_map.get(seed_id)

    def show(self):
        total = self.successes + self.failures + self.duplicates
        self.logger.info(
            'Done >>> Total(%s) | Time(%ss) | Successes(%s) | Failures(%s) | Duplicates(%s)' % (
                total,
                self.total_time / 1000,
                self.successes,
                self.failures,
                self.duplicates
            )
        )

    def success(self, seed):
        self.successes += 1
        self.succeeded_map[seed.id] = 1
        self.total_time += seed.time

    def failure(self):
        self.failures += 1

    def duplicate(self):
        self.duplicates += 1
