import os, re, email, email.policy, html, numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.pipeline import make_pipeline
def text_of(path):
    with open(path,'rb') as f: msg=email.message_from_bytes(f.read(), policy=email.policy.default)
    parts=[str(msg['subject'] or '')]
    for p in msg.walk():
        if p.get_content_maintype()=='text':
            try: t=p.get_content()
            except Exception: t=p.get_payload(decode=True).decode('latin-1','ignore') if p.get_payload(decode=True) else ''
            if p.get_content_subtype()=='html': t=html.unescape(re.sub(r'<[^>]+>',' ',t))
            parts.append(t)
    return '\n'.join(parts)
def norm(t):
    t=t.lower(); t=re.sub(r'(https?://|www\.)\S+',' URLTOKEN ',t); t=re.sub(r'\S+@\S+',' EMAILTOKEN ',t)
    t=re.sub(r'\d+(\.\d+)?',' NUMTOKEN ',t); return t
X,y=[],[]
for d,l in [('easy_ham',0),('easy_ham_2',0),('hard_ham',0),('spam',1),('spam_2',1)]:
    for fn in os.listdir('data/'+d):
        if fn=='cmds': continue
        X.append(norm(text_of(f'data/{d}/{fn}'))); y.append(l)
y=np.array(y); print('n',len(y),'spam',y.sum(),'ham',(y==0).sum())
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=0.2,stratify=y,random_state=42)
print('train',len(ytr),'test',len(yte),'test spam',yte.sum())
tok=r'(?u)\b[a-zA-Z][a-zA-Z]+\b'
def run(name,vec,clf):
    p=make_pipeline(vec,clf).fit(Xtr,ytr); pr=p.predict(Xte); pb=p.predict_proba(Xte)[:,1]
    tn,fp,fn,tp=confusion_matrix(yte,pr).ravel()
    cv=cross_val_score(make_pipeline(vec,clf),X,y,cv=StratifiedKFold(5,shuffle=True,random_state=42),scoring='accuracy')
    print(f'{name}: TP={tp} FN={fn} FP={fp} TN={tn} acc={accuracy_score(yte,pr):.4f} prec={precision_score(yte,pr):.4f} rec={recall_score(yte,pr):.4f} f1={f1_score(yte,pr):.4f} spec={tn/(tn+fp):.4f} auc={roc_auc_score(yte,pb):.4f} cv={cv.mean():.4f}±{cv.std():.4f} vocab={len(p[0].vocabulary_)}')
    return p
m=run('MNB counts',CountVectorizer(token_pattern=tok,stop_words='english',min_df=2),MultinomialNB(alpha=1.0))
run('BNB binary',CountVectorizer(token_pattern=tok,stop_words='english',min_df=2,binary=True),BernoulliNB(alpha=1.0))
run('MNB tfidf',TfidfVectorizer(token_pattern=tok,stop_words='english',min_df=2),MultinomialNB(alpha=0.1))
v=m[0]; nb=m[1]; lp=nb.feature_log_prob_[1]-nb.feature_log_prob_[0]; names=np.array(v.get_feature_names_out())
print('top spam',names[np.argsort(-lp)[:15]]); print('top ham',names[np.argsort(lp)[:15]])
# threshold tradeoff
pb=m.predict_proba(Xte)[:,1]
for th in [0.5,0.9,0.99]:
    pr=(pb>=th).astype(int); tn,fp,fn,tp=confusion_matrix(yte,pr).ravel(); print(th,'FP',fp,'FN',fn,'rec',round(tp/(tp+fn),4))
tr=np.array(ytr); 
for w in ['free','money','click','remove','linux']:
    has=np.array([bool(re.search(r'\b'+w+r'\b',t)) for t in Xtr])
    print(w, round(has[tr==1].mean(),3), round(has[tr==0].mean(),3))
print('prior',round(tr.mean(),3))
