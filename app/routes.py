from app import app,bizagi,process_id

from flask import render_template, flash, redirect, session

from app.forms.intialData import InitialData
from app.forms.compileForm import compileForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = InitialData()
    if form.validate_on_submit():
        flash('Login requested for  insuranceId={}'.format(
             form.insuranceId.data))
        data = {"startParameters":[
            {
                "xpath":"Patient.Patient.InsuranceId",
                "value": form.insuranceId.data
            }
        ]}
        response=bizagi.startNewCaseProcess(process=process_id,data=data)
        print(response)
        session["case_id"]=response["value"]
        return redirect('/compileForm')
    return  render_template('home.html',form=form)


@app.route('/compileForm', methods=['GET', 'POST'])
def fillForm():
    form = compileForm()
    print("prima if")
    if form.validate_on_submit():
        flash('Login requested for user {}'.format(
            form.name.data))
        print(session["case_id"])
        workitems=bizagi.getWorkItemCase(process=process_id,case_id=session["case_id"])
        print(workitems)
        if workitems["taskName"] == "FillrequestForm":
            print("trovato")
            data = {"startParameters":[
            {
                "xpath":"Patient.Patient.Email",
                "value": form.mail.data
            },
            {
                "xpath":"Patient.Patient.Name",
                "value": form.name.data
            },
            {
                "xpath":"Patient.Patient.Surname",
                "value": form.surname.data
            }
        ]}
        workExcecute= bizagi.executeWorkItemCase(process=process_id,case_id=session["case_id"],workitems=workitems["id"],data=data)
        print(workExcecute)
        return redirect('/end')
    print("dopo")
    return  render_template('compileForm.html',form=form)


@app.route('/end', methods=['GET', 'POST'])
def end():
    return  "complimenti"