import mysql.connector

def connection_BDD1():
    mydb = mysql.connector.connect(
      host="127.0.0.1",
      user="root",
      password="passwordmysql",
      database="Voitures",
    )
    return mydb


def connection_BDD():
    mydb = mysql.connector.connect(
      host="idelont.fr",
      port="59435",
      user="rvoiture",
      password="!NtM$nQ52zT3",
      database="projet_irve",
      auth_plugin="mysql_native_password"
    )
    return mydb


#conn = mysql.connector.connect(host="idelont.fr",user="rvoiture",password="!NtM$nQ52zT3", database="projet_irve", port="59435", auth_plugin="mysql_native_password")

def get_voiture():
    mydb = connection_BDD()
    
    mycursor = mydb.cursor()
    
    mycursor.execute("SELECT * FROM Voiture;")
    
    myresult = mycursor.fetchall()
    
    liste_car = []
    for x in myresult:
      liste_car.append(x)
    
    return liste_car