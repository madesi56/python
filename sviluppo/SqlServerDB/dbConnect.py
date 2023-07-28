import pyodbc



server = '192.168.68.108\sqlServer2017' 
database = 'GDS-CEM' 
username = 'sa' 
password = '@Admin2017' 
# ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.
#cnString = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password
cnString = "DSN=desma03;UID=sa; PWD=@Admin2017"
cnxn = pyodbc.connect(cnString)
cursor = cnxn.cursor()

cursor.execute("select plu,descr,wgru,walo,id from gds_cem.dbo.plu")
row = cursor.fetchall()
for r in row:
    print (str(r.id) , r.plu, r.descr, r.wgru)
    #print (str(r.id) , r.descrizione, str(r.notes).replace('\n', "@0A") )
