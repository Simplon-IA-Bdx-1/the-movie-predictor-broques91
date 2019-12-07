from database import Database
from company import Company

class CompanyFactory(Database):

    def insert(self, company):
        cnx = self.connect_to_database()
        cursor = self.create_cursor()
        stmt = "INSERT INTO companies (name) VALUES (%s)"
        company_details = company.name
        cursor.execute(stmt, (company_details,))
        self.commit()
        company.id = cursor.lastrowid
        self.close_cursor()
        self.disconnect_database()
        return company.id