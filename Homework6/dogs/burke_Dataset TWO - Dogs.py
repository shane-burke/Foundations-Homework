#!/usr/bin/env python
# coding: utf-8

# # Homework 6, Part Two: A dataset about dogs.
# 
# Data from [a FOIL request to New York City](https://www.muckrock.com/foi/new-york-city-17/pet-licensing-data-for-new-york-city-23826/)

# ## Do your importing and your setup

# In[1]:


import pandas as pd


# ## Read in the file `NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx` and look at the first five rows

# In[2]:


df = pd.read_excel("NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx").head(30000)
df.head(5)


# ## How many rows do you have in the data? What are the column types?
# 
# If there are more than 30,000 rows in your dataset, go back and only read in the first 30,000.

# In[3]:


len(df)
#81937 but going back for 30,000


# In[4]:


df.shape


# In[5]:


df.dtypes


# ## Describe the dataset in words. What is each row? List two column titles along with what each of those columns means.
# 
# For example: “Each row is an animal in the zoo. `is_reptile` is whether the animal is a reptile or not”

# In[6]:


print("This is a dataset of dog licenses in NYC. Each row describes a dog.")
print("The animal birth column describes the birthdate in date format.")
print("The animal name column gives the animal's name. Most values in there are strings.")


# # Your thoughts
# 
# Think of four questions you could ask this dataset. **Don't ask them**, just write them down in the cell below. Feel free to use either Markdown or Python comments.

# 1. How many dogs were given licenses in November 2014?
# 2. Do people buy (and license) more dogs in any season?
# 3. What was the most popular breed for each month/year recorded?
# 4. The longest animal name licensed in the set

# # Looking at some dogs

# ## What are the most popular (primary) breeds of dogs? Graph the top 10.

# In[7]:


#print(list(df.columns))

new_names = []
for column in df.columns:
    new_names.append(column.replace(" ", "_").lower())    

df.columns = new_names


# In[8]:


df.primary_breed.value_counts().head(10).sort_values(ascending=True).plot(kind="barh")


# ## "Unknown" is a terrible breed! Graph the top 10 breeds that are NOT Unknown

# In[9]:


import numpy as np
df.primary_breed = df.primary_breed.replace({"Unknown": np.nan})

df.primary_breed.dropna().value_counts().head(10).sort_values(ascending=True).plot(kind="barh")


# ## What are the most popular dog names?

# In[10]:


df.animal_name = df.animal_name.replace({"UNKNOWN": np.nan})
df.animal_name.dropna().value_counts().head(10)


# ## Do any dogs have your name? How many dogs are named "Max," and how many are named "Maxwell"?

# In[11]:


print("yes, 6 are named shane:")
df[df.animal_name == "Shane"]


# In[12]:


#df[df.animal_name == "Max"].animal_name.value_counts()
#df[df.animal_name == "Maxwell"].animal_name.value_counts()

print("There are", len(df[df.animal_name == "Max"]), "dogs named Max.")
print("There are", len(df[df.animal_name == "Maxwell"]), "dogs named Maxwell.")


# ## What percentage of dogs are guard dogs?
# 
# Check out the documentation for [value counts](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.value_counts.html).

# In[13]:


print(df.guard_or_trained.value_counts(normalize=True)*100)
print("\n")
print(".08% of registered dogs are guard dogs or trained guard dogs.")


# ## What are the actual numbers?

# In[14]:


df.guard_or_trained.value_counts()


# ## Wait... if you add that up, is it the same as your number of rows? Where are the other dogs???? How can we find them??????
# 
# Use your `.head()` to think about it, then you'll do some magic with `.value_counts()`

# In[15]:


#df.guard_or_trained.value_counts(dropna=False)
print("There are 10,174 dogs with null values in the guard column.")


# ## Fill in all of those empty "Guard or Trained" columns with "No"
# 
# Then check your result with another `.value_counts()`

# In[16]:


df.guard_or_trained = df.guard_or_trained.replace({np.nan: "No"})
df.guard_or_trained.value_counts(dropna=False)


# ## What are the top dog breeds for guard dogs? 

# In[17]:


df[df.guard_or_trained == "Yes"].primary_breed.value_counts()

#lol a yorkie as a guard dog


# ## Create a new column called "year" that is the dog's year of birth
# 
# The `Animal Birth` column is a datetime, so you can get the year out of it with the code `df['Animal Birth'].apply(lambda birth: birth.year)`.

# In[18]:


df['birth_year'] = df.animal_birth.apply(lambda birth: birth.year)
print(df['birth_year'])


# ## Calculate a new column called “age” that shows approximately how old the dog is. How old are dogs on average?

# In[19]:


df['dog_age'] = 2020 - df['birth_year']

#print(df) to check it implemented

print(f'NYC dogs are {df.dog_age.mean():.0f} years old on average.')


# # Joining data together

# ## Which neighborhood does each dog live in?
# 
# You also have a (terrible) list of NYC neighborhoods in `zipcodes-neighborhoods.csv`. Join these two datasets together, so we know what neighborhood each dog lives in. **Be sure to not read it in as `df`, or else you'll overwrite your dogs dataframe.**

# In[20]:


neighborhoods = pd.read_csv("zipcodes-neighborhoods.csv")

merged = df.merge(neighborhoods, 
         left_on = 'owner_zip_code', 
         right_on = 'zip', 
         how = 'left')

merged = merged.drop(columns=['zip'])

merged


# ## What is the most popular dog name in all parts of the Bronx? How about Brooklyn? The Upper East Side?

# In[21]:


merged = merged.replace({'Unknown' : np.nan, 'unknown': np.nan})

print("Most Popular Names and Counts per Borough:")
borough_list = ["Bronx", "Manhattan", "Queens", "Brooklyn", "Staten Island"]
for borough in borough_list:
    print(borough)
    print(merged[merged.borough == borough].animal_name.value_counts().head(1))
    print("---")

print("The most popular dog name in the Upper East Side is", merged[merged.neighborhood == "Upper East Side"].animal_name.value_counts().head(1).index[0], ".")
print("There are", merged[merged.neighborhood == "Upper East Side"].animal_name.value_counts().head(1).values[0], "of them in the UES.")


# ## What is the most common dog breed in each of the neighborhoods of NYC?

# In[22]:


print("Most Popular Breeds and Counts per Borough:")
borough_list = ["Bronx", "Manhattan", "Queens", "Brooklyn", "Staten Island"]
for borough in borough_list:
    print(borough)
    print(merged[merged.borough == borough].primary_breed.value_counts().head(1))
    print("---")


# In[ ]:





# In[ ]:





# ## What breed of dogs are the least likely to be spayed? Male or female?

# In[23]:


print("Male Spayed %:")
print(df[df.animal_gender == "M"].spayed_or_neut.value_counts(normalize="true"))
print('\n')

print("Female Spayed %:")
print(df[df.animal_gender == "F"].spayed_or_neut.value_counts(normalize="true"))

print('\n')
print("Male dogs are least likely to be spayed")


# ## Make a new column called monochrome that is True for any animal that only has black, white or grey as one of its colors. How many animals are monochrome?

# In[24]:


colors = []
for color in df.animal_dominant_color:
    colors.append(str(color).lower())

df.animal_dominant_color = colors


# In[25]:


df[(df.animal_dominant_color == "black") & (df.animal_secondary_color.isnull()) |
  (df.animal_dominant_color == "grey") & (df.animal_secondary_color.isnull()) | 
   ((df.animal_dominant_color == "gray") & (df.animal_secondary_color.isnull()))|
  (df.animal_dominant_color == "white") & (df.animal_secondary_color.isnull())]


# In[26]:


monochrome_num = df[(df.animal_dominant_color == "black") & (df.animal_secondary_color.isnull()) |
  (df.animal_dominant_color == "grey") & (df.animal_secondary_color.isnull()) | 
   ((df.animal_dominant_color == "gray") & (df.animal_secondary_color.isnull()))|
  (df.animal_dominant_color == "white") & (df.animal_secondary_color.isnull())] \
    .animal_dominant_color.value_counts().sum()

print(f'There are {monochrome_num:,} monochrome dogs in the list.')


# ## How many dogs are in each borough? Plot it in a graph.

# In[27]:


merged.borough.value_counts().sort_values(ascending=True).plot(kind='barh')


# ## Which borough has the highest number of dogs per-capita?
# 
# You’ll need to merge in `population_boro.csv`

# In[28]:


pops = pd.read_csv("boro_population.csv")

per_cap_df = merged.borough.value_counts().reset_index()
per_cap_df = per_cap_df.rename(columns = {'index': 'borough', 'borough': 'count'})

per_cap_df = per_cap_df.merge(pops, 
         left_on = 'borough', 
         right_on = 'borough', 
         how = 'left')

per_cap_df['per_capita'] = per_cap_df['count'] / per_cap_df['population']

top_borough = per_cap_df.sort_values(by = 'per_capita', ascending=False).head(1).borough.values[0]

print(f'{top_borough} has the most dogs per capita.')


# ## Make a bar graph of the top 5 breeds in each borough.
# 
# How do you groupby and then only take the top X number? You **really** should ask me, because it's kind of crazy.

# In[29]:


merged.groupby('borough').primary_breed.value_counts().groupby(level=0).nlargest(5).plot(kind='barh', figsize=(10, 12))


# ## What percentage of dogs are not guard dogs?

# In[30]:


not_guard_pct = df.guard_or_trained.value_counts(normalize = True)["No"]

print(f'{not_guard_pct * 100 :.2f}% are not guard dogs.')


# In[ ]:




