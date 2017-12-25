import mysql.connector
import numpy as np

def produce_data(user='root', database='restaurantwebsite'):
    '''
    TODO
    '''
    try:
        SQL_connection = mysql.connector.connect(user=user, database=database)
        restaurants_cursor = SQL_connection.cursor()
        users_cursor = SQL_connection.cursor()
        reviews_cursor = SQL_connection.cursor()

        get_restaurants_query = ("SELECT id FROM restaurant ORDER BY id")
        get_users_query = ("SELECT id FROM user ORDER BY id")
        get_reviews_query = ("SELECT pricing, speed, presentation, quality, user_id, restaurant_id FROM review ORDER BY user_id ")

        restaurants = []
        users = []
        reviews = []

        restaurants_cursor.execute(get_restaurants_query)
        i=0
        for id in restaurants_cursor:
            restaurants.append((id[0], i))
            i+=1
        
        i=0
        users_cursor.execute(get_users_query)   
        for id in users_cursor:
            users.append((id[0], i))
            i+=1
          
        reviews_cursor.execute(get_reviews_query)
        for (pricing, speed, presentation, quality, user_id, restaurant_id) in reviews_cursor:
            reviews.append((pricing, speed, presentation, quality, user_id, restaurant_id))
 
        pricing_matrix = np.zeros((len(users), len(restaurants)))
        speed_matrix = np.zeros((len(users), len(restaurants)))
        presentation_matrix = np.zeros((len(users), len(restaurants)))
        quality_matrix = np.zeros((len(users), len(restaurants)))

        for review in reviews:
            user_index=-1
            for user in users:
                if(review[4]==user[0]):
                    user_index=user[1]
            rest_index=-1
            for restaurant in restaurants:
                if(review[5]==restaurant[0]):
                    rest_index=restaurant[1]
            if(user_index>=0 and rest_index>=0):
                pricing_matrix[user_index, rest_index] = review[0]
                speed_matrix[user_index, rest_index] = review[1]
                presentation_matrix[user_index, rest_index] = review[2]
                quality_matrix[user_index, rest_index] = review[3]      
        restaurants_cursor.close()
        users_cursor.close()
        reviews_cursor.close()
        SQL_connection.close()
        ret = []
        ret.append(pricing_matrix)
        ret.append(speed_matrix)
        ret.append(presentation_matrix)
        ret.append(quality_matrix)
        return (ret, users, restaurants)
    
    except mysql.connector.Error as error:
        print("Could not connect to the server: {}".format(error))

if __name__ == "__main__":
    print(produce_data())
    
    
    
