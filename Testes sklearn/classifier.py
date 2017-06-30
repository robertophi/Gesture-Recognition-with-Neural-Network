from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix
import pandas as pd
import pickle, random
import matplotlib.pyplot as plt
import seaborn as sn






df = pd.read_csv("dataframe.csv")
X = df[df.columns.drop(["Gesture"])]
print(X.columns)
Y = df["Gesture"]
X_train, X_test, Y_train, Y_test = train_test_split(X, Y)




scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)


mlp = MLPClassifier(hidden_layer_sizes=(30,30,30), max_iter=2000)

mlp.fit(X_train,Y_train)



predictions = mlp.predict(X_test)

print(classification_report(Y_test,predictions))
print(confusion_matrix(Y_test,predictions))

cm=confusion_matrix(Y_test,predictions)

      
df_cm = pd.DataFrame(cm, range(6),
                  range(6))
#plt.figure(figsize = (10,7))
sn.set(font_scale=1.4)#for label size
sn.heatmap(df_cm, annot=True,annot_kws={"size": 16})# font size
plt.show()
plt.savefig("test.png")
