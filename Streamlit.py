import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
data = pd.read_csv('https://raw.githubusercontent.com/Jinsol-Kwon/Streamlit-App/main/heart_2020_cleaned.csv')

Yes_No_Columns = [column for column in data.columns if (len(data[column].value_counts()) == 2)]
Yes_No_Columns.remove('HeartDisease')
Yes_No_Columns.remove('Sex')

for Column in Yes_No_Columns:
    data[Column] = 1 * (data[Column] == 'Yes')

data['Sex'] = 1 * (data['Sex'] == 'Male')

data['HeartDisease'] = 1 * (data['HeartDisease'] == 'Yes')
data['BMI'] = pd.cut(data['BMI'], [0,18.5,25.0,30.0,40,50,100], labels = [0,1,2,3,4,5], right = False)
data['PhysicalHealth'] = pd.cut(data['PhysicalHealth'], [0,1,10,20,30,31],labels = [0,1,2,3,4], right = False)
data['MentalHealth'] = pd.cut(data['MentalHealth'], [0,1,10,20,30,31],labels = [0,1,2,3,4], right = False)
data['SleepTime'] = pd.cut(data['SleepTime'], [1,5,6,10,25], labels =[0,1,2,3] , right = False)

AgeCategory_Value = {}

for category in sorted(list(data['AgeCategory'].unique())):
    AgeCategory_Value[category] = sorted(list(data['AgeCategory'].unique())).index(category)

data['AgeCategory'] = data['AgeCategory'].apply(lambda p: AgeCategory_Value[p])

GenHealth_Value = {'Poor': 0, 'Fair': 1, 'Good': 2, 'Very good': 3, 'Excellent': 4}

data['GenHealth'] = data['GenHealth'].apply(lambda p: GenHealth_Value[p])

for Race in data['Race'].unique():
    data[Race] = 1 * (data['Race'] == Race)

for Diabetic in data['Diabetic'].unique():
    data[Diabetic] = 1 * (data['Diabetic'] == Diabetic)   
    
data = data.drop(['Race','Diabetic'], axis = 1)

X = data.drop('HeartDisease', axis = 1)
y = data['HeartDisease']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=20, stratify = y)

Under = X_train.copy()
Under['HeartDisease'] = y_train
Under_0 = Under[Under['HeartDisease'] == 0].copy()
Under_1 = Under[Under['HeartDisease'] == 1].copy()

Under_Sample = pd.concat([Under_1, Under_0.sample(frac = len(Under_1)/len(Under_0))])

Streamlit = ['BMI','AgeCategory','Sex','DiffWalking','SleepTime','Stroke']

Classifier_Streamlit = LogisticRegression(max_iter = 300)

Classifier_Streamlit.fit(Under_Sample[Streamlit], Under_Sample['HeartDisease'])

with st.form('form'):
    st.title('Heart Disease Prediction App')
    
    st.write('Complete the information and click Submit')
    
    
    Age = st.slider('What is your Age?',step = 1, min_value=18, max_value=74)

    SleepTime = st.slider('On average, how many hours of sleep do you get in a 24-hour period?', 1,24)
    
    BMI = st.slider('What is your BMI?',min_value=13,max_value=60, step=None)
    
    Gender = st.selectbox('What is your Gender?', ['Male','Female'])
    
    DiffWalking = st.selectbox('Do you have serious difficulty walking or climbing stairs?', ['Yes','No'])
    
    Stroke = st.selectbox('(Ever told) (you had) a stroke?', ['Yes','No'])
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        Gender = 1 * (Gender == 'Gender')
        
        DiffWalking = 1 * (DiffWalking == 'Yes')
        
        Stroke = 1 * (Stroke == 'Yes')
        
        Sleep_Value = 0

        if SleepTime < 5:
            Sleep_Value = 0
        elif SleepTime < 6:
            Sleep_Value = 1
        elif SleepTime < 10:
            Sleep_Value = 2
        else:
            Sleep_Value = 3
        
        Age_Value = 0

        for Category, Value in AgeCategory_Value.items():
            if int(Category[:2]) <= Age <= int(Category[-2:]):
                Age_Value = Value
                
        Age = Age_Value
        
        BMI_Value = 0
        
        if BMI < 18.5:
            BMI_Value = 0
        elif BMI < 25:
            BMI_Value = 1
        elif BMI < 30:
            BMI_Value = 2
        elif BMI < 40:
            BMI_Value = 3
        elif BMI < 50:
            BMI_Value = 4
        else:
            BMI_Value = 5
        
        Result = Classifier_Streamlit.predict(pd.Series([BMI_Value,Age,Gender,DiffWalking,Sleep_Value,Stroke]).to_numpy().reshape(1,-1))[0]
        
        if Result == 1:
            Result = 'Yes'
        else:
            Result = 'No'
        
        st.write('The prediction output of the Logistic Regression for Heart Disease:   ' + Result)
