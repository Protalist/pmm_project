from app import app,bizagi,process_id

from flask import render_template, flash, redirect, session,request

from app.forms.intialData import InitialData
from app.forms.compileForm import compileForm
from utili.globalVariable import payments

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = InitialData()
    if request.method == "GET":
        return render_template('home.html',form=form)
    if request.method =="POST":
        session["insuranceId"]= form.insuranceId.data
    return render_template('home.html',form=form)

@app.route('/init', methods=['GET', 'POST'])
def initProcess():
    form = InitialData()
    if form.validate_on_submit():
        flash('Login requested for  insuranceId={}'.format(
             form.insuranceId.data))
        data = {"startParameters":[
            {
                "xpath":"Request.PatientInfo.InsuranceId",
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
        if workitems["taskName"] == "FillRequest":
            print("trovato")
            data = {"startParameters":[
            {
                "xpath":"Request.PatientInfo.Email",
                "value": form.mail.data
            },
            {
                "xpath":"Request.PatientInfo.Name",
                "value": form.name.data
            },
            {
                "xpath":"Request.PatientInfo.Surname",
                "value": form.surname.data
            }
        ]}
            workExcecute= bizagi.executeWorkItemCase(process=process_id,case_id=session["case_id"],workitems=workitems["id"],data=data)
            print(workExcecute)
            return redirect('/ChoosePayment')
    print("dopo")
    return  render_template('compileForm.html',form=form)


@app.route('/ChoosePayment', methods=['GET', 'POST'])
def choosePayment():
    form = compileForm()
    if request.method == 'POST':
        print(request.form["payment"])
        workitems=bizagi.getWorkItemCase(process=process_id,case_id=session["case_id"])
        print(workitems)
        if len(workitems)>0 and workitems["taskName"] == "ChoosePayment":
            print("trovato")
            data = {"startParameters":[
            {
                "xpath":"Request.Payment",
                "value": request.form["payment"]
            }
        ]}
            workExcecute= bizagi.executeWorkItemCase(process=process_id,case_id=session["case_id"],workitems=workitems["id"],data=data)
            print(workExcecute)
            return redirect('/end')
    print(payments)
    return  render_template('choosePayment.html',payments=payments)

@app.route('/end', methods=['GET', 'POST'])
def end():
    return "congratulation"