from flask import render_template

from . import app
from .database import session, Company

@app.route("/")
def companies():
    companies = session.query(Company)
    companies = companies.order_by(Company.name.desc())
    companies = companies.all()
    return render_template("companies.html",
        companies=companies
    )
