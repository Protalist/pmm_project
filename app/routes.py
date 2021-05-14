from app import app,bizagi,process_id,city

from flask import render_template, flash, redirect, session,request,url_for

from app.forms.intialData import InitialData
from app.forms.compileForm import compileForm
from utili.globalVariable import payments, queries


import random
import datetime

idinsurance="insuranceId"
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = InitialData()
    if request.method == "GET" and not idinsurance  in session :
        return render_template('home.html',form=form)
    if request.method =="POST" or  idinsurance  in session :
        if  request.method =="POST":
            session[idinsurance]= form.insuranceId.data
        data={
        "startParameters": [
            {
                "xpath": "Request.PatientInfo.InsuranceId",
                "value": session[idinsurance]
            }
        ]
        }
        print(session[idinsurance])
        response=bizagi.excecuteQuery(queryid=queries["getCaseFromeInsuranceId"],data=data)
        print(response)
        if len(response)==0:
            render_template('home.html',form=form)
        else:
            return render_template('listOfRequest.html',cases=response)
    return render_template('home.html',form=form,len=len(response))

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
    insuranceId=""
    if "insuranceId" in session:
        insuranceId=session["insuranceId"]
    print(insuranceId)
    return  render_template('home.html',form=form,insuranceId=insuranceId)


@app.route('/compileForm', methods=['GET', 'POST'])
def FillRequest():
    form = compileForm()
    print("prima if")
    if form.validate_on_submit():
        print(session["case_id"])
        workitems=bizagi.getWorkItemCase(process=process_id,case_id=session["case_id"],taskName="FillRequest")
        print(workitems)
        if len(workitems)>0 and workitems["taskName"] == "FillRequest":
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
           # ,            {
            #    "xpath":"Request.City",
            #   "value": request.form["city"]
            #}
        ]}
            workExcecute= bizagi.executeWorkItemCase(process=process_id,case_id=session["case_id"],workitems=workitems["id"],data=data)
            print(workExcecute)
            return redirect('/ChoosePayment')
    print("dopo")
    #flash("something went wrong")
    return  render_template('compileForm.html',form=form,city=city)


@app.route('/ChoosePayment', methods=['GET', 'POST'])
def ChoosePayment():
    form = compileForm()
    if request.method == 'POST':
        print(request.form["payment"])
        workitems=bizagi.getWorkItemCase(process=process_id,case_id=session["case_id"],taskName="ChoosePayment")
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


@app.route('/check/<caseid>/<workitems>/<taskName>', methods=['GET', 'POST'])
def check(caseid,workitems,taskName):
    response=checkCorrectWorkItem(process_id,caseid,workitems,taskName)
    if response:
        session["case_id"]=caseid
        return redirect(url_for(taskName))
    else:
        flash("something went wrong")
        return redirect(url_for("home"))

@app.route('/getPayment', methods=['GET', 'POST'])
def getPayment():
    if random.uniform(0, 1)>0.25:
        return {"Payment": {"value":False}}
    else:
        return {"Payment": {"value":False}}

@app.route('/getAppointment', methods=['GET', 'POST'])
def getAppointment():
    hour=random.uniform(9, 19)
    
    tomorrow = datetime.datetime.now() + datetime.timedelta(days=1,hours=hour)
    print(tomorrow)
    if random.uniform(0, 1)>0.25:
        return {"Payment": {"value":tomorrow,"time":str(datetime.time())}}
    else:
        return {"Payment": {"value":tomorrow,"time":str(datetime.time())}}


def checkCorrectWorkItem(processid,case_id,ExecutableWorkItem,taskName):
   workitems= bizagi.getWorkItemCase(process=processid,case_id=case_id,taskName=taskName)
  
   if len(workitems)>0 and str(workitems["id"])==ExecutableWorkItem and workitems["taskName"]== taskName:
       return True
   return False