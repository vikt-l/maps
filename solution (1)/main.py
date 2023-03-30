from flask import Flask, render_template, redirect
from data import db_session, jobs_api
from data.users import User
from data.jobs import Jobs
from data.departments import Department
from data.forms import RegisterForm, LoginForm, JobsForm, JobsRedactionForm, DepartmentsForm, DepartmentsRedactionForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(id)


@app.route("/")
def journal_jobs():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return render_template("journal_jobs.html", title='List of Jobs', jobs=jobs)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Wrong email or password",
                               form=form)
    return render_template('login.html', title='Authorisation', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm.data:
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="Passwords don't match")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.login.data).first():
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="This user already exists")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.login.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Registration', form=form)


@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    form = JobsForm()
    if form.submit.data:
        db_sess = db_session.create_session()
        job = Jobs(
            team_leader=form.team_leader.data,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data,
            department=form.department.data
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('add_job.html', title='Adding Job', form=form)


@app.route('/redact_job/<int:job_id>', methods=['GET', 'POST'])
def redact_job(job_id):
    form = JobsRedactionForm()
    if form.submit.data:
        db_sess = db_session.create_session()
        if current_user.id != 1:
            job = db_sess.query(Jobs).filter(Jobs.id == job_id, Jobs.team_leader == current_user.id).first()
        else:
            job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
        if job:
            job.team_leader = form.team_leader.data if form.team_leader.data else job.team_leader
            job.job = form.job.data if form.job.data else job.job
            job.work_size = form.work_size.data if form.work_size.data else job.work_size
            job.collaborators = form.collaborators.data if form.collaborators.data else job.collaborators
            job.is_finished = form.is_finished.data if form.is_finished.data else job.is_finished
            job.department = form.department.data if form.department.data else job.department
            db_sess.commit()
            return redirect('/')
    return render_template('redact_job.html', title=f'Redacting Job: {job_id}', form=form)


@app.route('/delete_job/<int:job_id>', methods=['GET', 'POST'])
def delete_job(job_id):
    db_sess = db_session.create_session()
    if current_user.id != 1:
        job = db_sess.query(Jobs).filter(Jobs.id == job_id, Jobs.team_leader == current_user.id).first()
    else:
        job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
    return redirect('/')


@app.route("/departments")
def journal_departments():
    session = db_session.create_session()
    departments = session.query(Department).all()
    return render_template("journal_departments.html", title='List of Departments', departments=departments)


@app.route('/add_department', methods=['GET', 'POST'])
def add_department():
    form = DepartmentsForm()
    if form.submit.data:
        db_sess = db_session.create_session()
        department = Department(
            title=form.title.data,
            chief=current_user.id,
            members=form.members.data,
            email=form.email.data
        )
        db_sess.add(department)
        db_sess.commit()
        return redirect('/departments')
    return render_template('add_department.html', title='Adding Department', form=form)


@app.route('/redact_department/<int:department_id>', methods=['GET', 'POST'])
def redact_department(department_id):
    form = DepartmentsRedactionForm()
    if form.submit.data:
        db_sess = db_session.create_session()
        if current_user.id != 1:
            department = db_sess.query(Department).filter(Department.id == department_id,
                                                          Department.chief == current_user.id).first()
        else:
            department = db_sess.query(Department).filter(Department.id == department_id).first()
        if department:
            department.title = form.title.data if form.title.data else department.title
            department.chief = form.chief.data if form.chief.data else department.chief
            department.members = form.members.data if form.members.data else department.members
            department.email = form.email.data if form.email.data else department.email
            db_sess.commit()
            return redirect('/departments')
    return render_template('redact_department.html', title=f'Redacting Department: {department_id}', form=form)


@app.route('/delete_department/<int:department_id>', methods=['GET', 'POST'])
def delete_department(department_id):
    db_sess = db_session.create_session()
    if current_user.id != 1:
        department = db_sess.query(Department).filter(Department.id == department_id,
                                                      Department.chief == current_user.id).first()
    else:
        department = db_sess.query(Department).filter(Department.id == department_id).first()
    if department:
        db_sess.delete(department)
        db_sess.commit()
    return redirect('/departments')


def main():
    name_db = 'mars_explorer.db'
    db_session.global_init(f"db/{name_db}")
    app.register_blueprint(jobs_api.blueprint)
    app.run(port=5050)


if __name__ == '__main__':
    main()
