import requests

class Integration2Bizagi:
    baseURL=""
    authanticationCode=""
    endpopints={"login":"/oauth2/server/token",
    "getProcessByname":"/odata/data/processes?$filter=name eq ",
    "startcaseprocess":"/odata/data/processes(Insert_Process)/start",
    "getWorkItems": "/odata/data/processes(Insert_Process)/cases(insert_case)/workitems",
    "executeWorkItem":"/odata/data/processes(Insert_Process)/cases(insert_case)/workitems(insert_work)/next"}
    headers={"Authorization":"Bearer 562644b82ed553e583877806c264d9137c149590",
"Content-type":'application/json'}

    def __init__(self,localhost="none",outhCodeBase64="None"):
        self.baseURL=localhost
        self.__getAuthCode(outhCodeBase64)
    
    def __getAuthCode(self,base64=""):
        my_headers = {"Content-type":"application/x-www-form-urlencoded",
"Authorization":"Basic "+base64}
        response = requests.post(self.baseURL+self.endpopints["login"], headers=my_headers,data = "grant_type=client_credentials&scope=api")
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
    
    def getWorkItemCase(self, process="0",case_id="0"):

        response = requests.get(self.baseURL+self.endpopints["getWorkItems"].replace("Insert_Process",process).replace("insert_case",str(case_id)), headers=self.headers)
        print(response)
        if len(response.json()["value"])>0:
            return response.json()["value"][0]
        else:
            return []
    
    def executeWorkItemCase(self, process="0",case_id="0",workitems="0",data={"startParameters": []}):

        response = requests.get(self.baseURL+self.endpopints["executeWorkItem"].replace("Insert_Process",process).replace("insert_case",str(case_id)).replace("insert_work",str(workitems))
        , headers=self.headers,data=str(data))
        print(response)
        return response.json()