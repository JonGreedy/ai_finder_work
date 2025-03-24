from flask import Flask, render_template, request, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from finder_parser.models.vacancy import Vacancy
from finder_parser.database.db import Base

from math import ceil

app = Flask(__name__)

# Database setup
DATABASE_URL = 'sqlite:///finder_parser/database/vacancies.db'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


# @app.route('/')
# def home():
#     limit = request.args.get('limit', 'all', type=str)

#     if limit == 'all':
#         vacancies = session.query(Vacancy).all()
#     else:
#         per_page = int(limit)
#         vacancies = session.query(Vacancy).limit(per_page).all()

#     total_vacancies = session.query(Vacancy).count()
#     return render_template('index.html', vacancies=vacancies, total_vacancies=total_vacancies)


@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)  # Значение по умолчанию 10
    
    offset = (page - 1) * per_page
    vacancies = session.query(Vacancy).offset(offset).limit(per_page).all()
    total_vacancies = session.query(Vacancy).count()
    total_pages = (total_vacancies + per_page - 1) // per_page  # Округление вверх
    
    return render_template(
        'index.html',  # или ваш шаблон для вакансий
        vacancies=vacancies,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
        total_vacancies=total_vacancies
    )


@app.route('/vacancy/<int:vacancy_id>')
def vacancy(vacancy_id):
    vacancy = session.query(Vacancy).filter_by(vacancy_id=vacancy_id).first()
    if vacancy is None:
        return "Vacancy not found", 404
    return render_template('vacancy.html', vacancy=vacancy)


@app.route('/companies')
def companies():
    # Аналогично можно добавить пагинацию и для компаний
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    offset = (page - 1) * per_page
    
    companies = session.query(Vacancy).offset(offset).limit(per_page).all()
    total_companies = session.query(Vacancy).count()
    total_pages = ceil(total_companies / per_page)
    
    return render_template(
        'companies.html',
        companies=companies,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
        total_companies=total_companies
    )

# @app.route('/companies')
# def companies():
#     companies = session.query(Vacancy).all()
#     return render_template('companies.html', companies=companies)

if __name__ == '__main__':
    app.run(debug=True)
