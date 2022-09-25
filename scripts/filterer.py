def filterer(df):

    '''This filterer filters users who have logged at least one symptom and one condition. '''

    import numpy as np
    import pandas as pd

    assert isinstance(df, pd.DataFrame), f"Please enter a dataframe, you entered a {type(df)} data type"
    
    conditions = df[df['trackable_type'] == 'Condition']
    symptoms = df[df['trackable_type'] == 'Symptom']

    #Grouping these by IDs
    grouped_df_all = df.groupby(by='ids')
    cond_group = conditions.groupby(by='ids')
    symp_group = symptoms.groupby(by='ids')

    print(f"\n\nThere are {len(dict(grouped_df_all.ids.nunique()))} users the dataset")

    condition_numbers = dict(cond_group.trackable_name.nunique())

    symptom_numbers = dict(symp_group.trackable_name.nunique())

    print(f"\n\nThere are {len(condition_numbers)} users that have logged conditions")
    print(f'There are {len(symptom_numbers)} users that have logged symptoms')

    symptom_list = list()
    c_and_s_list = list()

    #  First, I'll create a list of users that have logged at least one unique symptom:

    for i,j in symptom_numbers.items():
        if j >= 1:
            symptom_list.append(i)
    
    print(f"\n\nThere are {len(symptom_list)} users who have logged one or more symptoms.")

    # Then, I will check for these users, if they have also logged at least one condition

    for i in condition_numbers.keys():
        if i in symptom_list:
            c_and_s_list.append(i)
    

    print(f"\n\nThere are {len(c_and_s_list)} users that have logged both conditions and symptoms.")
    print(f"\n\nRemoving {len(dict(grouped_df_all.ids.nunique())) - len(c_and_s_list)} users from the dataset")

    df_f = df.copy()

    df_filtered = df_f[df_f['ids'].isin(c_and_s_list)]

    print(f"\n\nThere are now {df_filtered.ids.nunique()} users in your dataframe.")
    print("Here is your dataframe!")

    return df_filtered