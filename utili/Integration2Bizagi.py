import requests


class Integration2Bizagi:
    baseURL=""
    authanticationCode=""
    endpopints={"login":"/oauth2/server/token",
    "getProcessByname":"/odata/data/processes?$filter=name eq ",
    "startcaseprocess":"/odata/data/processes(Insert_Process)/start",
    "getWorkItems": "/odata/data/processes(Insert_Process)/cases(insert_case)/workitems",
    "executeWorkItem":"/odata/data/processes(Insert_Process)/cases(insert_case)/workitems(insert_work)/next",
    "getCase":"/odata/data/cases(insert_case)",
    "excecuteQuery": "/odata/data/queries(insert_query)/executeQuery",#ffd50f9f-f997-4a7b-b092-f7a947e8e914
    "getEntities": "/odata/data/entities(insert_idEntities)/values"} #5860f4c5-7adc-47aa-9e22-bbe01e2f1186
    headers={"Authorization":"Bearer 6959074c976924d1ce8455899160193892f5be16",
"Content-type":'application/json'}

    def __init__(self,localhost="none",outhCodeBase64="None"):
        self.baseURL=localhost
        self.__getAuthCode(outhCodeBase64)
    
    def __getAuthCode(self,base64=""):
        my_headers = {"Content-type":"application/x-www-form-urlencoded",
"Authorization":"Basic "+base64}
        response = requests.post(self.baseURL+self.endpopints["login"], headers=my_headers,data = "grant_type=client_credentials&scope=api")
        print(response.json())
        self.headers["Authorization"]="Bearer "+response.json()['access_token']
        print(self.headers)

    def getProcessbyName(self, name=""):
        response = requests.post(self.baseURL+self.endpopints["getProcessByname"]+name, headers=self.headers)
        if len(response.json()["value"])>0:
            return response.json()["value"][0]["id"] 
        else:
            return []
    
    def startNewCaseProcess(self,process=0, data={"startParameters": []}):
         response = requests.post(self.baseURL+self.endpopints["startcaseprocess"].replace("Insert_Process",process), headers=self.headers,data=str(data))
         print(response)
         return response.json()
    
    def getWorkItemCase(self, process="0",case_id="0",taskName=""):

        response = requests.get(self.baseURL+self.endpopints["getWorkItems"].replace("Insert_Process",process).replace("insert_case",str(case_id)), headers=self.headers)
        print(response.json())
        if len(response.json()["value"])>0:
            for task in response.json()["value"]:
                print(task["taskName"])
                if  task["taskName"] == taskName:
                    return task
            return []
        else:
            return []
    
    def executeWorkItemCase(self, process="0",case_id="0",workitems="0",data={"startParameters": []}):

        response = requests.get(self.baseURL+self.endpopints["executeWorkItem"].replace("Insert_Process",process).replace("insert_case",str(case_id)).replace("insert_work",str(workitems))
        , headers=self.headers,data=str(data))
        print(response)
        return response.json()
    

    def excecuteQuery(self,queryid="",data={"startParameters": []}):
        response=requests.post(self.baseURL+self.endpopints["excecuteQuery"].replace("insert_query",queryid),headers=self.headers,data=str(data))
        return response.json()["value"]
    
    def getEntities(self,entitiesId):
        response=requests.post(self.baseURL+self.endpopints["getEntities"].replace("insert_idEntities",entitiesId),headers=self.headers)
        return response.json()["value"]
    
    def getcase(self,caseid):
        response=requests.post(self.baseURL+self.endpopints["getCase"].replace("insert_case",str(caseid)),headers=self.headers)
        return response.json()
    