from app.forms.makePaymentForm import makePaymentForm
from app import app,bizagi,process_id,city

from flask import render_template, flash, redirect, session,request,url_for

from app.forms.intialData import InitialData
from app.forms.compileForm import compileForm
from utili.globalVariable import payments, queries


import random
import datetime
import string    
import json

idinsurance="insuranceId"
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def home():
    form = InitialData()
    if request.method == "GET" and not idinsurance  in session :
        print("cosa")
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
            return render_template('listOfRequest.html',cases=[], info=[])
        else:
            cases={}
            for i in response:
                temp=bizagi.getcase(i["id"])
                print(temp)
                if "parameters" in temp:
                    cases[i["id"]]=temp["parameters"]
            return render_template('listOfRequest.html',cases=response, info=cases)
    return render_template('home.html',form=form,len=len(response))

@app.route('/exit', methods=['GET', 'POST'])
def exit():
    session.clear()
    form = InitialData()
    return redirect('/')

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
            ,            {
               "xpath":"Request.PatientInfo.City",
              "value": request.form["city"]
            }
        ]}
            workExcecute= bizagi.executeWorkItemCase(process=process_id,case_id=session["case_id"],workitems=workitems["id"],data=data)
            print(workExcecute)
            return redirect('/index')
        else:
            flash("something went wrong")
            return redirect('/index')
            
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
        if len(workitems)>0 and workitems["taskName"] == "ChoosePayment" :
            data = {"startParameters":[
            {
                "xpath":"Request.Payment",
                "value": request.form["payment"]
            }
        ]}
            workExcecute= bizagi.executeWorkItemCase(process=process_id,case_id=session["case_id"],workitems=workitems["id"],data=data)
            print(workExcecute)
            if request.form["payment"]==payments[1]:
                return redirect(url_for("MakePayment"))
            else:
                return redirect('/end')
    print(payments)
    return  render_template('choosePayment.html',payments=payments)


@app.route('/MakePayment', methods=['GET', 'POST'])
def MakePayment():
    form=makePaymentForm()
    if request.method == 'POST':
        workitems=bizagi.getWorkItemCase(process=process_id,case_id=session["case_id"],taskName="MakePayment")
        print(workitems)
        if len(workitems)>0 and workitems["taskName"] == "MakePayment" and form.validate_on_submit():
            print("trovato")
            S = 10  # number of characters in the string.  
            # call random.choices() string module to find the string in Uppercase + numeric data.  
            ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))    
            data = {"startParameters":[
            {
               "xpath":"Request.PaymentNumber",
              "value": ran
            }
            ]}
            workExcecute= bizagi.executeWorkItemCase(process=process_id,case_id=session["case_id"],workitems=workitems["id"],data=data)
            print(workExcecute)
            return redirect("/")
        else:
            return redirect("/")
    amount=""
    if "amount" in session:
        amount=session["amount"]
    return render_template('makePayment.html',form=form, amount=amount)

@app.route('/end', methods=['GET', 'POST'])
def end():
    return "congratulation"


@app.route('/check/<caseid>/<workitems>/<taskName>/<info>', methods=['GET', 'POST'])
def check(caseid,workitems,taskName,info):
    print("ecco le tue info")
    x=info
    x=x.replace("'",'"')
    x=x.replace("None",'"n"')
    x=x.replace("False",'"False"')
    x=x.replace("True",'"True"')
    y=json.loads(x)
    response=checkCorrectWorkItem(process_id,caseid,workitems,taskName)
    if response:
        session["case_id"]=caseid
        session["amount"]=y[0]["value"]
        return redirect(url_for(taskName))
    else:
        flash("something went wrong")
        return redirect(url_for("home"))
  


@app.route('/getPayment', methods=['GET', 'POST'])
def getPayment():
    if random.uniform(0, 1)>0.25:
        return {"Payment": {"value":True}}
    else:
        return {"Payment": {"value":False}}

@app.route('/getPayment/<PaymentNumber>', methods=['GET', 'POST'])
def getPayment2(PaymentNumber):
    print(PaymentNumber)
    if random.uniform(0, 1)>0.0:
        return {"Payment": {"value":True}}
    else:
        return {"Payment": {"value":False}}

@app.route('/getAppointment', methods=['GET', 'POST'])
def getAppointment():
    hospitals=bizagi.getEntities("cf62c824-07b0-462c-a58e-eb4e344dfd8d")
    hospital=random.uniform(0, len(hospitals))
    hospital=int(hospital)
    hour=random.uniform(8, 20)
    
    tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
    print(int(hour))
    tomorrow=tomorrow.replace(hour=int(hour))
    tomorrow=tomorrow.strftime("%m/%d/%Y %H:%M")
    return {"Appointment": {"date": tomorrow,"hospital":hospitals[hospital]["parameters"][0]["value"]}}
   


def checkCorrectWorkItem(processid,case_id,ExecutableWorkItem,taskName):
   workitems= bizagi.getWorkItemCase(process=processid,case_id=case_id,taskName=taskName)
  
   if len(workitems)>0 and str(workitems["id"])==ExecutableWorkItem and workitems["taskName"]== taskName:
       return True
   return False

