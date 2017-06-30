from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix
import pandas as pd
import pickle



df = pd.read_csv("dataframe.csv")
X = df[df.columns.drop(["Gesture"])]
Y = df["Gesture"]


scaler = StandardScaler()
scaler.fit(X)

X_train = scaler.transform(X)


#classificador com 3 camadas de 30 neurons cada
mlp = MLPClassifier(hidden_layer_sizes=(30,30,30))
#treinamento
mlp.fit(X_train,Y)





with open('mlp.pickle','wb') as f:
    pickle.dump(mlp, f)

with open('scaler.pickle','wb') as k:
    pickle.dump(scaler,k)


try:
    pickle_in = open('mlp.pickle', 'rb')
    mlp = pickle.load(pickle_in)
    print("Loaded saved mlp!")
except:
    print("Trained model not found at mlp.pickle!")


try:
    scaler_in = open('scaler.pickle', 'rb')
    sc = pickle.load(scaler_in)
    print("Loaded saved scaler!")
except:
    print("Scaler model not found at scaler.pickle!")