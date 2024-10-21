# blog/routes.py

from flask import render_template, request
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm
            
@app.route("/")
def index():
   all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())

   return render_template("homepage.html", all_posts=all_posts)

def create_edit_entry(entry_id=None):
    errors = None
    if entry_id is not None: # edit
        entry = Entry.query.filter_by(id=entry_id).first_or_404()
        form = EntryForm(obj=entry) 
        if form.validate_on_submit():
            form.populate_obj(entry)
            db.session.commit()
            return form
        else:
            errors = form.errors
            return errors
    else:
        form = EntryForm() # create
        if form.validate_on_submit():
            entry = Entry(
                title=form.title.data,
                body=form.body.data,
                is_published=form.is_published.data
            )
            db.session.add(entry)
            db.session.commit()
            return form
        else:
            errors = form.errors
            return errors
            
    

@app.route("/new-post/", methods=["GET", "POST"])
def create_entry():
    if request.method == 'POST':
        form = create_edit_entry()
    return render_template("entry_form.html", form=form, errors=form)
 
@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
    if request.method == 'POST': 
        form = create_edit_entry(entry_id)
    return render_template("entry_form.html", form=form, errors=form)


    

