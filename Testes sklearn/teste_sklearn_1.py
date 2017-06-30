from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix

import pickle, random



cancer = load_breast_cancer()

X = cancer['data']
X = X[:,5:10]
y = cancer['target']
for i in range(len(y)):
    y[i] = y[i]+random.randint(0,1)
    print(i+random.randint(0,1))

#Apenas divide o espaço amostral em um subset para treinamento, e outro para teste
X_train, X_test, y_train, y_test = train_test_split(X, y)

scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)


#classificador com 3 camadas de 30 neurons cada
mlp = MLPClassifier(hidden_layer_sizes=(30,30,30))
#treinamento
mlp.fit(X_train,y_train)




predictions = mlp.predict(X_test)

print(confusion_matrix(y_test,predictions))
print(classification_report(y_test,predictions))
