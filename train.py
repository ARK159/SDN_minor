from datetime import datetime
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from imblearn.under_sampling import RandomUnderSampler
import joblib

def flow_training():

    flow_dataset = pd.read_csv('Dataset1.csv')

    # flow_dataset.iloc[:, 2] = flow_dataset.iloc[:, 2].str.replace('.', '')
    # flow_dataset.iloc[:, 3] = flow_dataset.iloc[:, 3].str.replace('.', '')
    # flow_dataset.iloc[:, 5] = flow_dataset.iloc[:, 5].str.replace('.', '')
    flow_datasetn=flow_dataset[['ip_proto','icmp_code','icmp_type','flow_duration_sec','flow_duration_nsec','idle_timeout','hard_timeout','flags','packet_count','byte_count','packet_count_per_second','packet_count_per_nsecond','byte_count_per_second','byte_count_per_nsecond','label']]
    # flow_datasetn.iloc[:, 0] = flow_datasetn.iloc[:, 0].str.replace('.', '')
    # flow_datasetn.iloc[:, 2] = flow_datasetn.iloc[:, 2].str.replace('.', '')
    X_flow = flow_datasetn.iloc[:, :-1].values
    X_flow = X_flow.astype('float64')
    rus = RandomUnderSampler(random_state=42)

    y_flow = flow_datasetn.iloc[:, -1].values

    X_flow_train, X_flow_test, y_flow_train, y_flow_test = train_test_split(X_flow, y_flow, test_size=0.25, random_state=0)

    X_train_rus, y_train_rus = rus.fit_resample(X_flow_train, y_flow_train)

    classifier = RandomForestClassifier(n_estimators=10, criterion="entropy", random_state=0)
    flow_model = classifier.fit(X_train_rus, y_train_rus)

    y_flow_pred = flow_model.predict(X_flow_test)

    print("------------------------------------------------------------------------------")

    print("confusion matrix")
    cm = confusion_matrix(y_flow_test, y_flow_pred)
    print(cm)

    acc = accuracy_score(y_flow_test, y_flow_pred)

    print("succes accuracy = {0:.2f} %".format(acc*100))
    fail = 1.0 - acc
    print("fail accuracy = {0:.2f} %".format(fail*100))
    print("------------------------------------------------------------------------------")
    joblib.dump(flow_model,'RFC')
    
    
flow_training()