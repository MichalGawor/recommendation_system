import numpy as np
from data_extraction import produce_data
from data_injection import inject_data

from sklearn.metrics.pairwise import pairwise_distances
    
def predict_userwise(ratings, usr_sim):
    '''
    :param rating: matrix of ratings of n users for m items
    :param usr_sim: similarity matrix containing pairwise distances
                   between users calculated using cosine as metric function
    return: matrix of scores which restaurant will the user like the most, higher score it is more likely
    '''
    ret = []
    for i in range(0, 4):
        mean_usr_rating = ratings[i].mean(axis=1)
        rating_normalization = (ratings[i] - mean_usr_rating[:, np.newaxis])
        ret.append(mean_usr_rating[:, np.newaxis] + usr_sim[i].dot(rating_normalization) / np.array([np.abs(usr_sim[i]).sum(axis=1)]).T)
    return ret
        
def predict_itemwise(ratings, item_sim):
    '''
    :param ratings: matrix of ratings of n users for m items
    :param item_sim: similarity matrix containing paurwise distances
                    between users calculated using cosine as metric function
    :return: matrix of scores which restaurant will the user like the most, higher score it is more likely
    '''
    ret = []
    for i in range(0, 4):
        ret.append(ratings[i].dot(item_sim[i]) / np.array([np.abs(item_sim[i]).sum(axis=1)]))
    return ret

def predict(ratings, usr_sim, item_sim, alpha=0.8):
    '''
    :param rating: list of matrices of ratings of n users for m items
    :param usr_sim: similarity matrix containing pairwise distances
                   between users calculated using cosine as metric function
    :param item_sim: similarity matrix containing paurwise distances
                    between users calculated using cosine as metric function
    :param usr_factor: model weight for user and item filtering
    :param item_factor: model weight for user and item filtering
    :return: matrix of scores which restaurant will the user like the most, higher score it is more likely
    '''
    userwise = predict_userwise(ratings, usr_sim)
    itemwise = predict_itemwise(ratings, item_sim)
    ret = np.zeros(userwise[0].shape)
    for i in range(0, 4):
        ret += alpha * userwise[i] + (1 - alpha) * itemwise[i]
    return ret

def sim_matrix(rating_matrices, type='usr'):
    '''
    :param rating_matrices: list of matrices [usr] x [item] containing reviews
    :param type: type of similarity to be obtained, possible 'usr' and 'item'
    :return: list of similarity matrices
    '''
    if type == 'usr':
        usr_sim = []
        for review_matrix in rating_matrices:
            usr_sim.append(pairwise_distances(review_matrix, metric = 'cosine'))
        return usr_sim
    if type == 'item':
        item_sim = []
        for review_matrix in rating_matrices:
            item_sim.append(pairwise_distances(review_matrix.T, metric = 'cosine'))
        return item_sim
    else:
        raise ValueError("Wrong type for simimalirty matrix. Should be 'usr' or 'item'")
    
def map_id(predictions, users, restaurants):
    '''
    This function maps restaurant proposition to the user id
    :param predictions: matrix of predictions n_usrx10
    :param users: list in format (usr_id, usr_nb)
    :param restaurants: list in format (rest_id, rest_nb)
    :return: list of tuples (usr_id, rest_id[]) where rest_id[] is 10 long and 
    consist of predicted restaurants id for the user
    '''
    ret = []
    for i in range (0, predictions.shape[0]):
        rest_id = []
        for j in range(0, predictions.shape[1]):
            rest_id.append(restaurants[predictions[i, 9-j]][0])
        ret.append((users[i][0], rest_id))
    return ret
        
if __name__ == "__main__":
    (review_list, users, restaurants) = produce_data()
    pred = predict(review_list, sim_matrix(review_list, type='usr'), sim_matrix(review_list, type='item'))
    inject_data(map_id(pred.argsort()[:, -10:], users, restaurants))
    print("Successfully executed")
    




