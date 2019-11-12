from database import Database

class RoleFactory(Database):

    def find_role_id(self,role):
        cnx = self.connect_to_database()
        cursor = self.create_cursor()
        query = ("SELECT id FROM roles WHERE name = {}".format(role))
        cursor.execute(query)
        results = cursor.fetchall()
        self.close_cursor()
        self.disconnect_database
        return results[0]['id']