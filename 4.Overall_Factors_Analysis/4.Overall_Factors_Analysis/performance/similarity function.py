from scipy.stats import pearsonr
import numpy as np

def compare_sim(sim1, sim2):
    # A function to compare the similarities use pearsonr distance.
    com1 = sim1
    com2 = sim2
    score = pearsonr(com1, com2)[0]
    return score

def cosine_simil(vec1, vec2):
    # This funciton is to calculate the cosine similarity.
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    va1 = np.linalg.norm(vec1)
    va2 = np.linalg.norm(vec2)
    similarity = vec1.dot(vec2) / (va1 * va2)
    return similarity