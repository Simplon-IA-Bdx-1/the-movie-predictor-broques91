from database import Database
from person import Person

class PeopleFactory(Database):

    def insert(self, person):
        cnx = self.connect_to_database()
        cursor = self.create_cursor()
        stmt = ("INSERT INTO people "
                "(firstname, lastname)" 
                "VALUES (%s, %s)")
        person_details = (
            person.firstname,
            person.lastname,       
        )
        cursor.execute(stmt, person_details)
        cnx.commit()
        person.id = cursor.lastrowid
        self.close_cursor()
        self.disconnect_database()
        return person.id

    def find_one_by_fullname(self, person):
        cnx = self.connect_to_database()
        cursor = self.create_cursor()
        stmt = ("SELECT * FROM people WHERE firstname = {} and lastname = {} LIMIT 1".format(person.firstname, person.lastname))
        cursor.execute(stmt)
        results = cursor.fetchall()
        self.close_cursor()
        self.disconnect_database()
        return results

    def find_one_by_id(self, id):
        cnx = self.connect_to_database()
        cursor = self.create_cursor()
        stmt = ("SELECT * FROM people WHERE id = {}".format(id))
        cursor.execute(stmt)
        result = cursor.fetchall()
        self.close_cursor(cursor)
        self.disconnect_database()
        return result

    def find_all(self):
        cnx = self.connect_to_database()
        cursor = self.create_cursor()
        stmt = ("SELECT * FROM people")
        cursor.execute(stmt)
        results = cursor.fetchall() # liste de données scalaires
        people = []
        for result in results: #result: dictionnaire
            person = Person(
                firstname = result['firstname'],
                lastname = result['lastname'],
            )
            person.id = result['id']
            people.append(person)
        self.close_cursor()
        self.disconnect_database()
        return people

    




    