from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Runner
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)



@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/runner', methods=['GET', 'POST'])
@login_required
def runner():
    print(current_user)
    if (request.method == 'POST') and current_user.id == 1: 
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
    return render_template("runner.html", user=current_user)
