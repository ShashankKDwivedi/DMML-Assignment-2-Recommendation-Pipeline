from pathlib import Path
import numpy as np, pandas as pd

ROOT=Path(__file__).parent
rng=np.random.default_rng(2026)
raw=ROOT/'data/raw'; raw.mkdir(parents=True,exist_ok=True)
N_USERS,N_ITEMS=180,80
users=pd.DataFrame({'user_id':[f'U{i:04d}' for i in range(1,N_USERS+1)],'age':rng.integers(18,61,N_USERS),'country':rng.choice(['IN','US','UK','DE','AU'],N_USERS,p=[.55,.15,.1,.1,.1])})
categories=['Electronics','Books','Home','Sports','Beauty','Gaming','Fashion','Music']
items=pd.DataFrame({'item_id':[f'I{i:04d}' for i in range(1,N_ITEMS+1)],'category':rng.choice(categories,N_ITEMS),'item_title':[f'Item {i:04d}' for i in range(1,N_ITEMS+1)]})
rows=[]
start=pd.Timestamp('2025-01-01',tz='UTC')
for uid in users.user_id:
    n=int(rng.integers(18,45)); chosen=rng.choice(items.item_id,size=n,replace=False)
    preferred=rng.choice(categories,size=2,replace=False)
    for item in chosen:
        cat=items.loc[items.item_id==item,'category'].iloc[0]
        base=4.0 if cat in preferred else 3.0
        rating=float(np.clip(np.round(base+rng.normal(0,.8)),1,5))
        ts=start+pd.Timedelta(days=int(rng.integers(0,365)),hours=int(rng.integers(0,24)),minutes=int(rng.integers(0,60)))
        rows.append((uid,item,rating,ts))
interactions=pd.DataFrame(rows,columns=['user_id','item_id','rating','timestamp'])
# Inject a few deliberately invalid records so the validation/error dataset is demonstrated.
bad=pd.DataFrame([
    ('U0001','I0001',6.0,start+pd.Timedelta(days=10)),
    ('U0002','I0002',2.0,pd.NaT),
    ('U9999','I0003',4.0,start+pd.Timedelta(days=12)),
    ('U0003','I9999',5.0,start+pd.Timedelta(days=13)),
],columns=interactions.columns)
interactions=pd.concat([interactions,bad],ignore_index=True)
interactions=pd.concat([interactions,interactions.iloc[[0]]],ignore_index=True) # duplicate row
users.to_csv(raw/'users.csv',index=False); items.to_csv(raw/'items.csv',index=False); interactions.to_csv(raw/'interactions.csv',index=False)
print(f'Generated users={len(users)}, items={len(items)}, interactions={len(interactions)}')
