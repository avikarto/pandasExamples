# Analysis of national baby names from 1880-2017
# This code was written in the Atom IDE with Hydrogen as a Jupyter environment
# The # %% lines are cell breaks in Hydrogen

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %%
# The data is split into files for each year, so let's import all data with that in mind
years = range(1880, 2018)
cols = ['Name', 'Sex', 'Counts']  # these are the columns in the comma-delimited data files
rawData = []

root = os.getcwd()
for year in years:
    path = root + '\\nameData\\yob%d.txt' % year
    tempFrame = pd.read_csv(path, names=cols)  # import the yearly data
    tempFrame['Year'] = year  # label this data set with the year
    rawData.append(tempFrame)

df = pd.concat(rawData, ignore_index=True)  # ignore_index=True to avoid duplicate indices from similarly indexed files
df.head()

# %%

# -------------------------------------------------------------------------
# How do birth rates differ by sex?
# -------------------------------------------------------------------------

birthsBySex = df.pivot_table(values='Counts', index='Year', columns='Sex', aggfunc=sum)
birthsBySex.tail()

# %%
birthsBySex.plot()
# %%

# -------------------------------------------------------------------------
# How have birth rates changed over the years?
# -------------------------------------------------------------------------

fData = birthsBySex['F'].values
mData = birthsBySex['M'].values
plt.xlabel('Year')
plt.ylabel('Births')
plt.title('Total births by year and sex')
plt.plot(years, fData, 'k', label='Female')
plt.plot(years, mData, 'b', label='Male')
plt.legend()
plt.show()

# %%

# -------------------------------------------------------------------------
# How common has my name been historically?
# -------------------------------------------------------------------------

myName = 'Andrew'
myNameDF = df.loc[df['Name'] == myName]
myNameDF.tail()

# %%

# -------------------------------------------------------------------------
# Apparently, Andrew has been a female name also.  How commonly overall?
# -------------------------------------------------------------------------

nameSexDF = myNameDF.pivot_table(values='Counts', aggfunc='sum', index='Sex')
nameSexDF['%'] = nameSexDF['Counts']/nameSexDF['Counts'].sum()*100
nameSexDF

# %%

# -------------------------------------------------------------------------
# How often has this happened by year, compared to the male case?
# -------------------------------------------------------------------------

sexByYear = myNameDF.drop(labels='Name', axis='columns')
sexByYear = sexByYear.pivot(index='Year', columns='Sex', values='Counts')
sexByYear.fillna(value=0, inplace=True)

plt.plot(years, sexByYear.F*100, label='F (x100)', color='g')
plt.plot(years, sexByYear.M, label='M', color='b')
plt.legend()
plt.title('Relative commonality of my name for males and females')
plt.show()
# %%
# An alternative display of the above, using twinx instead of value scaling
plt.ylabel('Female', color='g')
plt.tick_params(axis='y', colors='g')
plt.plot(years, sexByYear.F, 'g-')

plt.twinx()  # two plots share an x-axis, with different y-scales
plt.ylabel('Male', color='b')
plt.tick_params(axis='y', colors='b')
plt.plot(years, sexByYear.M, 'b-')
plt.title('Relative commonality - alternative display')
plt.show()

# %%
# -------------------------------------------------------------------------
# How has the average length of baby names changed?
# -------------------------------------------------------------------------

# We start by finding the length of each name and adding it to df
df['Length'] = df['Name'].str.len()
df.head()

# %%
# Let's compute a weighted average of name lengths by year
# The weighting will be by name popularity
df['CountLengths'] = df['Counts']*df['Length']
dfYearGroups = df.groupby('Year')
averages = {}
for year in years:
    ttlCountLengths = dfYearGroups.get_group(year).CountLengths.sum()
    ttlCounts = dfYearGroups.get_group(year).Counts.sum()
    averages[year] = ttlCountLengths/ttlCounts

# %%
xs = list(averages.keys())
ys = list(averages.values())
plt.title('Average name length by year')
plt.plot(xs, ys)
plt.show()
# %%

# -------------------------------------------------------------------------
# How many unique names have babies had by year?
# -------------------------------------------------------------------------

ys = []
for year in years:
        ys.append(dfYearGroups.get_group(year).Name.size)

plt.title('Number of unique names by year')
plt.plot(xs, ys)
plt.show()
# %%

# -------------------------------------------------------------------------
# What was the most popular name for each sex by year?
# -------------------------------------------------------------------------

df1 = df.drop(columns=['Length', 'CountLengths']).sort_values(by='Counts', ascending=False)
popularityFrame = df1.groupby(['Year', 'Sex'])

popularNames = {}
for year in years:
    tempM = popularityFrame.get_group((year, 'M')).iloc[0].Name
    tempF = popularityFrame.get_group((year, 'F')).iloc[0].Name
    popularNames[year] = [tempM, tempF]

# %%
popDF = pd.DataFrame(popularNames).T
popDF.columns = ['M', 'F']
popDF.tail()

# %%
# I want to visualize these results for males and females individually
maleNames = popDF.M.unique()
malePercentages = [list(popDF.M.values).count(x)/popDF.M.size*100 for x in maleNames]
femaleNames = popDF.F.unique()
femalePercentages = [list(popDF.F.values).count(x)/popDF.F.size*100 for x in femaleNames]
# %%
plt.title('Relative popularity of most popular male names')
plt.pie(malePercentages, labels=maleNames, autopct='%1.1f%%')
plt.show()
# %%
plt.title('Relative popularity of most popular female names')
plt.pie(femalePercentages, labels=femaleNames, autopct='%1.1f%%')
plt.show()
