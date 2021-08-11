# -*- coding: utf-8 -*-
"""Targil4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EtaTtSZuXo2EC83atKRqkGJ4v6-EL1Dh

In this homework, we will learn about SKLEARN and a little about how Python deals with files (using Dataframes) and arrays (numpy) and its graphing library, matplot.
"""

import numpy as np
import pandas as pd
url = 'https://github.com/rosenfa/nn/blob/master/pima-indians-diabetes.csv?raw=true'
df=pd.read_csv(url,  header=0, error_bad_lines=False) 
X = np.asarray(df.drop('Outcome',1))
y = np.asarray(df['Outcome'])

"""Let's print the dataset so we can see what we got!"""



"""Now let's add libraries for learning"""

from sklearn import tree #For decision trees
from sklearn.model_selection import cross_val_score #For cross validation
import matplotlib.pyplot as plt #for plotting graphs
from sklearn import datasets #for datasets

clf = tree.DecisionTreeClassifier()
clf.max_depth = 5
print("Decision Tree: ")
precision = cross_val_score(clf, X, y, scoring='precision', cv=10)
accuracy = cross_val_score(clf, X, y, scoring='accuracy', cv=10)
recall = cross_val_score(clf, X, y, scoring='recall', cv=10)
f1Score = cross_val_score(clf, X, y, scoring='f1', cv=10)

print("Average Precision of DT with depth ", clf.max_depth, " is: ", round(precision.mean(),3))
print("Average Accuracy of DT with depth ", clf.max_depth, " is: ", round(accuracy.mean(),3))
print("Average Recall of DT with depth ", clf.max_depth, " is: ", round(recall.mean(),3))
print("Average F1Score of DT with depth ", clf.max_depth, " is: ", round(f1Score.mean(),3))

"""We can do this for other datasets that are built-in to Sklearn:"""

iris = datasets.load_iris()
#mylist = []
#do loop
clf = tree.DecisionTreeClassifier()
clf.max_depth = 5
clf.criterion = 'entropy'
print("Decision Tree: ")
precision = cross_val_score(clf, iris.data, iris.target, scoring='precision_weighted', cv=10)
accuracy = cross_val_score(clf, iris.data, iris.target, scoring='accuracy', cv=10)
recall = cross_val_score(clf, iris.data, iris.target, scoring='recall_weighted', cv=10)
f1Score = cross_val_score(clf,iris.data, iris.target, scoring='f1_weighted', cv=10)

print("Average Precision of DT with depth ", clf.max_depth, " is: ", round(precision.mean(),3))
print("Average Accuracy of DT with depth ", clf.max_depth, " is: ", round(accuracy.mean(),3))
print("Average Recall of DT with depth ", clf.max_depth, " is: ", round(recall.mean(),3))
print("Average F1Score of DT with depth ", clf.max_depth, " is: ", round(f1Score.mean(),3))

def statsByDepth(depth, data, target):
  clf = tree.DecisionTreeClassifier()
  clf.max_depth = depth
  precision = round(cross_val_score(clf, data, target, scoring='precision_weighted', cv=10).mean(),3)
  accuracy = round(cross_val_score(clf, data, target, scoring='accuracy', cv=10).mean(),3)
  recall = round(cross_val_score(clf, data, target, scoring='recall_weighted', cv=10).mean(),3)
  f1Score = round(cross_val_score(clf, data, target, scoring='f1_weighted', cv=10).mean(),3)

  return [depth, precision, accuracy, recall, f1Score]

diabetes_stats = [statsByDepth(i, X, y) for i in range(1, 11)]

df_diabetes = pd.DataFrame(np.array(diabetes_stats), columns=["Depth","Percision", "Accuracy", "Recall", "F1-Score"])
df_diabetes

iris_stats = [statsByDepth(i, iris.data, iris.target) for i in range(1, 11)]

df_iris = pd.DataFrame(np.array(iris_stats), columns=["Depth","Percision", "Accuracy", "Recall", "F1-Score"])
df_iris



"""A confusion matrix for the data..."""

from sklearn.metrics import plot_confusion_matrix
class_names = iris.target_names
clf.max_depth = 2
clf = clf.fit(iris.data, iris.target)
titles_options = [("Confusion matrix")]

disp = plot_confusion_matrix(clf, iris.data, iris.target,
                              display_labels=class_names,
                              cmap=plt.cm.Blues)
disp.ax_.set_title(title)

print(title)
print(disp.confusion_matrix)

plt.show()

"""Hint for how to plot the results:"""

depths = range(1,11)
diabetes_stats = [statsByDepth(i, X, y) for i in depths]
precisions = [diabetes_stats[i][1] for i in range(10)]
accuracies = [diabetes_stats[i][2] for i in range(10)]
recalls = [diabetes_stats[i][3] for i in range(10)]
f1Scores = [diabetes_stats[i][4] for i in range(10)]
plt.plot(depths, precisions, label="precisions")
plt.plot(depths, accuracies, label="accuracies")
plt.plot(depths, recalls, label="recalls")
plt.plot(depths, f1Scores, label="f1-Scores")
plt.legend(loc="upper right")
plt.xlabel("Tree's Depth")
plt.ylabel("Stats")
plt.show()



depths = range(1,11)
iris_stats = [statsByDepth(i, iris.data, iris.target) for i in depths]
precisions = [iris_stats[i][1] for i in range(10)]
accuracies = [iris_stats[i][2] for i in range(10)]
recalls = [iris_stats[i][3] for i in range(10)]
f1Scores = [iris_stats[i][4] for i in range(10)]
plt.plot(depths, precisions, label="precisions")
plt.plot(depths, accuracies, label="accuracies")
plt.plot(depths, recalls, label="recalls")
plt.plot(depths, f1Scores, label="f1-Scores")
plt.legend(loc="best")
plt.xlabel("Tree's Depth")
plt.ylabel("Stats")
plt.show()

wine = datasets.load_wine()
depths = range(1,11)
wine_stats = [statsByDepth(i, wine.data, wine.target) for i in depths]
precisions = [wine_stats[i][1] for i in range(10)]
accuracies = [wine_stats[i][2] for i in range(10)]
recalls = [wine_stats[i][3] for i in range(10)]
f1Scores = [wine_stats[i][4] for i in range(10)]
plt.plot(depths, precisions, label="precisions")
plt.plot(depths, accuracies, label="accuracies")
plt.plot(depths, recalls, label="recalls")
plt.plot(depths, f1Scores, label="f1-Scores")
plt.legend(loc="best")
plt.xlabel("Tree's Depth")
plt.ylabel("Stats")
plt.show()

digits = datasets.load_digits()
depths = range(1,11)
digits_stats = [statsByDepth(i, digits.data, digits.target) for i in depths]
precisions = [digits_stats[i][1] for i in range(10)]
accuracies = [digits_stats[i][2] for i in range(10)]
recalls = [digits_stats[i][3] for i in range(10)]
f1Scores = [wine_stats[i][4] for i in range(10)]
plt.plot(depths, precisions, label="precisions")
plt.plot(depths, accuracies, label="accuracies")
plt.plot(depths, recalls, label="recalls")
plt.plot(depths, f1Scores, label="f1-Scores")
plt.legend(loc="best")
plt.xlabel("Tree's Depth")
plt.ylabel("Stats")
plt.show()

def bestAccuracyByDepth(depths, data, target):
  bestAcc = 0
  bestDepth = 0
  for i in depths:
    clf = tree.DecisionTreeClassifier()
    clf.max_depth = i
    accuracy = round(cross_val_score(clf, data, target, scoring='accuracy', cv=10).mean(),3)
    if accuracy > bestAcc:
      bestAcc = accuracy
      bestDepth = i

  return bestDepth, bestAcc

db_row = ["Diabetes", *bestAccuracyByDepth(range(1,11), X, y)]
ir_row = ["Iris", *bestAccuracyByDepth(range(1,11), iris.data, iris.target)]
wine_row = ["Wine", *bestAccuracyByDepth(range(1,11), wine.data, wine.target)]
dg_row = ["Digits", *bestAccuracyByDepth(range(1,11), digits.data, digits.target)]
df = pd.DataFrame([db_row, ir_row, wine_row, dg_row], columns=["Data-Set","Depth", "Best Accuracy"])
df