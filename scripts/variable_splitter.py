
def variable_splitter(df):

    '''This function takes in a dataframe, and outputs several X and Y variable subsets for the Flaredown Capstone project. Those Variable Lists include:
    
        o y = The DV (target)
        o Several IV (X) subsets: 
            o All Variables
            o Basic Variables (age, gender (female, other), total logs, total unique date days, total log rate, conditions total, symptoms toal and fibro comorbidities)
            o Symptom / Condition Binaries
            o Symptom / Condition Total Logs
            o Symptom / Condition Activity
            o Symptom / Condition Log Rate
     '''
    import pandas as pd

    # making sure getting a dataframe
    assert isinstance(df, pd.DataFrame), f"Please enter a dataframe, you entered a {type(df)} data type"

    df = df.drop(columns=['gender', 'country', 'male'])

    # extracting the target
    y = df['target']

    #Creating the X variables

    # all
    X_all = df.copy()
    X_all.drop(columns='target', inplace=True)

    # Basic
    X_basic = df[['ids','age', 'female', 'other', 'total_logs',
       'total_unique_dates_days', 'total_log_rate', 'conditions_total', 'symptoms_total',
       'fibro_comorbidities']]
    
    all_cols = list(X_all.columns)
    columns_new = list()
    X_basic_list = list(X_basic.columns)

    for col in all_cols:
        if col not in X_basic_list:
            columns_new.append(col)

    # creating the other X variables: binary, total logs, activity, log rate, and unique dates
    X_CS_binaries_list = list()
    X_CS_total_logs_list = list()
    X_CS_activity_list = list()
    X_CS_log_rate_list = list()
    X_CS_unique_dates_list = list()

    print("Total Condition / Symptom Binary length", len(X_CS_binaries_list))
    print("Total logs length:", len(X_CS_total_logs_list))
    print("Median activity length:",len(X_CS_activity_list))
    print("Log rate length:",len(X_CS_log_rate_list))
    print("Unique dates length:",len(X_CS_unique_dates_list))

    for col in columns_new:
        if "_activity" in col:
            X_CS_activity_list.append(col)
        elif '_total_logs' in col:
            X_CS_total_logs_list.append(col)
        elif "_log_rate" in col:
            X_CS_log_rate_list.append(col)
        elif "_unique_dates_days" in col:
            X_CS_unique_dates_list.append(col)

    # adding the basic variables into each list
    X_CS_binaries_list = X_basic_list + X_CS_binaries_list 
    X_CS_total_logs_list = X_basic_list + X_CS_total_logs_list
    X_CS_activity_list = X_basic_list + X_CS_activity_list
    X_CS_log_rate_list = X_basic_list + X_CS_log_rate_list
    X_CS_unique_dates_list = X_basic_list + X_CS_unique_dates_list

     # creating condition and symptom binaries
    to_remove = X_CS_total_logs_list + X_CS_activity_list + X_CS_log_rate_list + X_CS_unique_dates_list

    for col in all_cols:
        if col not in to_remove:
            X_CS_binaries_list.append(col)

    print("Total Condition / Symptom Binary length", len(X_CS_binaries_list))
    print("Total logs length:", len(X_CS_total_logs_list))
    print("Median activity length:",len(X_CS_activity_list))
    print("Log rate length:",len(X_CS_log_rate_list))
    print("Unique dates length:",len(X_CS_unique_dates_list))

    # Creating X variables

    X_CS_binary = df[X_CS_binaries_list]
    X_CS_total_logs = df[X_CS_total_logs_list]
    X_CS_activity = df[X_CS_activity_list]
    X_CS_log_rate = df[X_CS_log_rate_list]
    X_CS_unique_dates = df[X_CS_unique_dates_list]

    # returning them

    return y, X_all, X_basic, X_CS_binary, X_CS_total_logs, X_CS_activity, X_CS_log_rate, X_CS_unique_dates
