class Movie:

    def __init__(self, title, original_title, duration, release_date, rating):
        self.title = title
        self.original_title = original_title
        self.duration = duration
        self.release_date = release_date
        self.rating = rating

        self.id = None
        self.actor = []
        self.producer = []
        self.is_3d = None
        self.marketing_budget = None
        self.production_budget = None

    def total_budget(self):
        if self.production_budget == None and self.marketing_budget == None:
            return None

        return self.marketing_budget + self.production_budget