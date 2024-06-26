from datetime import datetime
import os

from flask import Flask, render_template, request, redirect, url_for, session
from passlib.hash import pbkdf2_sha256

from model import Task, User

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY').encode()

@app.route('/all')
def all_tasks():
    return render_template('all.jinja2', tasks=Task.select())


@app.route('/create', methods=['GET', 'POST'])
def create():
    #Check if the user is logged in; if not, prompt user to login:
    if 'username' not in session:
        return redirect(url_for('login'))
    # If the method is POST:
    #    then use the name that the user submitted to create a
    #    new task and save it
    if request.method == 'POST':
        task = Task(task=request.form['username'])
        task.save()

        # Then, redirect the user to the list of all tasks
        return redirect(url_for('all_tasks'))

    # Otherwise, just render the create.jinja2 template
    else:
        return render_template('create.jinja2')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # If the user is attempting to submit the login form (method is POST)
    #    Find a user from the database that matches the username provided in the form submission
    if request.method == 'POST':
        user = User.select().where(User.username == request.form['username']).get()

    #    If you find such a user and their password matches the provided password:
    #        Then log the user in by settings session['username'] to the users name
    #        And redirect the user to the list of all tasks
        if user and pbkdf2_sha256.verify(request.form['password'], user.password):
            session['username'] = request.form['username']
            return redirect(url_for('all_tasks'))
        
        #    Else:
        #        Render the login.jinja2 template and include an error message 
        return render_template('login.jinja2', error="Incorrect username or password.")

    # Else the user is just trying to view the login form
    #    so render the login.jinja2 template
    else:
        return render_template('login.jinja2')


@app.route('/incomplete', methods=['GET', 'POST'])
def incomplete_tasks():
    # If the visitor is not logged in as a user:
        # Then redirect them to the login page
    if 'username' not in session:
        return redirect(url_for('login'))

    # If the request method is POST
        # Then retrieve the username from the session and find the associated user
    if request.method == 'POST':
        user = User.select().where(User.username == session['username']).get()

        # Retrieve the task_id from the form submission and use it to find the associated task 
        # Update the task to indicate that it has been completed at datetime.now() by the current user 
        Task.update(performed=datetime.now(), performed_by=user)\
            .where(Task.id == request.form['task_id'])\
            .execute()

    # Retrieve a list of all incomplete tasks 
    # Render the incomplete.jinja2 template, injecting in the list of all incomplete tasks
    return render_template('incomplete.jinja2', tasks=Task.select().where(Task.performed.is_null()))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)