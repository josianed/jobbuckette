import os
from flask_script import Manager

from jobbuckette import app
from jobbuckette.database import session, Company, Position, Application, Base

manager = Manager(app)

@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

@manager.command
def seed():
    location = "location y"
    industry = "industry z"
    link_to_website = "www.google.com"

    for i in range(10, 20, 1):
        company = Company(name="company {}".format(i+1), location=location,
                    industry=industry, link_to_website=link_to_website)
        session.add(company)

    for i in range(10, 20, 1):
        position = Position(position_name="position {}".format(i+1),
                    link_to_website="www.position{}.com".format(i+1), company_id=i)

        session.add(position)

    session.commit()
    # session.query(Company).delete()
    # session.query(Position).delete()
    # session.commit()

if __name__ == "__main__":
    manager.run()
