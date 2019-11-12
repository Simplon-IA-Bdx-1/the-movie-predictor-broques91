from database import Database

class MoviePeopleRoleFactory(Database):

    def insert(self, movie_id, person_id, role_id):
        cnx = self.connect_to_database()
        cursor = self.create_cursor()
        stmt = ("INSERT INTO movies_people_roles " 
                "(movie_id, people_id, role_id)" 
                "VALUES (%s, %s, %s)")
        mpr_details = (movie_id, person_id, role_id)
        cursor.execute(stmt, mpr_details)
        self.commit()
        self.close_cursor()
        self.disconnect_database()
