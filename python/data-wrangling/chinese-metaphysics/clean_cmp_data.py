import numpy as np
import pandas as pd
import math

# Read each excel sheet as a DataFrame and append to dict
file_path = 'raw_data.xlsx'
sheets = {}
for sheet in range(1928, 2041):
    df = pd.read_excel(file_path, sheet_name=str(sheet))
    sheets[sheet] = df

# Open a new excel file in write mode
with pd.ExcelWriter('clean_data.xlsx', engine = "openpyxl", mode = "w") as writer:

    # Clean data for each DataFrame
    for sheet, df in sheets.items():
        # Populate all NaN cells in 'Year' column with the first value
        df['Year'].fillna(value=df.loc[0]['Year'], inplace=True)

        # Loop through each cell in 'Month' column and replace NaN cells with appropriate value
        current_gregorian_month = 0
        for index, month in df['Month'].items():
            if math.isnan(month):
                pass
            elif month != current_gregorian_month and not math.isnan(month):
                current_gregorian_month = month
            df.loc[index, 'Month'] = current_gregorian_month

        # Remove empty column
        df.drop(labels=['Unnamed: 3'], axis=1, inplace=True)

        # Create 2 new columns - 'HS (Year)', 'EB (Year)'
        empty_array = np.zeros(len(df), dtype=str)
        df.insert(3, 'HS (Year)', empty_array)
        df.insert(4, 'EB (Year)', empty_array)

        # Loop through each cell in 'Lunar' column and split the value into 'HS (Year)' and 'EB (Year)'
        current_lunar_day = ''
        for index, lunar in enumerate(df['Lunar']):
            if isinstance(lunar, str):
                current_lunar_day = lunar
            elif math.isnan(lunar):
                pass
            df.loc[index, 'HS (Year)'] = current_lunar_day[0:3]
            df.loc[index, 'EB (Year)'] = current_lunar_day[3:]

        # Remove 'Lunar' column
        df.drop(labels=['Lunar'], axis=1, inplace=True)

        # Loop through each cell in 'Zodiac' column and replace NaN cells with appropriate value
        current_zodiac = ''
        for index, zodiac in enumerate(df['Zodiac']):
            if isinstance(zodiac, str):
                current_zodiac = zodiac
            elif math.isnan(zodiac):
                pass
            df.loc[index, 'Zodiac'] = current_zodiac

        # Loop through each cell in 'Month' column and replace NaN cells with appropriate value
        current_lunar_month = 0
        for index, month in enumerate(df['Month.1']):
            if math.isnan(month):
                pass
            elif month != current_lunar_month:
                current_lunar_month = month
            df.loc[index, 'Month.1'] = current_lunar_month

        # Rename 'Month.1' and 'Day.1' columns
        df.rename(
            columns={'Month.1': 'Lunar Month', 'Day.1': 'Lunar Day'},
            inplace=True
        )

        # Create 1 new column - 'Lunar Year'
        empty_array = np.zeros(len(df), dtype=int)
        df.insert(6, 'Lunar Year', empty_array)

        # Fill 'Lunar Year' column with appropriate values
        current_gregorian_year = df.loc[0, 'Year']
        for index, month in enumerate(df['Lunar Month']):
            if month == 1:
                break
            else:
                df.loc[index, 'Lunar Year'] = current_gregorian_year - 1

        df['Lunar Year'].replace(to_replace=0, value=current_gregorian_year, inplace=True)
            
        # Remove empty column
        df.drop(labels=['Unnamed: 8'], axis=1, inplace=True)

        # Create 2 new columns - 'HS (Day)', 'EB (Day)'
        empty_array = np.zeros(len(df), dtype=str)
        df.insert(8, 'HS (Day)', empty_array)
        df.insert(9, 'EB (Day)', empty_array)

        # Loop through each cell in 'HS/EB' column and split the value into 'HS (Day)' and 'EB (Day)'
        current_lunar_day = ''
        for index, lunar in enumerate(df['HS/EB']):
            if isinstance(lunar, str):
                current_lunar_day = lunar
            elif math.isnan(lunar):
                pass
            df.loc[index, 'HS (Day)'] = current_lunar_day[0:3]
            df.loc[index, 'EB (Day)'] = current_lunar_day[3:]

        # Remove 'HS/EB' column
        df.drop(labels=['HS/EB'], axis=1, inplace=True)

        # Write DataFrame to a new sheet
        df.to_excel(writer, sheet_name=str(sheet), index=False)


print('done')