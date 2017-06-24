from flask import render_template
from flask import request, redirect, url_for, flash

from . import app
from .database import session, Company

PAGINATE_BY = 10

@app.route("/")
@app.route("/company/<int:page>")
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
