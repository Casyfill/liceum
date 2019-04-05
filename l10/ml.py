import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances

def _closest_N(X1, X2, N):
    matrix = euclidean_distances(X1, X2)
    
    ix = pd.np.argsort(matrix, axis=0)[-1:-1-N:-1].T
    return ix


class KNN:
    X, y = None, None
    k = None
    
    def __init__(self, k=5, mode='mean'):
        assert mode in {'mean', 'mode', 'wmean'}
        self.k = k
    
    def fit(self, X, y):
        self.X = pd.np.array(X)
        self.y = pd.np.array(y)
        
    
    def predict(self, X):
        closest_index = _closest_N(self.X, X.values, self.k)
        values = self.y[closest_index].mean(1)  # feel free to add mode for classification, or weighted mean

#         if isinstance(X, pd.DataFrame):
#             return pd.Series(values, index=X.index)

        return values