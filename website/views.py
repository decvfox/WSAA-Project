from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import login_required, current_user
from .models import Runner, User
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
def home():
    users = User.query.order_by(User.id)
    runners = Runner.query.order_by(Runner.user_id)
    return render_template("home.html", user=current_user, runners = runners, users = users)

@views.route('/runner', methods=['GET', 'POST'])
@login_required
def runner():
    if (request.method == 'POST'): 
        name = request.form.get('name')
        jockey = request.form.get('jockey')
        trainer = request.form.get('trainer')
		
        runner = Runner.query.filter_by(name=name).first()
        if runner:
            flash('Horse already exists.', category='error')
        elif len(name) < 5:
            flash('Name must be greater than 5 characters.', category='error')
        elif len(jockey) < 5:
            flash('Jockey must be greater than 5 character.', category='error')
        elif len(trainer) < 5:
            flash('Trainer must be greater than 5 character.', category='error')
        else:
            new_horse = Runner(name = name, jockey=jockey, trainer = trainer, user_id=current_user.id)
            db.session.add(new_horse)
            db.session.commit()
            flash('Horse added', category='success')
    return render_template("runner.jinja2", user=current_user)

@views.route('/delete-runner', methods=['POST'])
def delete_runner():  
    runner = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    runnerId = runner['runnerId']
    runner = Runner.query.get(runnerId)
    if runner:
        if runner.user_id == current_user.id:
            db.session.delete(runner)
            db.session.commit()
    return jsonify({})

@views.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    runner_to_update =  Runner.query.get(id)
    if (request.method == 'POST') and current_user.id == runner_to_update.user_id:
        runner_to_update.name = request.form['name']
        runner_to_update.jockey = request.form['jockey']
        runner_to_update.trainer = request.form['trainer']
        db.session.commit()
        return redirect('/')
    else:
        return render_template('update.html', runner_to_update = runner_to_update, user=current_user)
    
@views.route('/about', methods=['GET'])
def about():
    return render_template("about.html", user=current_user)