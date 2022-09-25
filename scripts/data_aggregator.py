def data_aggregator(df, DV_list): # change date diff to unique number of dates

    ''' This function aggregates incoming cleaned data, and transforms it such that there is a single user's data on each row of of the new dataframe.'''

    import numpy as np
    import pandas as pd
    from tqdm.notebook import tqdm, trange
    import time    # to be used in loop iterations

    # Turning off warning messages
    pd.options.mode.chained_assignment = None  # default='warn'

    assert isinstance(df, pd.DataFrame), f'Please enter a dataframe, you have entered a {type(df)} data type.'

    print('Beginning aggregation...')

    ## Removing the DVS from the Dataset ##

    print("\n\nFirst, I will remove the dependent variables from the dataset conditions: ")

    for DV in DV_list:
        print(f"\tRemoving {DV} from the dataset")
        df.drop(df[df.trackable_name == DV].index, inplace=True)

    # Initialize needed items
    comorbs = list(('anxiety', 'depression', 'migraine', 'chronic fatigue syndrome'))

    user_data = dict()
    
    DV_list = DV_list

    full_conditions_list = list(df[df['trackable_type'] == 'Condition'].trackable_name.unique())

    print(f"\n\nHere is the final condition list:")

    for condition in full_conditions_list:
        print(f"\t{condition}")

    # all the possible symptoms
    full_symptoms_list = list(df[df['trackable_type'] == 'Symptom'].trackable_name.unique())

    print(f"\n\nHere is the final symptoms list:")

    for symptom in full_symptoms_list:
        print(f"\t{symptom}")

    ids_list = df.ids.unique()

    print("Extracting user level information...")
    print("\n\nCreating the following basic variables: \no Age\no Gender\no Country\no Fibromyalgia\no Total Logs\no Total Unique Dates (Days)\no Total Logging Rate\no Conditions Total\no Symptoms Total")
    print("\n\nCreating the following variables for each condition and symptom: \no Condition/Symptom Binary (0/1)\no Condition/Symptom Total Logs\no Condition/Symptom Activity (median trackable value)\no Condition/Symptom Unique Dates (Days) \no Condition/Symptom Log Rate")
    print("\n\nThis will take a while. Perhaps grab a coffee?")

    for id in tqdm(ids_list):
    
        id_df = df[df['ids'] == id]

        # Get the dependent variable (target), will append it last:

        id_target = id_df['target'].unique()

        ### GENERAL INFORMATION ##
    
        ids = {'ids': id}
        age = {'age': id_df.age.unique()}
        gender = {'gender': id_df.sex.unique()}
        country = {'country': id_df.country.unique()}
        total_logs = {'total_logs': len(id_df)}
        target_type = {'target': id_target}

        # Total date range and log rate in days
        unique = id_df.checkin_date.nunique()

        total_log_day_unique= {'total_unique_dates_days': unique}

        # Now the logging rate by day 

        rate = len(id_df) / unique

        total_log_rate = {'total_log_rate': rate}

        #add these to dictionary
        user_data[id] = ids
        user_data[id].update(age)
        user_data[id].update(gender)
        user_data[id].update(country)
        user_data[id].update(target_type)
        user_data[id].update(total_logs)
        user_data[id].update(total_log_day_unique)
        user_data[id].update(total_log_rate)

        
        #### CONDITIONS ####

        ## temporary condition dataframe
        condition_df = id_df[id_df['trackable_type'] == 'Condition']

        # dictionary for appending info
        conditions_dict = dict()
    
        #-measures-#

        # total conditions logged minus the DV
        id_conditions_list = list(condition_df.trackable_name.unique())
        
    
        condition_number = {'conditions_total': len(id_conditions_list)} # Append it

    # total fibro comorbs
        comorb_number = 0
        for comorb in comorbs:
            if comorb in id_conditions_list:
                comorb_number = comorb_number + 1

        comorbidities = {'fibro_comorbidities': comorb_number}

        # information for each individual condition
        for condition in full_conditions_list:
    
            condition_dict = dict()

            if condition in id_conditions_list:
                # Has condition = 1
                condition_dict[condition] = 1

                # Total number of logs
                condition_log = int(condition_df[condition_df['trackable_name'] == condition].trackable_name.count())
                condition_dict[f"{condition}_total_logs"] = int(condition_log)

                # Median trackable value

                condition_value = int(condition_df[condition_df['trackable_name'] == condition].trackable_value.median())
                condition_dict[f"{condition}_activity"] = condition_value

                # Total numbers of days logged
                uniqueC = condition_df.checkin_date.nunique()

                condition_dict[f"{condition}_unique_dates_days"] = uniqueC

                rateC = condition_log / uniqueC
    
                condition_dict[f"{condition}_log_rate"] = rateC

                # conditions_dict[condition] = condition_dict
                # median trackable value
        
            else:
        
                # if have
                condition_dict[condition] = 0

                #number of logs
                condition_dict[f"{condition}_total_logs"] = 0

                #Median activity value
                condition_dict[f"{condition}_activity"] = 0

                #Condition unique dates
                condition_dict[f"{condition}_unique_dates_days"] = 0

                # logging frequency
                condition_dict[f"{condition}_log_rate"] = 0

            conditions_dict.update(condition_dict)
             
        # add to dictionary
        
        user_data[id].update(condition_number)
        user_data[id].update(comorbidities)
        user_data[id].update(conditions_dict)

        
        
        ###  SYMPTOMS ####

        # symptom temp dataframe 
        symptom_df = id_df[id_df['trackable_type'] == 'Symptom']

        # dict for adding
        symptoms_dict = dict()
    
        #-measures-#

        # total symptoms logged
        id_symptoms_list = list(symptom_df.trackable_name.unique())
        symptom_number = {'symptoms_total': len(id_symptoms_list)}
        # Add to dictionary
        user_data[id].update(symptom_number)

        # For loop for symptom specific data
        for symptom in full_symptoms_list:
    
            symptom_dict = dict()

            if symptom in id_symptoms_list:
                # Has condition = 1
                symptom_dict[symptom] = 1

                # Total number of logs
                symptom_log = int(symptom_df[symptom_df['trackable_name'] == symptom].trackable_name.count())
                symptom_dict[f"{symptom}_total_logs"] = int(symptom_log)

                # Median trackable value

                symptom_value = int(symptom_df[symptom_df['trackable_name'] == symptom].trackable_value.median())
                symptom_dict[f"{symptom}_activity"] = symptom_value

                # Total numbers of days logged
                uniqueS = symptom_df.checkin_date.nunique()

                symptom_dict[f"{symptom}_unique_dates_days"] = uniqueS

                rateS = symptom_log / uniqueS

                symptom_dict[f"{symptom}_log_rate"] = rateS

                # conditions_dict[condition] = condition_dict
                # median trackable value
        
            else:
        
                # if have
                symptom_dict[symptom] = 0

                #number of logs
                symptom_dict[f"{symptom}_total_logs"] = 0

                #Median activity value
                symptom_dict[f"{symptom}_activity"] = 0

                #Symptom unique dates logged
                symptom_dict[f"{symptom}_unique_dates_days"] = 0

                # number of loggin rate
                symptom_dict[f"{symptom}_log_rate"] = 0

            symptoms_dict.update(symptom_dict)
            
        # add general info and condition information
    
        user_data[id].update(symptoms_dict)


    # Final Aggregations

    print('\n\nDone! Creating the dataframe...')
    
    df_agg = pd.DataFrame.from_dict(user_data, orient='index')

    print(f'Fixing the column names for modeling...')

    columns = list(df_agg.columns)
    new_cols = list()

    for col in columns:
        col = col.replace(" ", "_")
        new_cols.append(col)
    
    df_agg.columns = new_cols

    print(f"Here are your new columns!")

    for column in new_cols:
        print(f"\t {column}")

    print('\n\nAll done!')

    # fixing columns data types

    df_agg['age'] = df_agg['age'].astype('int')
    df_agg['gender'] = df_agg['gender'].str[0]
    df_agg['country'] = df_agg['country'].str[0]
    df_agg['target'] = df_agg['target'].astype('int')

    # resetting index
    df_agg.reset_index(inplace=True)
    df_agg.drop(columns=['index'], inplace=True)
    

    return df_agg