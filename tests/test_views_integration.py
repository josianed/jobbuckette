import os
import unittest
import datetime

from urllib.parse import urlparse

# Configure your app to use the testing database
os.environ["CONFIG_PATH"] = "jobbuckette.config.TestingConfig"

from jobbuckette import app
from jobbuckette.database import Base, engine, session, Company, Position, Application

class TestViews(unittest.TestCase):
    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create test company
        company = Company(
            name="Test Name",
            location="Test Location",
            industry="Test Industry",
            link_to_website="Test Link",
        )
        session.add(company)
        session.commit()

        # Create test position
        position = Position(
            position_name=r"Position Name",
            link_to_website="Some Sample Link",
            company_id=1
        )
        session.add(position)
        session.commit()


    def test_add_company(self):
        response = self.client.post("/companies/add", data={
            "name": "Test Company Name",
            "location": "Test Location",
            "industry": "Test Industry",
            "link_to_website": "http://www.facebook.com"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/companies")
        companies = session.query(Company).all()
        self.assertEqual(len(companies), 1)

        company = companies[1]
        self.assertEqual(company.name, "Test Company Name")
        self.assertEqual(company.location, "Test content")
        self.assertEqual(company.industry, "Test Industry")
        self.assertEqual(company.link_to_website, "http://www.facebook.com")

    def test_add_position(self):
        response = self.client.post("/companies/1/positions/add", data={
            "position_name": "Test Position Name",
            "company_id": 1,
            "link_to_website": "http://www.facebook.com"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/companies/1/positions")
        positions = session.query(Position).all()
        self.assertEqual(len(positions), 1)

        position = positions[0]
        self.assertEqual(position.position_name, "Test Position Name")
        self.assertEqual(position.company_id, 1)
        self.assertEqual(position.link_to_website, "http://www.facebook.com")

    def test_add_application(self):
        response = self.client.post("/companies/1/positions/1/applications/create", data={
            "application_status": "Submitted",
            "contact_info": "Jane Doe +1 514 987-6543",
            "recruitment_process": "Test recruitment process",
            "cv": True,
            "cover_letter": False,
            "application_questions": True,
            "position_id": 1
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/companies/1/positions/1")
        applications = session.query(Application).all()
        self.assertEqual(len(applications), 1)

        application = applications[0]
        self.assertEqual(application.application_status, "Submitted")
        self.assertEqual(application.company_id, "Jane Doe +1 514 987-6543")
        self.assertEqual(application.link_to_website, "Test recruitment process")
        self.assertEqual(application.cv, True)
        self.assertEqual(application.cover_letter, False)
        self.assertEqual(application.application_questions, True)
        self.assertEqual(application.position_id, 1)

    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

if __name__ == "__main__":
    unittest.main()
