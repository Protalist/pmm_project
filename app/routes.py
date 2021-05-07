from app import app

from flask import render_template, flash, redirect

from app.forms.intialData import InitialData
from app.forms.compileForm import compileForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = InitialData()
    if form.validate_on_submit():
        flash('Login requested for  insuranceId={}'.format(
             form.insuranceId.data))
        return redirect('/compileForm')
    return  render_template('home.html',form=form)


@app.route('/compileForm', methods=['GET', 'POST'])
def fillForm():
    form = compileForm()
    if form.validate_on_submit():
        flash('Login requested for user {}'.format(
            form.name.data))
        return redirect('/end')
    return  render_template('compileForm.html',form=form)


@app.route('/end', methods=['GET', 'POST'])
def end():
    return  "complimenti"