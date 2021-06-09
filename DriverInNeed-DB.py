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

tripsql="""
CREATE TABLE trip(
TripId INTEGER PRIMARY KEY AUTOINCREMENT,
ClientId NUMBER NOT NULL,
DriverId NUMBER NOT NULL,
ServiceId NUMBER NOT NULL,
FOREIGN KEY (ClientId) REFERENCES client (ClientId),
FOREIGN KEY (DriverId) REFERENCES driver (DriverId),
FOREIGN KEY (ServiceId) REFERENCES service (ServiceId)

      
)
"""

servicesql="""
CREATE TABLE service(
ServiceId INTEGER PRIMARY KEY AUTOINCREMENT,
ServiceType TEXT NOT NULL,
Startdate INTEGER NOT NULL,
Enddate INTEGER NOT NULL,
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
cur.execute(tripsql)
cur.execute(servicesql)
cur.execute(adminsql)

print("the database has been created")
conn.commit()
conn.close()