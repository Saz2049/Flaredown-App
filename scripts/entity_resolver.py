def entity_resolver(list1, list2, df, string):

    '''This function takes in two lists, a dataframe and a string: list1 is the full list of conditions within the concerned parameter, and list2 are items from this list for exclusion.
    It then replaces the resolved list items in the dataframe with the string provided.'''

    import pandas as pd

    assert isinstance(df, pd.DataFrame), f"Please enter a dataframe, you entered a {type(df)} data type"
    assert isinstance(list1, list), f"Please enter a dataframe, you entered a {type(list1)} data type"
    assert isinstance(list2, list), f"Please enter a dataframe, you entered a {type(list2)} data type"
    assert isinstance(string, str), f"Please enter a dataframe, you entered a {type(string)} data type"

    to_resolve_list = list1

    print(f"\n\nHere are the items to exclude {list2}")

    for item in list1:
        if item in list2:
            print(f"Dropping {item}")
            to_resolve_list.remove(item)
        else: 
            print(f'Keeping {item}')

    print("\n\nHere is the final list of things to resolve", to_resolve_list)

    print(f"\n\nReplacing the list with the string {string}")

    df.trackable_name.replace(to_resolve_list, string, inplace=True)
    
    print(df)

    return df