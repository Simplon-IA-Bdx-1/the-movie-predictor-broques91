class Movie:

    def __init__(self, title, original_title, synopsis, duration, rating, release_date, imdb_id):

        self.title = title
        self.original_title = original_title
        self.synopsis = synopsis
        self.duration = duration
        self.rating = rating
        self.release_date = release_date
        self.imdb_id = imdb_id

        self.id = None
        self.actor = []
        self.writer = []
        self.is_3d = None
        self.marketing_budget = None
        self.production_budget = None

    def __repr__(self):
        return "#{}: {} released on {}".format(self.id, self.title, self.release_date)

    def total_budget(self):
        if self.production_budget == None and self.marketing_budget == None:
            return None

        return self.marketing_budget + self.production_budget