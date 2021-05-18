from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://aarbaz77:pock1234@cluster0.dqqjg.mongodb.net/mydb?retryWrites=true&w=majority'
mongo = PyMongo(app)

todos = mongo.db.todos
jobvacancy = mongo.db.jobvacancy
@app.route('/')
def navigation():
    return render_template('navigationpage.html')

@app.route('/apprenticeshipadd')
def apprenticeshippage():
    saved_todos = todos.find()
    print(saved_todos)
    return render_template('apprenticeship.html', todos=saved_todos)

@app.route('/add', methods=['POST'])
def add_todo():
    title = request.form.get('app-title')
    company = request.form.get('app-company')
    university = request.form.get('app-university')
    description = request.form.get('app-description')
    todos.insert_one({'title' : title, 'university':university,'company':company,'description':description, 'complete':False})
    return redirect(url_for('apprenticeshippage'))

@app.route('/complete/<oid>')
def complete(oid):
    todo_item = todos.find_one({'_id': ObjectId(oid)})
    todo_item['complete'] = True
    todos.save(todo_item)
    return redirect(url_for('apprenticeshippage'))

@app.route('/delete_completed')
def delete_completed():
    todos.delete_many({'complete' : True})
    return redirect(url_for('apprenticeshippage'))

@app.route('/delete_all')
def delete_all():
    todos.delete_many({})
    return redirect(url_for('apprenticeshippage'))

@app.route('/apprenticeship', methods=['GET'])
def get_all_apprenticeship_list():
    results = []
    for r in todos.find():
        results.append({'title': r['title'], 'company':r['company'],'university': r['university'],'description':r['description'],'completed': r['complete']})
    return jsonify({'result':results})

#Job Vacancy adder
@app.route('/vacancyadd')
def vacancy():
    saved_jobvacancy = jobvacancy.find()
    print(saved_jobvacancy)
    return render_template('vacancies.html', jobvacancys=saved_jobvacancy)

@app.route('/addvacancy', methods=['POST'])
def addvacancy():
    title = request.form.get('app-title')
    company = request.form.get('app-company')
    location = request.form.get('app-location')
    salary = request.form.get('app-salary')
    description = request.form.get('app-description')
    jobvacancy.insert_one({'title' : title, 'salary':salary,'company':company,'location':location,'description':description, 'complete':False})
    return redirect(url_for('vacancy'))

@app.route('/completevacany/<oid>')
def completevacany(oid):
    jobvacancys_item = jobvacancy.find_one({'_id': ObjectId(oid)})
    jobvacancys_item['complete'] = True
    jobvacancy.save(jobvacancys_item)
    return redirect(url_for('vacancy'))

@app.route('/delete_vacancy_completed')
def delete_vacancy_completed():
    jobvacancy.delete_many({'complete' : True})
    return redirect(url_for('vacancy'))

@app.route('/delete_vacancy_all')
def delete_vacancy_all():
    jobvacancy.delete_many({})
    return redirect(url_for('vacancy'))

# @app.route('/vacancy', methods=['GET'])
# def get_all_vacancy_list():
#     results = []
#     for r in jobvacancy.find():
#         results.append({'title': r['title'], 'company':r['company'],'location':r['location'], 'salary': r['salary'],'description':r['description'],'completed': r['complete']})
#     return jsonify({'result':results})

@app.route('/vacancy/<locat>', methods=['GET'])
def get_all_vacancy_list(locat):
    results = []
    for r in jobvacancy.find({'location': locat}):
        results.append({'title': r['title'], 'company':r['company'],'location':r['location'], 'salary': r['salary'],'description':r['description'],'completed': r['complete']})
    return jsonify({'result':results})

if __name__ == "__main__":
    app.run(debug=True)
