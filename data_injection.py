def inject_data(user='root', database='restaurantwebsite'):
    '''
    TODO
    '''
    try:
        SQL_connection = mysql.connector.connect(user=user, database=database)
        droptable_cursor = SQL_connection.cursor()
        database_cursor = SQL_connection.cursor()
        
        #TODO
        droptable_query = "IF EXISTS ...TODO... \nBEGIN \nDROP TABLE ...tablename...\n END\n"
        #/TODO
        droptable_cursor.execute(droptable_query)
        
    except mysql.connector.Error as error:
        print("Could not connect to the server: {}".format(error))
        
def make_query(list):
    querries = []
    for tuple in list:
        #TODO TOTEST 
        querry = "INSERT INTO..."
        for elem in tuple[1]:
            querry += (',' + str(elem))
        querries.append(querry)
    return querries
        
    
        