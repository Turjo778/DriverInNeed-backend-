import sqlite3

conn=sqlite3.connect("DriverInNeed")
cur=conn.cursor()


clientsql="""
CREATE TABLE client(
ClientId INTEGER PRIMARY KEY AUTOINCREMENT,
pos TEXT,
ClientFname TEXT NOT NULL ,
ClientLname TEXT NOT NULL ,
ClientPhoneNo NUMBER NOT NULL ,
ClientNid  NUMBER NOT NULL ,
ClientAddress TEXT NOT NULL ,
ClientEmail TEXT NOT NULL ,
CarlicenseNO TEXT NOT NULL ,
ClientPassword TEXT NOT NULL,  
ClientRequiredService TEXT,
ClientDestinationLocation TEXT ,
ClientPhoto BLOB,
ClientStatus TEXT


)
"""


driversql="""
CREATE TABLE driver(
DriverId INTEGER PRIMARY KEY AUTOINCREMENT,
pos TEXT,
DriverFname TEXT NOT NULL,
DriverLname TEXT NOT NULL,
DriverPhoneNo NUMBER NOT NULL,
DriverNid NUMBER NOT NULL,
DriverEmail NUMBER NOT NULL,
DriverAddress TEXT NOT NULL,
DriverLicenseNo TEXT NOT NULL,
DriverPassword TEXT NOT NULL,
DriverService TEXT NOT NULL,
DriverPhoto BLOB,
Fare NUMBER,
DriverStatus TEXT


)
"""

applysql="""
CREATE TABLE applied(
ApplicationId INTEGER PRIMARY KEY AUTOINCREMENT,
CPhone NUMBER NOT NULL,
Dphone NUMBER NOT NULL,
DFname TEXT NOT NULL,
DLname TEXT NOT NULL,
DAddress TEXT NOT NULL,
Fare NUMBER,
DriverService TEXT



      
)
"""

servicesql="""
CREATE TABLE service(
ServiceId INTEGER PRIMARY KEY AUTOINCREMENT,
ServiceType TEXT NOT NULL,
Startdate INTEGER NOT NULL,
Enddate INTEGER,
Fare NUMBER ,
CFname TEXT NOT NULL,
CLname TEXT NOT NULL,
CAddress TEXT NOT NULL,
CPhone NUMBER NOT NULL,
DFname TEXT NOT NULL,
DLname TEXT NOT NULL,
DAddress TEXT NOT NULL,
DPhone NUMBER NOT NULL,
DLicense TEXT NOT NULL,
ServiceStatus TEXT

)

"""
adminsql="""
CREATE TABLE admin(
adminID INTEGER PRIMARY KEY AUTOINCREMENT,
pos TEXT,
adminName TEXT NOT NULL,
adminPassword TEXT NOT NULL

)
"""


cur.execute(clientsql)
cur.execute(driversql)
cur.execute(applysql)
cur.execute(servicesql)
cur.execute(adminsql)

print("the database has been created")
conn.commit()
conn.close()