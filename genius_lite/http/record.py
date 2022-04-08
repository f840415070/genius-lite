from genius_lite.log.logger import Logger


class Record:
    def __init__(self):
        self.success_count = 0
        self.failure_count = 0
        self.duplicate_count = 0
        self.duplicates = {}
        self.logger = Logger.instance()

    def is_duplicate(self, seed_id):
        return self.duplicates.get(seed_id)

    def show(self):
        self.logger.info(
            'All done! '
            'total %s, successes %s, failures %s, duplicates %s' % (
                self.success_count + self.failure_count + self.duplicate_count,
                self.success_count,
                self.failure_count,
                self.duplicate_count
            )
        )

    def success(self, seed_id):
        self.success_count += 1
        self.duplicates[seed_id] = 1

    def failure(self):
        self.failure_count += 1

    def duplicate(self):
        self.duplicate_count += 1
