import math
import numpy as np


def precision_recall_ndcg_at_k(recs, relevant, k=5):
    recs = recs[:k]; relevant = set(relevant)
    hits = [1 if x in relevant else 0 for x in recs]
    precision = sum(hits) / k
    recall = sum(hits) / len(relevant) if relevant else 0.0
    dcg = sum(h / math.log2(i + 2) for i, h in enumerate(hits))
    ideal_hits = min(len(relevant), k)
    idcg = sum(1 / math.log2(i + 2) for i in range(ideal_hits))
    ndcg = dcg / idcg if idcg else 0.0
    return precision, recall, ndcg


def evaluate_model(model, train, test, all_items, k=5, item_metadata=None):
    train_seen = train.groupby('user_id')['item_id'].apply(set).to_dict()
    relevant = test[test.rating >= 4].groupby('user_id')['item_id'].apply(set).to_dict()
    users = sorted(set(relevant) & set(train_seen))
    rows=[]; recommended_all=set(); intra=[]
    category_map = {} if item_metadata is None else item_metadata.set_index('item_id')['category'].to_dict()
    for u in users:
        recs = model.recommend(u, k=k, seen=train_seen.get(u,set()))
        recommended_all.update(recs)
        p,r,n = precision_recall_ndcg_at_k(recs, relevant[u], k)
        rows.append((p,r,n))
        if len(recs)>1:
            if category_map:
                intra.append(len({category_map.get(x, 'UNKNOWN') for x in recs}) / len(recs))
            else:
                intra.append(len(set(recs)) / len(recs))
    arr=np.array(rows) if rows else np.zeros((1,3))
    coverage=len(recommended_all)/len(all_items)
    diversity=float(np.mean(intra)) if intra else 0.0
    return {'Precision@K': float(arr[:,0].mean()), 'Recall@K': float(arr[:,1].mean()), 'NDCG@K': float(arr[:,2].mean()), 'Coverage': float(coverage), 'Diversity': diversity, 'Users evaluated': len(users)}
