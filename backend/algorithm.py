# The following code contains a preliminary version of a novel Shelling point-based consensus
# ... algorithm. For more information about the algorithm, please see the attached paper to the
# ... website.
#
#
# Author: Conner Delahanty, 2020
# Copyright pending
#

import numpy as np

''' Takes a matrix of votes (P) and returns the true distribution '''
def get_true_distribution(P):
    P = np.asarray(P)
    # Compute first mean weight
    w_bar_1 = np.mean(P, axis=0)
    # Compute each person's accuracy (L2 norm)
    acc_1 = np.sum(np.power(P - w_bar_1, 2.), axis =  1)
    # Normalize by inverse of L2 norm (to get measure of accuracy)
    acc_1_normed = (1. / acc_1) / (1. / acc_1).sum()
    # Apply this new weighting (accuracy) to the initial predictions
    w_bar_2 = np.matmul(acc_1_normed, P)
    w_bar_2 /= w_bar_2.sum()
    return w_bar_2

'''
Takes a true distribution, a voting matrix, and a 'harshness' parameter
and punishes users based off their guesses. In this case, one's final score
is being weighted by their accuracy (whereas previously, one's accuracy
influences their votes' weights)
'''
def punish(true_dist, P, harshness=0.1):
    # Compute a revised L2 Norm that measures accuracy
    acc = np.sum(np.power(P - true_dist, 2.), axis = 1)
    # Normalize to create final accuracy measure
    acc_normed = (1 / acc) / (1 / acc).sum()
    # Weight the final result by the square of the accuracy
    # measure (squared to reduce stark differences)
    result = true_dist * np.power(acc_normed, harshness)
    result_normed = result / result.sum()
    return(result_normed)

''' Performs the algorithm on a voting matrix, P. '''
def algorithm(P, harshness = 0.5):
    true = get_true_distribution(P)
    punished = punish(true, P, harshness)
    return punished.tolist()

'''
This is a convenience adapter. It takes an array of the voters, along with a json
version of each voters votes. These are then converted to the P matrix for the
above methods.
Input:
[User1, User2,  ...], {User1: {User1: 10, User2: 20 ...}, User2: {User1: 20, User2: 40 ...}, ... }
Output:
[[10, 20, ...], [20, 40, ...], ...]
'''
def json_to_voting_matrix(voters, json):
    P = np.zeros((len(voters), len(voters)))
    for v1 in range(len(voters)):
        for v2 in range(len(voters)):
            P[v1, v2] = json[voters[v1].__str__()][voters[v2].__str__()]
    return P


