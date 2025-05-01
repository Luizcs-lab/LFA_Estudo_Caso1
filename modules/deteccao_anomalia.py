# Arquivo: processamento/anomalias.py
from sklearn.ensemble import IsolationForest

def detectar_anomalias(df):
    clf = IsolationForest(contamination=0.05)
    valores = df[['preco', 'quantidade']].values
    preds = clf.fit_predict(valores)
    df['anomalia'] = preds
    return df[df['anomalia'] == -1]
