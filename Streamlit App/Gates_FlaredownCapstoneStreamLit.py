### THIS IS MY STREAMLIT APP

##Author: Sarah Gates
##Contact: sarahgates22@gmail.com

### import libraries
import pandas as pd
import numpy as np
import streamlit as st
import joblib

from sklearn.preprocessing import StandardScaler

#######################################################################################################################################
### LAUNCHING THE APP ON THE LOCAL MACHINE
### 1. Save your *.py file (the file and the dataset should be in the same folder)
### 2. Open git bash (Windows) or Terminal (MAC) and navigate (cd) to the folder containing the *.py and *.csv files
### 2.5 If you don't have the streamlit library installed, then use "pip install streamlit" in gitbash/terminal 
### 3. Execute... streamlit run <name_of_file.py>
### 4. The app will launch in your browser. A 'Rerun' button will appear every time you SAVE an update in the *.py file


#######################################################################################################################################
### Create a title

st.markdown("<h1 style='text-align: center; color: grey;'>Autoimmune Disease Prediction Using Machine Learning</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: light_blue;'>BrainStation Capstone </h2>", unsafe_allow_html=True)

st.markdown("<h5 style='text-align: center; color: grey;'>Author: Sarah Gates </h5>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: grey;'>Contact: sarahgates22@gmail.com</h5>", unsafe_allow_html=True)


st.image('./gallery_logoFull.png')


#######################################################################################################################################
############################################# BINARY CLASSIFICATION MODEL INFERENCE ###################################################
#######################################################################################################################################
st.markdown("<h2 style='text-align: center; color: light_blue;'>Fibromyalgia Prediction </h2>", unsafe_allow_html=True)

## Empty dataframe to fill
user_binary_df = pd.read_csv('data/binary_df.csv', index_col='Unnamed: 0')
user_binary_df.reset_index(inplace=True)
user_binary_df.drop(columns=['index'], inplace=True)
# Resetting values to 0
user_binary_df.loc[:,:] = 0


st.markdown("<h4 style='text-align: center; color: grey;'> Please Select Your Age and Gender </h4>", unsafe_allow_html=True)



########################################### BIOGRAPHICAL VARIABLES ###################################
age = st.selectbox('Age', options=[18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
       35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51,
       52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68,
       69,70, 71,72,73,74,75])
gender = st.selectbox('Gender', ['female', 'male', 'nonbinary'])


############################################ BINARY CONDITIONS #########################################

st.markdown("<h4 style='text-align: center; color: grey;'> Please Select Any Conditions You Have: </h4>", unsafe_allow_html=True)

conditions_select = st.multiselect('Conditions', ['anxiety',
 'arthritis',
 'asthma',
 'chronic fatigue syndrome',
 'depression',
 'ehlers-danlos syndrome',
 'endometriosis',
 'generalized anxiety disorder',
 'gerd',
 'insomnia',
 'irritable bowel syndrome',
 'lupus',
 'osteoarthritis',
 'polycystic ovary syndrome (pcos)',
 'post-traumatic stress disorder',
 'postural orthostatic tachycardia syndrome',
 'rheumatoid arthritis'])


conditions_selected = list()

for itemC in conditions_select:
    itemC = itemC.replace(" ", "_")
    conditions_selected.append(itemC)

st.markdown("<h4 style='text-align: center; color: grey;'> Please Select Any Symptoms You Have: </h4>", unsafe_allow_html=True)

################################################## BNARY SYMPTOMS #####################################################

symptoms_select = st.multiselect('Symptoms', ['abdominal pain',
 'acid reflux',
 'arm pain',
 'back pain',
 'bloating',
 'brain fog',
 'chest pain',
 'chronic pain',
 'constipation',
 'diarrhea',
 'difficulty concentrating',
 'dizziness or vertigo',
 'fatigue',
 'foot pain',
 'gas',
 'hand pain',
 'headache',
 'hip pain',
 'irritability',
 'jaw pain',
 'joint pain',
 'knee pain',
 'leg pain',
 'light sensitivity',
 'lightheadedness',
 'menstrual cramps',
 'migraine',
 'muscle ache',
 'muscle pain',
 'muscle spasm',
 'nausea',
 'neck pain',
 'nerve pain',
 'numbness and tingling',
 'palpitations',
 'pelvic pain',
 'rash',
 'shortness of breath',
 'shoulder pain',
 'sore throat',
 'stiffness',
 'stomach cramps',
 'stomach pain',
 'subluxation or dislocation',
 'sweating',
 'swelling',
 'tachycardia',
 'vomiting',
 'weakness'])

# converting list
symptoms_selected = list()

for itemS in symptoms_select:
    itemS = itemS.replace(" ", "_")
    symptoms_selected.append(itemS)

################################################################### UPDATING DATAFRAME ################################################################
# AGE
if age:
    user_binary_df['age'] = age
# setting age


if gender:
#setting gender:
    if gender == 'female':
        user_binary_df['female'] = 1
    if gender == 'nonbinary':
        user_binary_df['other'] = 1

conditions_number = 0
# filling in user input
for col in user_binary_df:
    if col in conditions_selected:
        conditions_number = conditions_number + 1
        user_binary_df[col] = 1
    # elif col not in symptoms_selected:
    #     user_binary_df[col] = 0

symptoms_number = 0
# filling in user input
for col in user_binary_df:
    if col in symptoms_selected:
        symptoms_number = symptoms_number + 1
        user_binary_df[col] = 1
    # elif col not in symptoms_selected:
    #     user_binary_df[col] = 0


# Adding in Fibro comorbs
comorbs = list(('anxiety', 'depression', 'migraine', 'chronic_fatigue_syndrome'))
comorb_act = 0
co_print = list()

for co in comorbs:
    if user_binary_df.loc[0, co] == 1:
        comorb_act = comorb_act + 1
        co = co.replace('_', ' ')
        co_print.append(co)

user_binary_df['fibro_comorbidities'] = comorb_act


############################################  Fibromyalgia Prediction ################################

st.markdown("<h4 style='text-align: center; color: grey;'> Final Prediction </h4>", unsafe_allow_html=True)

# A. Load the model using joblib
model = joblib.load('binary_final.pkl')
scaler = joblib.load('SCALERPICKLED.pkl')

X_scaled = scaler.transform(user_binary_df)

predict_it = st.button('Predict Fibromyalgia')

# C. Use the model to predict sentiment & write result
prediction = model.predict(X_scaled)
soft_prediction = ((model.predict_proba(X_scaled)[0][1])*100).round(2)

# B. USER SUMMARY 


if predict_it:
    st.markdown("<h3 style='text-align: left; color: white;'> User Summary: </h3>", unsafe_allow_html=True)
    st.metric(label="Age", value=age)
    st.metric(label='Gender', value=gender)
    # st.metric(label="Number of Conditions", value=conditions_number)
    # st.metric(label="Number of Symptoms", value=symptoms_number)
    st.metric(label="Number of Fibromyalgia Comorbidities", value=comorb_act)
    if comorb_act != 0:
        st.write('Fibromyalgia Comorbidites')
        # st.markdown("<h6 style='text-align: left; color: white;'> Fibromyalgia Comorbidites: </h6>", unsafe_allow_html=True)
        for co in co_print:
            st.markdown(f"<h3 style='text-align: left; color: white;'> {co} </h3>", unsafe_allow_html=True)

    # probability
    st.write('-----------------------------------------------------------')
    # st.markdown("<h3 style='text-align: left; color: white;'> \n </h3>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: left; color: white;'> Fibromyalgia Prediction </h3>", unsafe_allow_html=True)
    st.write('\n')
    st.metric(label="Probability of Having Fibromyalgia", value=(f"{soft_prediction}%"))

    if prediction == 1:
        st.write('We predict that you may have fibromyalgia.')
    else:
        st.write('We predict that you do not have fibromyalgia.')
        




