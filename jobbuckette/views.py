from flask import render_template

from . import app
from .database import session, Entry

@app.route("/")
def companies():
    companies = session.query(Company)
    companies = companies.order_by(Company.company.desc())
    companies = companies.all()
    return render_template("companies.html",
        companies=companies
    )
