from database import Database
from movie import Movie

class MovieFactory(Database):

    def insert(self, movie):
        cnx = self.connect_to_database()
        cursor = self.create_cursor()
        stmt = ("INSERT INTO movies "
                "(title, original_title, synopsis, duration, rating, release_date, budget, revenue, imdb_id, score)" 
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        movie_details = (
            movie.title,
            movie.original_title,
            movie.synopsis,
            movie.duration,
            movie.rating,
            movie.release_date,
            movie.budget,
            movie.revenue,
            movie.imdb_id,
            movie.score
        )
        cursor.execute(stmt, movie_details)
        cnx.commit()
        last_id = cursor.lastrowid
        self.close_cursor()
        self.disconnect_database()
        return last_id

    def find_one_by_id(self, id):
        cnx = self.connect_to_database()
        cursor = self.create_cursor()
        stmt = ("SELECT * FROM movies WHERE id = {} LIMIT 1".format(id))
        cursor.execute(stmt)
        results = cursor.fetchall()
        movie = None 
        if cursor.rowcount == 1:
            row = results[0]
            movie = Movie(
                title=row['title'], 
                original_title= row['original_title'], 
                synopsis= row['synopsis'], 
                duration= row['duration'],
                rating = row['rating'], 
                release_date = row['release_date'],
                budget = row['budget'], 
                revenue = row['revenue'] ,
                imdb_id = row['imdb_id'], 
                score = row['vote_average'] 
                )
            movie.id = row['id']
        self.close_cursor()
        self.disconnect_database()
        return movie

    def find__one_by_imdb_id(self, imdb_id):
        cnx = self.connect_to_database()
        cursor = self.create_cursor()
        stmt = ("SELECT * FROM movies WHERE imdb_id = {}".format(imdb_id))
        cursor.execute(stmt)
        result = cursor.fetchall()
        self.close_cursor(cursor)
        self.disconnect_database()
        return result

    def find_all(self):
        cnx = self.connect_to_database()
        cursor = self.create_cursor()
        stmt = ("SELECT * FROM movies")
        cursor.execute(stmt)
        results = cursor.fetchall() # liste de données scalaires
        movies = []
        for result in results: #result: dictionnaire
            movie = Movie(
                title = result['title'],
                original_title = result['original_title'],
                synopsis = result['synopsis'],
                duration = result['duration'],
                rating = result['rating'],
                release_date = result['release_date'],
                budget = result['budget'],
                revenue = result['revenue'],
                imdb_id = result['imdb_id'],
                score = result['score']
            )
            movie.id = result['id']
            movies.append(movie)
        self.close_cursor()
        self.disconnect_database()
        return movies

    




    