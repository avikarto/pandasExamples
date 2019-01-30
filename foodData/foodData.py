# Analysis of USDA nutrition data
# This code was written in the Atom IDE with Hydrogen as a Jupyter environment
# The # %% lines are cell breaks in Hydrogen

import pandas as pd
import numpy as np
import json
import os

# %%

db = json.load(open(os.getcwd()+'\\database.json'))
len(db)  # number of food entries in the database

# %%
# Each entry is a mess in this raw dictionary/JSON format:

db[0]

# %%
# I want this all in a dataframe.  What does the raw data look like, and how can I shape it?

db[0].keys()
# %%
db[0]['nutrients']

# %%
# This is the list of nutrients tracked for each food item.  So many nutrients!

for i in range(len(db[0]['nutrients'])):
    print(db[0]['nutrients'][i]['description'])

# %%
# I don't really need all of the information that is available here.  I'll pick some and make a smaller df out of it.

interestingParts = ['description', 'nutrients', 'portions']
df = pd.DataFrame(db, columns=interestingParts)
df.head()

# %%
# Let's say I'm only interested in the nutritional information for kcal, fats, protein, and carbs.

df1 = df.reindex(columns=interestingParts+['kcal', 'fats (g)', 'protein (g)', 'carbs (g)'], fill_value=0.0)
df1.head()

# %%
# However, these nutrients don't hold the same position in each database entry:

for i in range(5):
    print(df1['nutrients'][i][0].get('description'))

# %%
# Therefore, we must search each database entry for each of these 4 nutrients for each food and
# add it to appropriate column of df1.  These lists of nutrients don't have the same length either,
# and there are duplicate entries (some with different units) so the data must be iterated over dynamically.

for i in range(len(df1)):
    for j in range(len(df1['nutrients'][i])):
        if df1['nutrients'][i][j].get('description') == 'Protein' and df1['nutrients'][i][j].get('units') == 'g':
            df1.loc[i, 'protein (g)'] = df1['nutrients'][i][j].get('value')
        elif df1['nutrients'][i][j].get('description') == 'Total lipid (fat)' and df1['nutrients'][i][j].get('units') == 'g':
            df1.loc[i, 'fats (g)'] = df1['nutrients'][i][j].get('value')
        elif df1['nutrients'][i][j].get('description') == 'Carbohydrate, by difference' and df1['nutrients'][i][j].get('units') == 'g':
            df1.loc[i, 'carbs (g)'] = df1['nutrients'][i][j].get('value')
        elif df1['nutrients'][i][j].get('description') == 'Energy' and df1['nutrients'][i][j].get('units') == 'kcal':
            df1.loc[i, 'kcal'] = df1['nutrients'][i][j].get('value')

df1.drop(labels=['nutrients'], axis='columns', inplace=True)
df1.head()

# %%
# Let's confirm that these were set properly by comparing with some entries in the original database.

for i in range(5):
    kept = ['Protein', 'Total lipid (fat)', 'Carbohydrate, by difference', 'Energy']
    print(db[i].get('description'))
    for j in range(len(db[i]['nutrients'])):
        if db[i]['nutrients'][j].get('description') in kept and db[i]['nutrients'][j].get('units') in ['g', 'kcal']:
            kept.remove(db[i]['nutrients'][j].get('description'))
            print(' ', db[i]['nutrients'][j].get('description'), db[i]['nutrients'][j].get('value'), db[i]['nutrients'][j].get('units'))
    print('')
# looks good!

# %%
# Let's say that I need to find some foods with high protein and low calories.  Let's find a protein/kcal ratio of all foods.

df1['prot/kcal'] = df1['protein (g)']/df1['kcal']
df1.sort_values(by="prot/kcal", ascending=False, inplace=True)
df1.head()

# %%
# Let's assume that zero-calorie foods such as coffee are not appropriate sources of protein, and remove them from consideration.
# While we are at it, let's remove anything with less than 1 gram of protein per serving as these are likely not good sources either.

noZeroCal = df1.copy()
for i in range(len(noZeroCal)-1, -1, -1):
    if noZeroCal.iloc[i]['kcal'] == 0 or noZeroCal.iloc[i]['protein (g)'] < 1:
        noZeroCal.drop(noZeroCal.iloc[i].name, inplace=True)
noZeroCal.head()
