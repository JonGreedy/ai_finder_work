from math import ceil

from database.db import get_db
from models.vacancy import Vacancy
from models.company import Company

from flask import Flask, render_template, request
from sqlalchemy import desc, asc, or_, func
from sqlalchemy.sql.expression import nulls_last


app = Flask(__name__)

# Database setup
session = next(get_db())


@app.route('/')
def home():
    return render_template('index.html', current_page='home')


@app.route('/vacancies')
def vacancies():
    # Получаем параметры запроса
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '').strip()

    search_location = request.args.get('search_location', '').strip()

    sort = request.args.get('sort', 'relevance')  # По умолчанию сортируем по новым
    # Фильтры
    salary_from = request.args.get('salary_from', type=int)

    distant_work = request.args.get('distant_work')
    employment_types = request.args.getlist('employment_type')
    # Получаем параметры опыта работы
    experience = request.args.getlist('experience')

    offset = (page - 1) * per_page
    query = session.query(Vacancy)

    # Применяем поиск
    if search:
        query = query.filter(func.lower(Vacancy.title).contains(search.lower()))

    if search_location:
        query = query.filter(Vacancy.locations.contains(search_location.capitalize()))

    # Фильтр по удаленной работе
    if distant_work:
        query = query.filter(Vacancy.distant_work)

    # Фильтр по типу занятости
    if employment_types:
        query = query.filter(Vacancy.employment_type.in_(employment_types))

    # Применяем фильтр по опыту работы
    if experience:
        experience_conditions = []

        for level in experience:
            if level == 'no_experience':
                experience_conditions.append(Vacancy.experience == 'no_experience')
            elif level == 'up_to_one_year':
                experience_conditions.append(Vacancy.experience == 'up_to_one_year')
            elif level == 'year_minimum':
                experience_conditions.append(Vacancy.experience == 'year_minimum')
            elif level == 'two_years_more':
                experience_conditions.append(Vacancy.experience == 'two_years_more')
            elif level == 'three_years_more':
                experience_conditions.append(Vacancy.experience == 'three_years_more')
            elif level == 'five_years_more':
                experience_conditions.append(Vacancy.experience == 'five_years_more')

        if experience_conditions:
            query = query.filter(or_(*experience_conditions))

    # Применяем фильтр по зарплате
    if salary_from:
        query = query.filter(or_(Vacancy.salary_from >= salary_from, Vacancy.salary_to >= salary_from))

    # Применяем сортировку
    if sort == 'newest':
        query = query.order_by(desc(Vacancy.publication_at))
    elif sort == 'oldest':
        query = query.order_by(asc(Vacancy.publication_at))
    elif sort == 'salary_desc':
        query = query.order_by(
            nulls_last(desc(Vacancy.salary_to)),
            nulls_last(desc(Vacancy.salary_from))
        )
    elif sort == 'salary_asc':
        query = query.order_by(
            nulls_last(asc(Vacancy.salary_from)),
            nulls_last(asc(Vacancy.salary_to))
        )
    else:  # relevance или по умолчанию
        query = query.order_by(desc(Vacancy.created_at))

    # Получаем данные с пагинацией
    vacancies = query.offset(offset).limit(per_page).all()
    total_vacancies = query.count()
    total_pages = (total_vacancies + per_page - 1) // per_page

    return render_template(
        'vacancies.html',
        vacancies=vacancies,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
        total_vacancies=total_vacancies,
        current_page='vacancies',
        request_args=request.args  # Передаем все параметры запроса в шаблон
    )

# Остальные маршруты остаются без изменений
@app.route('/vacancy/<int:vacancy_id>')
def vacancy(vacancy_id):
    vacancy = session.query(Vacancy).filter_by(vacancy_id=vacancy_id).first()
    if vacancy is None:
        return "Vacancy not found", 404
    return render_template('vacancy.html', vacancy=vacancy, current_page='vacancy')


@app.route('/companies')
def companies():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    offset = (page - 1) * per_page

    companies = session.query(Company).offset(offset).limit(per_page).all()
    total_companies = session.query(Company).count()
    total_pages = ceil(total_companies / per_page)

    return render_template(
        'companies.html',
        companies=companies,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
        total_companies=total_companies,
        current_page='companies'
    )


@app.route('/company/<int:company_id>')
def company(company_id):
    company = session.query(Company).filter_by(company_id=company_id).first()
    if company is None:
        return "Company not found", 404
    return render_template('company.html', company=company, current_page='company')


if __name__ == '__main__':
    app.run(debug=True)