from database import Database

class MovieCompaniesRoleFactory(Database):

    def insert(self, movie_id, company_id, role_id):
        cnx = self.connect_to_database()
        cursor = self.create_cursor()
        stmt = ("INSERT INTO movies_companies_roles " 
                "(movie_id, company_id, role_id)" 
                "VALUES (%s, %s, %s)")
        mcr_details = (movie_id, company_id, role_id)
        cursor.execute(stmt, mcr_details)
        self.commit()
        self.close_cursor()
        self.disconnect_database()
