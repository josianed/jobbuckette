from flask import render_template
from flask import request, redirect, url_for, flash

from . import app
from .database import session, Company, Position, Application

PAGINATE_BY = 10

@app.route("/")
@app.route("/companies")
@app.route("/companies/<int:page>")
def companies(page=1):

    try:
        limit = int(request.args.get('limit', PAGINATE_BY))
        if limit < 10:
            limit = PAGINATE_BY
        if limit > 100:
            limit = 100
    except ValueError:
        limit = PAGINATE_BY

    # Zero-indexed page
    page_index = page - 1

    count = session.query(Company).count()

    start = page_index * limit
    end = start + limit

    total_pages = (count - 1) // limit + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    companies = session.query(Company)
    companies = companies.order_by(Company.name.desc())
    companies = companies[start:end]

    return render_template("companies.html",
        companies=companies,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages
    )

@app.route("/companies/add", methods=["GET"])
def add_company_get():
    return render_template("add_company.html")

@app.route("/companies/add", methods=["POST"])
def add_company_post():
    company = Company(
        name=request.form["inputCompanyName"],
        location=request.form["inputLocation"],
        industry=request.form["inputIndustry"],
        link_to_website=request.form["inputWebsite"],
    )
    session.add(company)
    session.commit()
    return redirect(url_for('companies'))

@app.route("/company/<int:id>/edit")
def edit_company_get(page):
    pass

@app.route("/company/<int:id>/edit")
def edit_company_post(page):
    pass

@app.route("/company/<int:id>/confirm-delete")
def delete_company(page):
    pass

@app.route("/company/<id>/positions")
def positions(id):
    positionsid = int(id) + 1
    positions = session.query(Position)
    for position in positions:
        if str(position.id) == str(positionsid):
            position=position
            break

    return render_template('positions.html',
    positions=positions)

@app.route("/company/position/<int:id>/edit")
def edit_position_get(id):
    pass

@app.route("/company/position/<int:id>/edit")
def edit_position_post(id):
    pass

@app.route("/company/position/<int:id>/confirm-delete")
def delete_position(id):
    pass
