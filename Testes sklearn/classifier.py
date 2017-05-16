from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix
import pandas as pd
import pickle, random



df = pd.read_csv("dataframe.csv")
X = df[df.columns.drop("Gesture")]
Y = df["Gesture"]
X_train, X_test, Y_train, Y_test = train_test_split(X, Y)




scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)



mlp = MLPClassifier(hidden_layer_sizes=(30,30,30))

mlp.fit(X_train,Y_train)


predictions = mlp.predict(X_test)

print(confusion_matrix(Y_test,predictions))
print(classification_report(Y_test,predictions))
