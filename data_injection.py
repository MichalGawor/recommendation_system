import mysql.connector

def inject_data(data, user='root', database='restaurantwebsite'):
    cnx = mysql.connector.connect(user=user, database=database)
    cursor0 = cnx.cursor()
    cursor1 = cnx.cursor()
    cursor2 = cnx.cursor(prepared=True)
    
    query0 = ("DROP TABLE IF EXISTS top10")
    query1 = ("CREATE TABLE  top10(id varchar(50), first varchar(20), second varchar(20), third varchar(20), fourth varchar(20),"
             "fifth varchar(20), sixth varchar(20), seventh varchar(20), eighth varchar(20), nineth varchar(20), tenth varchar(20))")
    query2 = ("INSERT INTO top10(id, first, second, third, fourth, fifth, sixth, seventh, eighth, nineth, tenth)" 
              "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ")

    cursor0.execute(query0)
    cursor1.execute(query1)

    for tuple in data:
        helper = []
        helper.append(tuple[0])
        for elem in tuple[1]:
            helper.append(elem)
        print(helper)
        cursor2.execute(query2, helper)
    cnx.commit() 
    cursor0.close()
    cursor1.close()
    cursor2.close()

    cnx.close()