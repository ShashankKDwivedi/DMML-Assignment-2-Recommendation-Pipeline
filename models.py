from pathlib import Path
import json
import pickle
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class PopularityRecommender:
    def __init__(self, item_features):
        self.item_features = item_features.copy()
    def fit(self, train):
        self.scores = train.groupby('item_id').agg(popularity=('user_id','count'), avg_rating=('rating','mean')).reset_index()
        self.scores['score'] = self.scores['popularity'] * (self.scores['avg_rating'] / 5.0)
        return self
    def recommend(self, user_id, k=5, seen=None):
        seen = set() if seen is None else set(seen)
        s = self.scores[~self.scores.item_id.isin(seen)].sort_values(['score','popularity','avg_rating'], ascending=False)
        return s.item_id.head(k).tolist()

class ItemCFRecommender:
    def __init__(self):
        self.sim = None; self.item_ids = None; self.user_item = None
    def fit(self, train):
        self.user_item = train.pivot_table(index='user_id', columns='item_id', values='rating', aggfunc='mean', fill_value=0)
        self.item_ids = self.user_item.columns.tolist()
        self.sim = cosine_similarity(self.user_item.T)
        np.fill_diagonal(self.sim, 0)
        return self
    def recommend(self, user_id, k=5, seen=None):
        seen = set() if seen is None else set(seen)
        if user_id not in self.user_item.index:
            return [i for i in self.item_ids if i not in seen][:k]
        ratings = self.user_item.loc[user_id].values
        scores = ratings @ self.sim
        ranked = np.argsort(-scores)
        recs = [self.item_ids[i] for i in ranked if self.item_ids[i] not in seen]
        return recs[:k]

def save_model(model, path):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('wb') as f: pickle.dump(model, f)
