#!/usr/bin/env python
# coding: utf-8

# # Homework 5, Part 2: Answer questions with pandas
# 
# **Use the Excel file to answer the following questions.** This is a little more typical of what your data exploration will look like with pandas.

# ## 0) Setup
# 
# Import pandas **with the correct name** .

# In[1]:


import pandas as pd
#!pip install xlrd
import xlrd


# ## 1) Reading in an Excel file
# 
# Use pandas to read in the `richpeople.xlsx` Excel file, saving it as a variable with the name we'll always use for a dataframe.
# 
# > **TIP:** You will use `read_excel` instead of `read_csv`, *but you'll also need to install a new library*. You might need to restart your kernel afterward!

# In[2]:


df = pd.read_excel("richpeople.xlsx")

#df


# ## 2) Checking your data
# 
# Display the number of rows and columns in your data. Also display the names and data types of each column.

# In[3]:


print(len(df), "rows")
print(len(df.columns), "columns")
print("---")
df.info()


# In[ ]:





# In[ ]:





# ## 3) Who are the top 10 richest billionaires? Use the `networthusbillion` column.

# In[4]:


df.sort_values(by='networthusbillion', ascending = False).head(10)


# ## 4) How many male billionaires are there compared to the number of female billionares? What percent is that? Do they have a different average wealth?
# 
# > **TIP:** The last part uses `groupby`, but the count/percent part does not.
# > **TIP:** When I say "average," you can pick what kind of average you use.

# In[5]:


print("---   Counts:   ---")
print(df.gender.value_counts())
print("/n")
print("---   Percents:   ---")
print(round(df.gender.value_counts() / len(df) * 100, 1))


# In[6]:


print("---   Avg. Net Worth by Gender   ---")
print(df.groupby('gender').networthusbillion.mean())


# ## 5) What is the most common source/type of wealth? Is it different between males and females?
# 
# > **TIP:** You know how to `groupby` and you know how to count how many times a value is in a column. Can you put them together???
# > **TIP:** Use percentages for this, it makes it a lot more readable.

# In[7]:


print("Top source of wealth:", df.sourceofwealth.mode()[0])
print("Top type of wealth:", df.typeofwealth.mode()[0])


# In[8]:


df_source_by_gender = df.groupby('gender').sourceofwealth.value_counts(ascending = False)

print("Top 5 Male Billionaire Sources of Wealth By Pct.")
print(df_source_by_gender.male.sort_values(ascending=False).head(5)/len(df_source_by_gender.male)*100)
print("\n")

print("Top 5 Female Billionaire Sources of Wealth By Pct.")
print(df_source_by_gender.female.sort_values(ascending=False).head(5)/len(df_source_by_gender.female)*100)


# ## 6) What companies have the most billionaires? Graph the top 5 as a horizontal bar graph.
# 
# > **TIP:** First find the answer to the question, then just try to throw `.plot()` on the end
# >
# > **TIP:** You can use `.head()` on *anything*, not just your basic `df`
# >
# > **TIP:** You might feel like you should use `groupby`, but don't! There's an easier way to count.
# >
# > **TIP:** Make the largest bar be at the top of the graph
# >
# > **TIP:** If your chart seems... weird, think about where in the process you're sorting vs using `head`

# In[9]:


#pd.set_option("display.max_columns", 200)
#print(df)


# In[10]:


df.company.value_counts().sort_values(ascending=False).head(5).sort_values().plot(kind="barh")


# ## 7) How much money do these billionaires have in total?

# In[11]:


billionaire_wealth = df.networthusbillion.sum() * 1000000000
print(f'Together, they have ${billionaire_wealth:,.2f}')


# ## 8) What are the top 10 countries with the most money held by billionaires?
# 
# I am **not** asking which country has the most billionaires - this is **total amount of money per country.**
# 
# > **TIP:** Think about it in steps - "I want them organized by country," "I want their net worth," "I want to add it all up," and "I want 10 of them." Just chain it all together.

# In[12]:


print("Here are the top 10 countries in cumulative wealth of billionaires (in billions):")
df.groupby('countrycode').networthusbillion.sum().sort_values(ascending = False).head(10)


# ## 9) How old is an average billionaire? How old are self-made billionaires  vs. non self-made billionaires? 

# In[13]:


print("The average billionaire's age is", df.age.mean().round(1), "years old")


# In[14]:


print("The average self-made billionaire is", df[df.selfmade == "self-made"].age.mean().round(1), "years old")
print("The average non-self-made billionaire is", df[df.selfmade != "self-made"].age.mean().round(1), "years old")


# ## 10) Who are the youngest billionaires? Who are the oldest? Make a graph of the distribution of ages.
# 
# > **TIP:** You use `.plot()` to graph values in a column independently, but `.hist()` to draw a [histogram](https://www.mathsisfun.com/data/histograms.html) of the distribution of their values

# In[15]:


print("Age Distribution of Billionaires:")
df.age.hist(bins =100)


# ## 11) Make a scatterplot of net worth compared to age

# In[16]:


df.plot(
    x='networthusbillion', 
    y='age',
    kind='scatter')


# ## 13) Make a bar graph of the wealth of the top 10 richest billionaires
# 
# > **TIP:** When you make your plot, you'll need to set the `x` and `y` or else your chart will look _crazy_
# >
# > **TIP:** x and y might be the opposite of what you expect them to be

# In[17]:


df.sort_values(by='networthusbillion', ascending=True)     .tail(10)     .plot(
        x='name', 
        y='networthusbillion',
        kind='barh',
        )


# In[ ]:





# In[ ]:




