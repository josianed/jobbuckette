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

@app.route("/companies/<int:coid>/edit")
def edit_company_get(coid):
    pass

@app.route("/companies/<int:coid>/edit")
def edit_company_post(coid):
    pass

@app.route("/companies/<int:coid>/confirm-delete", methods=["GET"])
def delete_company_get(coid):
    company = session.query(Company).get(coid)
    return render_template("delete_company.html", company=company)
#
@app.route("/companies/<int:coid>/delete", methods=["GET", "DELETE"])
def delete_company(coid):
    company = session.query(Company).get(coid)
    session.delete(company)
    session.commit()
    return redirect(url_for('companies'))

@app.route("/companies/<int:coid>/positions", methods=["GET"])
def positions(coid):
    company = session.query(Company).get(id)
    positions = session.query(Position).filter(Position.company_id == id).all()
    return render_template('positions.html', positions=positions)

@app.route("/companies/<int:coid>/positions/add", methods=["GET"])
def add_position_get(coid):
    company = session.query(Company).get(coid)
    position = session.query(Position).filter(Position.company_id == coid).all()
    return render_template("add_position.html", company=company, position=position)

@app.route("/companies/<int:coid>/positions/add", methods=["POST"])
def add_position_post(coid):
    position = Position(
        position_name=request.form["inputPositionName"],
        date_due=request.form["inputDueDate"],
        link_to_website=request.form["inputWebsite"],
        company_id=coid
    )
    session.add(position)
    session.commit()
    return redirect(url_for('positions', coid=coid))

@app.route("/companies/<int:coid>/position/<int:posid>/edit")
def edit_position_get(coid, posid):
    pass

@app.route("/companies/<int:coid>/position/<int:posid>/edit")
def edit_position_post(coid, posid):
    pass

@app.route("/companies/<int:coid>/position/<int:posid>/confirm-delete", methods=["GET", "DELETE"])
def delete_position_get(coid, posid):
    company = session.query(Company).get(coid)
    position = session.query(Position).get(posid)
    return render_template("delete_position.html", position=position, company=company)

@app.route("/companies/<int:coid>/position/<int:posid>/delete", methods=["POST", "DELETE"])
def delete_position(coid):
    company = session.query(Company).get(coid)
    position = session.query(Position).get(posid)
    session.delete(position)
    session.commit()
    return redirect(url_for('positions', company=company, position=position))

@app.route("/companies/<int:coid>/position/<int:posid>")
def application(coid, posid):
    company = session.query(Company).get(coid)
    position = session.query(Position).get(posid)
    application = session.query(Application).filter(Application.position_id == posid).all()
    return render_template("applications.html", application=application, company=company, position=position)
