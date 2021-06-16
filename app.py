from flask import Flask, request, jsonify
import json
from flask_cors import CORS,cross_origin
import sqlite3 as sql
import base64


app = Flask(__name__)

CORS(app)




@app.route('/addClient', methods=['POST'])
def addNewClient():

    if request.method=='POST':
        data = request.data
        my_json = data.decode('utf8')
        data1 = json.loads(my_json)

        ClientFname = data1['ClientFname']
        ClientLname = data1['ClientLname']
        ClientPhoneNo =data1['ClientPhoneNo']
        ClientNid = data1['ClientNid']
        ClientAddress = data1['ClientAddress']
        ClientEmail = data1['ClientEmail']
        ClientCarLicense =data1['ClientCarLicense']
        ClientPassword = data1['ClientPassword']


        conn = sql.connect("DriverInNeed")
        cur=conn.cursor()

        #
        # validation=("SELECT * FROM client WHERE  ClientPhoneNo=?")
        # checkValue=(data1['ClientPhoneNo'])
        # cur.execute(validation,checkValue )
        # valid=cur.fetchone()
        # print(valid)
        # return jsonify('')


        script=("INSERT INTO Client (pos,ClientFname,ClientLname,ClientPhoneNo,ClientNid,"
                "ClientAddress,ClientEmail ,CarlicenseNO,ClientPassword,ClientStatus)VALUES ('client',?,?,?,?,?,?,?,?,'vacant') ")
        val=(ClientFname, ClientLname, ClientPhoneNo,ClientNid,ClientAddress,ClientEmail,
             ClientCarLicense,ClientPassword)
        cur.execute(script, val)
        conn.commit()
        return jsonify('')

@app.route('/addDriver', methods=['POST'])
def addNewDiver():
    if request.method=='POST':
        data = request.data
        my_json = data.decode('utf8')
        print(my_json)
        data1 = json.loads(my_json)

        DriverFname=data1['DriverFname']
        DriverLname=data1['DriverLname']
        DriverEmail=data1['DriverEmail']
        DriverPassword=data1['DriverPassword']
        DriverAddress=data1['DriverAddress']
        DriverPhone=data1['DriverPhone']
        DriverNid = data1['DriverNid']
        DriverLicense = data1['DriverLicense']
        RadioOptions=data1['RadioOptions']


        conn = sql.connect("DriverInNeed")
        cur = conn.cursor()
        script = ("INSERT INTO driver (pos,DriverFname,DriverLname,"
                  "DriverPhoneNo,DriverNid,DriverEmail,DriverAddress,DriverLicenseNo"
                  ",DriverPassword,DriverService,DriverStatus)VALUES ('driver',?,?,?,?,?,?,?,?,?,'vacant') ")
        val=(DriverFname, DriverLname, DriverPhone,DriverNid,
             DriverEmail,DriverAddress,DriverLicense,DriverPassword,RadioOptions)
        cur.execute(script,val)
        conn.commit()

        return jsonify('')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        data = request.data
        my_json = data.decode('utf8')
        # print("printing json ==>",type(my_json))
        userInfo = json.loads(my_json)
        # print("printing userInfo ==>", userInfo)
        phone = userInfo['phonenumber']
        password = userInfo['password']

        conn = sql.connect("DriverInNeed")
        cur = conn.cursor()
        info2='None'
        cur.execute("SELECT pos,ClientFname, ClientLname, ClientPhoneNo, ClientNid, ClientAddress, ClientEmail, CarLicenseNO, ClientPassword,ClientStatus From client WHERE ClientPhoneNo=? AND ClientPassword=? UNION SELECT pos,DriverFname, DriverLname, DriverPhoneNo, DriverNid, DriverAddress, DriverEmail, DriverLicenseNo,DriverService,Fare From driver WHERE  DriverPhoneNo=? AND DriverPassword=? ",(phone,password,phone,password))
        # cur.execute(script)
        info = cur.fetchone()
        print(info)
        if info!=None:
            return jsonify(info)
        else:
            return jsonify(info2)


@app.route('/adminlogin', methods=['POST'])
def adminlogin():
    if request.method == 'POST':
        data = request.data
        my_json = data.decode('utf8')
        # print(my_json)
        userInfo = json.loads(my_json)

        phone = userInfo['phonenumber']
        password = userInfo['password']
        val=(phone,password)
        conn = sql.connect("DriverInNeed")
        cur2 = conn.cursor()

        script3 = ("SELECT * FROM admin WHERE  adminID=? AND adminPassword=?")
        cur2.execute(script3, val)
        info2 = cur2.fetchone()
        # print(info2[1])
        return jsonify(info2)
@app.route('/clientData', methods=['GET'])
def getclientdata():
    if request.method=='GET':
        conn = sql.connect("DriverInNeed")
        cur = conn.cursor()
        script=("SELECT ClientFname,ClientLname,ClientPhoneNo,ClientAddress,ClientEmail,ClientStatus FROM client")
        cur.execute(script)
        data=cur.fetchall()
        if data==None :
            return("nodata")
        else:
            return jsonify(data)


@app.route('/driverData', methods=['GET'])
def getdriverdata():
    if request.method=='GET':
        conn = sql.connect("DriverInNeed")
        cur = conn.cursor()
        script=("SELECT DriverFname,DriverLname,DriverPhoneNo,DriverAddress,DriverEmail,DriverNid,DriverLicenseNo,DriverService,DriverStatus FROM driver")
        cur.execute(script)
        data=cur.fetchall()
        if data==None :
            return("nodata")
        else:
            return jsonify(data)

@app.route('/addClientImage', methods=['GET','PUT'])
def addClientImage():
    conn = sql.connect("DriverInNeed")
    cur = conn.cursor()
    if request.method == 'PUT':
        data = request.data
        my_json = data.decode('utf8')
        userInfo = json.loads(my_json)
        phone = userInfo[1]
        image = userInfo[0]


        binImg=(base64.b64decode(image))
        val=(binImg,phone)
        script = ("UPDATE client SET ClientPhoto=? WHERE ClientPhoneNo=?")
        cur.execute(script, val)
        conn.commit()

        return jsonify('Updated')

@app.route('/addDriverImage', methods=['GET','PUT'])
def addDriverImage():
    conn = sql.connect("DriverInNeed")
    cur = conn.cursor()
    if request.method == 'PUT':
        data = request.data
        my_json = data.decode('utf8')
        userInfo = json.loads(my_json)
        phone = userInfo[1]
        image = userInfo[0]


        binImg=(base64.b64decode(image))
        val=(binImg,phone)
        script = ("UPDATE driver SET DriverPhoto=? WHERE DriverPhoneNo=?")
        cur.execute(script, val)
        conn.commit()

        return jsonify('Updated')

@app.route('/displayClientImage/<int:phn>', methods=['GET'])
def displayClientImage(phn):
    conn = sql.connect("DriverInNeed")
    cur = conn.cursor()
    if request.method == 'GET':
        cur.execute("Select ClientPhoto  FROM client where ClientPhoneNo=? ", (phn,))
        img=cur.fetchone()
        # print(type(img[0]))
        data_base64 = base64.b64encode(img[0])
        base64_string = data_base64.decode('utf-8')



    return jsonify(base64_string)


@app.route('/displayDriverImage/<int:phn>', methods=['GET'])
def displayDriverImage(phn):
    conn = sql.connect("DriverInNeed")
    cur = conn.cursor()
    if request.method == 'GET':
        cur.execute("Select DriverPhoto  FROM driver where DriverPhoneNo=? ", (phn,))
        img=cur.fetchone()
        print(img[0])
        data_base64 = base64.b64encode(img[0])
        base64_string = data_base64.decode('utf-8')

        # print(base64_string)

    return jsonify(base64_string)


@app.route('/editClientAddress', methods=['PUT'])
def editClientAddress():
    if request.method=='PUT':
        data = request.data
        my_json = data.decode('utf8')
        userInfo = json.loads(my_json)
        phone = userInfo[1]
        address = userInfo[0]
        val=(address,phone)

        conn = sql.connect("DriverInNeed")
        cur = conn.cursor()


        script = ("UPDATE client SET ClientAddress=? WHERE ClientPhoneNo=?")
        cur.execute(script,val)
        conn.commit()

        return  jsonify('Updated')


@app.route('/editClientEmail', methods=['PUT'])
def editClientEmail():
    if request.method == 'PUT':
        data = request.data
        my_json = data.decode('utf8')
        userInfo = json.loads(my_json)
        phone = userInfo[1]
        email = userInfo[0]
        val = (email, phone)

        conn = sql.connect("DriverInNeed")
        cur = conn.cursor()

        script = ("UPDATE client SET ClientEmail=? WHERE ClientPhoneNo=?")
        cur.execute(script, val)
        conn.commit()

        return jsonify('Updated')

@app.route('/editClientPhone', methods=['PUT'])
def editClientPhone():
    if request.method == 'PUT':
        data = request.data
        my_json = data.decode('utf8')
        userInfo = json.loads(my_json)
        phone = userInfo[1]
        Upphone = userInfo[0]
        val = (Upphone, phone)

        conn = sql.connect("DriverInNeed")
        cur = conn.cursor()

        script = ("UPDATE client SET ClientPhoneNo=? WHERE ClientPhoneNo=?")
        cur.execute(script, val)
        conn.commit()

        return jsonify('Updated')


@app.route('/editClientLicense', methods=['PUT'])
def editClientlicense():
    if request.method == 'PUT':
        data = request.data
        my_json = data.decode('utf8')
        userInfo = json.loads(my_json)
        phone = userInfo[1]
        license = userInfo[0]
        val = (license, phone)

        conn = sql.connect("DriverInNeed")
        cur = conn.cursor()

        script = ("UPDATE client SET CarlicenseNO=? WHERE ClientPhoneNo=?")
        cur.execute(script, val)
        conn.commit()

        return jsonify('Updated')

@app.route('/getDailyDriver', methods=['GET'])
def getDailyDriver():
    if request.method == 'GET':
        conn = sql.connect("DriverInNeed")
        cur = conn.cursor()
        script=("SELECT Driverfname,DriverLname,DriverPhoneNo,DriverEmail,DriverLicenseNo,DriverService,DriverPhoto,Fare FROM driver WHERE (DriverService ='daily' AND DriverStatus='vacant')")
        cur.execute(script)
        data=cur.fetchall()
        mylist=[]
        for i in range(len(data)):
            list4 = list(data[i])
            data_base64 = base64.b64encode(list4[6])
            base64_string = data_base64.decode('utf-8')
            list4[6]=base64_string
            mylist.append(list4)
        print(mylist)
    return jsonify(mylist)

@app.route('/changeClientReqService', methods=['PUT'])
def changeClientReqService():
    if request.method == 'PUT':
        conn = sql.connect("DriverInNeed")
        cur = conn.cursor()
        data = request.data
        my_json = data.decode('utf8')
        userInfo = json.loads(my_json)
        servicetype=userInfo[0]
        phone=userInfo[1]
        val=(servicetype,phone)
        print(val)
        script=("UPDATE client SET ClientRequiredService=? WHERE ClientPhoneNo=?")
        cur.execute(script,val)
        conn.commit()
    return jsonify("updated")

@app.route('/getMonthlyDriver', methods=['GET'])
def getMonthlyDriver():
    if request.method == 'GET':

        conn = sql.connect("DriverInNeed")
        cur = conn.cursor()
        script=("SELECT Driverfname,DriverLname,DriverPhoneNo,DriverEmail,DriverLicenseNo,DriverService,DriverPhoto,Fare FROM driver WHERE (DriverService ='monthly' AND DriverStatus='vacant')")
        cur.execute(script)
        data=cur.fetchall()
        mylist = []

        for i in range(len(data)):
            list4 = list(data[i])

            data_base64 = base64.b64encode(list4[6])
            #
            base64_string = data_base64.decode('utf-8')

            list4[6] = base64_string
            mylist.append(list4)

        print(mylist)

    return jsonify(mylist)

@app.route('/updateDriverAddress',methods=['PUT'])
def updateDriverAddress():
    if request.method == 'PUT':
        data = request.data
        my_json = data.decode('utf8')
        userInfo = json.loads(my_json)
        phone = userInfo[1]
        address = userInfo[0]
        val = (address, phone)

        conn = sql.connect("DriverInNeed")
        cur = conn.cursor()

        script = ("UPDATE driver SET DriverAddress=? WHERE DriverPhoneNo=?")
        cur.execute(script, val)
        conn.commit()
        return jsonify('Updated')

@app.route('/updateDriverEmail',methods=['PUT'])
def updateDriverEmail():
    if request.method == 'PUT':
        data = request.data
        my_json = data.decode('utf8')
        userInfo = json.loads(my_json)
        phone = userInfo[1]
        email = userInfo[0]
        val = ( email, phone)

        conn = sql.connect("DriverInNeed")
        cur = conn.cursor()

        script = ("UPDATE driver SET DriverEmail=? WHERE DriverPhoneNo=?")
        cur.execute(script, val)
        conn.commit()
        return jsonify('Updated')

@app.route('/updateDriverPhone',methods=['PUT'])
def updateDriverPhone():
    if request.method == 'PUT':
        data = request.data
        my_json = data.decode('utf8')
        userInfo = json.loads(my_json)
        phone = userInfo[1]
        EditedPhone = userInfo[0]
        val = ( EditedPhone, phone)

        conn = sql.connect("DriverInNeed")
        cur = conn.cursor()

        script = ("UPDATE driver SET DriverPhoneNo=? WHERE DriverPhoneNo=?")
        cur.execute(script, val)
        conn.commit()
        return jsonify('Updated')

# @app.route('/getjob/<string:servicetype>',methods=['GET'])
# def getjob(servicetype):
#     if request.method == 'GET':
#         print(servicetype)
#         conn = sql.connect("DriverInNeed")
#         cur = conn.cursor()
#         cur.execute("SELECT ClientFname,ClientLname,ClientPhoneNo,ClientEmail,ClientPhoto,ClientAddress,CarlicenseNO FROM client WHERE (ClientStatus='vacant' AND ClientRequiredService=?) ", (servicetype,))
#         # cur.execute(script)
#         data = cur.fetchall()
#         mylist = []
#
#         for i in range(len(data)):
#             list4 = list(data[i])
#
#             data_base64 = base64.b64encode(list4[4])
#             #
#             base64_string = data_base64.decode('utf-8')
#
#             list4[4] = base64_string
#             mylist.append(list4)
#
#         print(mylist)
#
#     return jsonify(mylist)

@app.route('/getjob/<string:servicetype>',methods=['GET'])
def getjob(servicetype):
    if request.method == 'GET':
        print(type(servicetype))
        conn = sql.connect("DriverInNeed")
        cur = conn.cursor()
        cur.execute("SELECT ClientFname,ClientLname,ClientPhoneNo,ClientEmail,ClientPhoto,ClientAddress,CarlicenseNO FROM client WHERE (ClientStatus='vacant' AND ClientRequiredService=? AND ClientPhoneNo NOT IN ( SELECT CPhone FROM applied) )" , (servicetype,))
        # cur.execute(script)
        data = cur.fetchall()
        mylist = []

        for i in range(len(data)):
            list4 = list(data[i])

            data_base64 = base64.b64encode(list4[4])
            #
            base64_string = data_base64.decode('utf-8')

            list4[4] = base64_string
            mylist.append(list4)

        print(mylist)

    return jsonify(mylist)

@app.route('/deleteClient/<int:phn>',methods=['DELETE'])
def deleteClient(phn):
    if request.method == 'DELETE':


        conn = sql.connect("DriverInNeed")
        cur = conn.cursor()


        cur.execute("DELETE  FROM client where ClientPhoneNo=? ",(phn,))
        # data = cur.fetchall()
        conn.commit()
        return jsonify("updated")

@app.route('/deleteDriver/<int:phn>',methods=['DELETE'])
def deleteDriver(phn):
    if request.method == 'DELETE':


        conn = sql.connect("DriverInNeed")
        cur = conn.cursor()


        cur.execute("DELETE  FROM driver where DriverPhoneNo=? ",(phn,))

        conn.commit()
        return jsonify("updated")



@app.route('/driverDatabyPhn/<int:phn>', methods=['GET'])
def driverDatabyPhn(phn):

    if request.method == 'GET':
        conn = sql.connect("DriverInNeed")
        cur = conn.cursor()


        cur.execute("SELECT DriverFname,DriverLname,DriverAddress,DriverPhoneNo,DriverLicenseNo,DriverService,Fare  FROM driver WHERE DriverPhoneNo=? ", (phn,))
        conn.commit()
        data = cur.fetchone()

        return jsonify(data)
@app.route('/clientDatabyPhn/<int:phn>', methods=['GET'])
def clientDatabyPhn(phn):

    if request.method == 'GET':
        conn = sql.connect("DriverInNeed")
        cur = conn.cursor()


        cur.execute("SELECT ClientFname,ClientLname,ClientAddress,ClientPhoneNo,CarlicenseNO,ClientEmail FROM client WHERE ClientPhoneNo=? ", (phn,))
        conn.commit()
        data = cur.fetchone()

        return jsonify(data)


@app.route('/EnterServiceData', methods=['POST'])
def ServiceData():
    conn = sql.connect("DriverInNeed")
    cur = conn.cursor()
    if request.method == 'POST':

        data = request.data
        my_json = data.decode('utf8')
        # print(my_json)
        info = json.loads(my_json)
        print(info)
        service=info[0]
        startdate=info[1]
        enddate=info[2]
        fare= info[3]
        Cfname=info[4]
        Clname=info[5]
        Caddress=info[6]
        Cphone=info[7]
        Dfname=info[8]
        Dlname=info[9]
        Daddress=info[10]
        Dphone=info[11]
        Dlicense=info[12]
        ServiceStatus=info[13]
        val=(service, startdate,enddate,fare,Cfname,Clname,Caddress,Cphone,Dfname,Dlname,Daddress,Dphone,Dlicense,ServiceStatus)

        script = ("INSERT INTO service (ServiceType, Startdate,Enddate,Fare,CFname,CLname,CAddress,CPhone,DFname,DLname,DAddress,DPhone,DLicense,ServiceStatus) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)")
        cur.execute(script, val)
        conn.commit()
        info = cur.fetchone()

        return jsonify("Inserted")

@app.route('/servicedata', methods=['GET'])
def servicedata():

    if request.method == 'GET':
        conn = sql.connect("DriverInNeed")
        cur = conn.cursor()
        cur.execute("SELECT * FROM service ")
        # WHERE ServiceStatus='occupied'
        data=cur.fetchall()
        conn.commit()
        return jsonify(data)



@app.route('/deleteservicedata/<int:cp>', methods=['DELETE'])
def deleteservicedata(cp):
    if request.method == 'DELETE':
        print(cp)
        conn = sql.connect("DriverInNeed")
        cur = conn.cursor()
        cur.execute("DELETE  FROM service where CPhone=? ",(cp,))

        conn.commit()
        return jsonify("deleted")

# changing driver and client status

@app.route('/changeDriverStatus', methods=['PUT'])

def DriverStatus():


    if request.method == 'PUT':
        data = request.data
        my_json = data.decode('utf8')
        userInfo = json.loads(my_json)
        phone = userInfo[0]
        status=userInfo[1]
        val=(status,phone)


        conn = sql.connect("DriverInNeed")
        cur = conn.cursor()
        script=("UPDATE driver SET DriverStatus=? WHERE DriverPhoneNo=?")
        cur.execute(script, val)
        conn.commit()
        return jsonify("driver status changed")

@app.route('/changeClientStatus', methods=['PUT'])
def ClientStatus():

        if request.method == 'PUT':
            data = request.data
            my_json = data.decode('utf8')
            userInfo = json.loads(my_json)
            phone = userInfo[0]
            status = userInfo[1]
            val = (status, phone)
            print(val)
            conn = sql.connect("DriverInNeed")
            cur = conn.cursor()
            script = ("UPDATE client SET ClientStatus=? WHERE ClientPhoneNo=?")
            cur.execute(script, val)
            conn.commit()
            return jsonify("client status changed")


@app.route('/checkClientInService/<int:phn>', methods=['GET'])
def checkClientInService(phn):
    if request.method == 'GET':
        conn = sql.connect("DriverInNeed")
        cur = conn.cursor()
        cur.execute("SELECT  DFname, DLname, Startdate,Enddate,DPhone,Fare FROM service where CPhone=?", (phn,))
        count=cur.fetchone()

        conn.commit

        return jsonify(count)

@app.route('/checkDriverInService/<int:phn>', methods=['GET'])
def checkDriverInService(phn):
    if request.method == 'GET':
        conn = sql.connect("DriverInNeed")
        cur = conn.cursor()
        cur.execute("SELECT  CFname, CLname, Startdate,Enddate,CPhone,CAddress FROM service where DPhone=?", (phn,))
        count=cur.fetchone()

        conn.commit

        return jsonify(count)



@app.route('/setDriversFare', methods=['PUT'])
def setDriversFare():
    if request.method == 'PUT':
        conn = sql.connect("DriverInNeed")
        cur = conn.cursor()
        data = request.data
        my_json = data.decode('utf8')
        userInfo = json.loads(my_json)
        phone = userInfo[0]
        fare = userInfo[1]
        val = (fare,phone)
        script = ("UPDATE driver SET Fare=? WHERE DriverPhoneNo=?")
        cur.execute(script, val)
        conn.commit()
        return jsonify("Fare Updated")


@app.route('/getDriversFare/<int:phn>', methods=['GET'])
def getDriversFare(phn):
        if request.method == 'GET':
            conn = sql.connect("DriverInNeed")
            cur = conn.cursor()

            cur.execute("SELECT Fare FROM driver WHERE DriverPhoneNo=? ",(phn,))
            conn.commit()
            data = cur.fetchone()

            return jsonify(data)

@app.route('/ApplyForJob', methods=['POST'])
def ApplyForJob():
    if request.method == 'POST':
        conn = sql.connect("DriverInNeed")
        cur = conn.cursor()
        data = request.data
        my_json = data.decode('utf8')
        data1 = json.loads(my_json)
        print(data1)
        cphone=data1[0]
        dphone=data1[1]
        dfname=data1[2]
        dlname=data1[3]
        daddress=data1[4]
        fare=data1[5]
        service=data1[6]
        val=(cphone,dphone,dfname,dlname,daddress,fare,service)
        script=("INSERT into applied (CPhone,Dphone,DFname,DLname,DAddress,Fare,DriverService) VALUES (?,?,?,?,?,?,?) ")
        cur.execute(script,val)
        conn.commit()
        return jsonify("done")

@app.route('/LookForJobReq/<int:phn>', methods=['GET'])
def LookForJobReq(phn):
    if request.method == 'GET':
        conn = sql.connect("DriverInNeed")
        cur = conn.cursor()
        cur.execute("SELECT * FROM applied WHERE CPhone=? ", (phn,))
        conn.commit()
        data = cur.fetchall()

        return jsonify(data)
@app.route('/DeleteJobReq/<int:phn>', methods=['DELETE'])
def DeleteJobReq(phn):
    if request.method == 'DELETE':
        conn = sql.connect("DriverInNeed")
        cur = conn.cursor()
        cur.execute("DELETE FROM applied WHERE CPhone=? ", (phn,))
        conn.commit()


        return jsonify("deleted")


if __name__ == '__main__':
    app.run(debug=True)
