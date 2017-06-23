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
    link_to_website = "this-is-a-link.com"

    for i in range(10):
        company = Company(name="company {}".format(i), location=location,
                    industry=industry, link_to_website=link_to_website)
        session.add(company)
    session.commit()

if __name__ == "__main__":
    manager.run()
