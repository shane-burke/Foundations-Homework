#!/usr/bin/env python
# coding: utf-8

# # Texas Licenses
# 
# I originally got this dataset from the [License Files page](https://www.license.state.tx.us/licensesearch/licfile.asp) from the Texas Department of Licensing and Regulation, but they've changed around since then! I'm pretty sure it's [this dataset](https://www.opendatanetwork.com/dataset/data.texas.gov/7358-krk7), but we'll just use a local version instead of the most current.

# # PART ONE: OPENING UP OUR DATASET

# ## 0. Do your setup
# 
# Import what you need to import, etc.

# In[1]:


import pandas as pd
from pprintpp import pprint as pp
import numpy as np 


# ## 1. Open the file
# 
# We'll start with `licfile.csv`, which is a list of licenses.

# In[2]:


df = pd.read_csv("licfile.csv")
df.head()


# ## 2. That looks terrible, let's add column names.
# 
# It apparently doesn't have headers! **Read the file in again, but setting your own column names**. Their [current data dictionary might not perfectly match](https://www.opendatanetwork.com/dataset/data.texas.gov/7358-krk7), but you can use it to understand what the columns are. For the dataset we're using, the order goes like this:
# 
# * LICTYPE
# * LICNUMBER
# * BIZCOUNTY
# * BIZNAME
# * BIZLINE1
# * BIZLINE2
# * BIZCITYSTATE
# * BIZTELEPHONE
# * EXPIRATION
# * OWNER
# * MAILLINE1
# * MAILLINE2
# * MAILCITYSTATE
# * MAILCOUNTYCODE
# * MAILCOUNTY
# * MAILZIP
# * TELEPHONE
# * LICSUBTYPE
# * CEFLAG
# 
# **Note:** You can rename the columns to things that make sense - "expiration" is a little more manageable than "LICENSE EXPIRATION DATE (MMDDCCYY)". I've named my License Type column LICTYPE, so if you haven't you'll have to change the rest of my sample code to match.

# In[3]:


columns = ['license_type', 
           'license_number', 
           'county', 
           'business_name', 
           'business_line1', 
           'business_line2', 
           'business_city_state',
           'business_telephone',
           'expiration', 
           'owner',
           'mail_line1',
           'mail_line2',
           'mail_city_state',
           'mail_county_code',
           'mail_county',
           'mail_zip',
           'phone',
           'license_subtype',
           'cont_ed_flag'
          ]

df = pd.read_csv("licfile.csv", names = columns)
df.tail(100)


# # 3. Force string columns to be strings
# 
# The county code and expiration dates are being read in as numbers, which is going to cause some trouble later on. You can force a column to be a certain type (most usually strings) when reading it in with the following code:
# 
#     df = pd.read_csv("your-filename.csv", dtype={"colname1": str, "colname2": str})
# 
# You don't need to do it for every column, just the ones you want to force!
# 
# **Re-import the file, forcing the expiration date, license number, mailing address county code, mailing zip code and telephone to all be strings.**

# In[4]:


df = pd.read_csv("licfile.csv", names = columns, dtype={"expiration": str, "license_number": str, "mail_county_code": str, "mail_zip": str, "phone": str})

df.head()


# Check the data types of your columns to be sure! If you do it right they'll be `object` (not `str`, oddly).

# In[5]:


df.dtypes


# ## 4. Convert those expiration dates from MMDDYYYY to YYYY-MM-DD
# 
# You can use list slicing with `.str` (we did `dt.per_name.str[:4]` for the home data stuff once), `pd.to_datetime`, or a hundred other methods.

# In[6]:


df.expiration[0][:4]

for i in df.expiration.head(5):
    df['year'] = i[4:]
    df['month'] = i[0:2]
    df['day'] = i[2:4]

df['expiration'] = df['year'] + "-" + df['month'] + "-" + df['day']

df.drop(['year', 'month', 'day'], axis=1)


# Check the first five expirations to make sure they look right.

# # PART TWO: LOOKING AT LICENSES

# ## 5. What are the top 10 most common licenses?

# In[7]:


df.value_counts('license_type').head(10)


# ## 6. What are the top 10 least common?

# In[8]:


df.value_counts('license_type').tail(10)


# ## 7. Try to select everyone who is any type of electrician.
# 
# You're going to get an error about `"cannot index with vector containing NA / NaN values"`. Let's work our way in there.

# In[9]:


# Yes I know I left this in here, it's a learning experience!
#df[df['license_type']].str.contains("Electrician")


# ## 8. How many of the rows of LICTYPE are NaN?

# In[10]:


df['license_type'].str.contains("Electrician").value_counts(dropna=False)
#7086 NaNs


# Over 7000 licenses don't have types! As a result, when we look for license types with electricians - aka do `df['LICTYPE'].str.contains("Electrician")` - we get three results:
# 
# * `True` means `LICTYPE` exists and contains `"Electrician"`
# * `False` means `LICTYPE` exists and does not contain `"Electrician"`
# * `NaN` means `LICTYPE` does not exist for that row

# ## 9. Actually getting everyone who is an electrician

# In[11]:


df[df.license_type.str.contains("Electrician").fillna(False)]


# This doesn't work when trying to select electricians, though, as NaN is a no-go for a filter. We *could* filter out everywhere the LICTYPE is null, but we could also cheat a little and say "replace all of the `NaN` values with `False` values."
# 
# `.fillna(False)` will take every `NaN` and replace it with `False`. 

# In[12]:


#used this above


# ## 10. What's the most popular kind of electrician?

# In[13]:


electricians = df[df.license_type.str.contains("Electrician").fillna(False)]

electricians.license_type.mode()


# ## 11. Graph it, with the largest bar on top.

# In[14]:


electricians.license_type.value_counts().sort_values(ascending=True).plot(kind='barh')


# ## 12. How many sign electricians are there?
# 
# There are a few ways to do this one.

# In[15]:


sign_electricians = df[df.license_type.str.contains("Sign Electrician").fillna(False)]
#sign_electricians
sign_electrician_number = len(sign_electricians)

print(f'There are {sign_electrician_number:,} sign electricians.')


# # PART THREE: LOOKING AT LAST NAMES

# ## 13. Extract every owner's last name
# 
# You want everything before the comma. We've done this before (in a few different ways!).
# 
# * **Hint:** If you get an error about missing or `NaN` data, you might use `.fillna('')` to replace every empty owner name with an empty string. This might not happen to you, though, depending on how you do it!
# 
# * **Hint:** You probably want to do `expand=False` on your extraction to make sure it comes out as a series instead of a dataframe.

# In[16]:


df.owner.fillna('').str.extract("^(\w+),", expand=False)


# ## 14. Save the last name into a new column
# 
# Then check to make sure it exists, and you successfully saved it into the dataframe.

# In[17]:


df['lastname'] = df.owner.fillna('').str.extract("^(\w+\W?.{0,10}?),", expand=False)


# In[18]:


df


# # 15. What are the ten most popular last names?

# In[19]:


df['lastname'].value_counts().head(10)


# ## 16. What are the most popular licenses for people with the last name Nguyen? Tran? Le?
# 
# Those are the top 3 last names in Vietnam.

# In[20]:


df[(df.lastname == "NGUYEN") | (df.lastname == "TRAN") | (df.lastname == "LE")].license_type.value_counts()


# In[21]:


print("The most popular licenses for people with these last names are cosmetology-related.")


# The background of this [is interesting](https://www.npr.org/2019/05/19/724452398/how-vietnamese-americans-took-over-the-nails-business-a-documentary) and [tragic](https://www.nytimes.com/2015/05/10/nyregion/at-nail-salons-in-nyc-manicurists-are-underpaid-and-unprotected.html).

# ## 17. Now do all of that in one line - most popular licenses for Nguyen, Tran and Le - without using `&`

# In[22]:


#I might have done this the first time
df[(df.lastname == "NGUYEN") | (df.lastname == "TRAN") | (df.lastname == "LE")].license_type.value_counts()


# ## 19. Most popular license for anyone with a last name that ENDS in `-ko`
# 
# The answer is not `.str.contains('ko')`, but it isn't necessarily too different.
# 
# * One way involves a `.str.` method that check if a string ends with something,
# * the other way involves a regular expression that has a "end of the string" marker (similar to how we've used `^` for the start of a string before)
# 
# If you're thinking about the latter, I might take a look at [this page](http://www.rexegg.com/regex-quickstart.html) under "Anchors and Boundaries". 

# In[23]:


df[df.lastname.str.contains("KO$").fillna(False)].license_type.mode()


# .#### 20. Get that as a percentage

# In[24]:


df[df.lastname.str.contains("KO$").fillna(False)].license_type.value_counts(normalize=True).head(1) * 100


# # PART FOUR: LOOKING AT FIRST NAMES

# ## 21. Extract the owner's first name
# 
# First, a little example of how regular expressions work with pandas.

# In[25]:


# Build a dataframe
sample_df = pd.DataFrame([
    { 'name': 'Mary', 'sentence': "I am 90 years old" },
    { 'name': 'Jack', 'sentence': "I am 4 years old" },
    { 'name': 'Anne', 'sentence': "I am 27 years old" },
    { 'name': 'Joel', 'sentence': "I am 13 years old" },
])
# Look at the dataframe
sample_df


# In[26]:


# Given the sentence, "I am X years old", extract digits from the middle using ()
# Anything you put in () will be saved as an output.
# If you do expand=True it makes you a dataframe, but we don't want that.
sample_df['sentence'].str.extract("I am (\d+) years old", expand=False)


# In[27]:


# Save it into a new column
sample_df['age'] = sample_df['sentence'].str.extract("I am (\d+) years old", expand=False)
sample_df.head()


# **Now let's think about how we're going to extract the first names.** Begin by looking at a few full names.

# In[28]:


df['owner'].head(10)


# What can you use to find the first name? It helps to say "this is to the left and this is to the right, and I'm going to take anything in the middle."
# 
# Once you figure out how to extract it, you can do a `.head(10)` to just look at the first few.

# In[29]:


df.owner.str.extract("^\w+, (\w+)").head(10)


# ## 22. Saving the owner's first name
# 
# Save the name to a new column, `FIRSTNAME`.

# In[30]:


df['firstname'] = df.owner.str.extract("^\w+, (\w+)")
#df


# # 23. Examine everyone without a first name
# 
# I purposefully didn't do a nicer regex in order to have some screwed-up results. **How many people are there without an entry in the first name column?**
# 
# Your numbers might be different than mine.

# In[31]:


df.firstname.value_counts(dropna=False)


print("105,055 people... yikes.")


# What do their names look like?

# In[32]:


# They're NaN values with some sort of space or character in the name.
# I found a lot of names like De ___, O'____, St ____, La ____, etc as nulls in the last names through this too.
# I changed my original last name regex to include them.
#df[df.firstname.isna()]

#So I reset it:
#df['firstname'] = df.owner.str.extract("^\w+\W?.{0,30}?, (\w+)")

#But then anything with strange spacing on the commas in the "owner" column or with a company name as the owner name did not fit.
#for instance names like "Lowery,Mark" or "Lastname ,Firstname"
#So I added a space before and after the comma with a ? after to get these people

df['firstname'] = df.owner.str.extract("^\w+\W?.{0,30}? ?, ?(\w+)")

#Now it's just companies with a business name in the owner column

df[df.firstname.isna()]


# ## 24. If it's a problem, you can fix it (if you'd like!)
# 
# Maybe you have another regular expression that works better with JUST these people? It really depends on how you've put together your previous regex!
# 
# If you'd like to use a separate regex for this group, you can use code like this:
# 
# `df.loc[df.FIRSTNAME.isnull(), 'FIRSTNAME'] = .....`
# 
# That will only set the `FIRSTNAME` for people where `FIRSTNAME` is null.

# In[33]:


df.loc[df.firstname.isnull(), 'firstname'] = "unknown"

#Testing with one of the nas from above
#df[df.owner == "BALLARD COMPANY"]


# How many empty first names do we have now?

# In[34]:


print(len(df[df.firstname == "unknown"]), "empty names. :(")


# My code before only worked for people with middle names, but now it got people without middle names, too. Looking much better!

# ## 25. Most popular first names?

# In[35]:


df.firstname = df.firstname.replace({"unknown": np.nan})

print("---Top 10 First Names, Percentage of Total First Names---")
df.firstname.value_counts(normalize=True).head(10)*100



# ## 26. Most popular first names for a Cosmetology Operator, Cosmetology Esthetician, Cosmetologist, and anything that seems similar?
# 
# If you get an error about "cannot index vector containing NA / NaN values" remember `.fillna(False)` or `na=False` - if a row doesn't have a license, it doesn't give a `True`/`False`, so we force all of the empty rows to be `False`.

# In[36]:


print("---Top 10 Cosmetological License Holder Names (%)---")
df[df.license_type.str.contains("Cosm").fillna(False)].firstname.value_counts(normalize=True).head(10)*100


# ## 27. Most popular first names for anything involving electricity?

# In[37]:


print("---Top 10 Electrical License Holder Names (%)---")
df[df.license_type.str.contains("Electric").fillna(False)].firstname.value_counts(normalize=True).head(10)*100


# ## 28. Can we be any more obnoxious in this assignment?
# 
# A terrible thing that data analysts are often guilty of is using names to make assumptions about people. Beyond stereotypes involving last names, first names are often used to predict someone's race, ethnic background, or gender.
# 
# And if that isn't bad enough: if we were looking for Python libraries to do this sort of analysis, we'd come across [sex machine](https://github.com/ferhatelmas/sexmachine/). Once upon a time there was Ruby package named sex machine and everyone was like "come on are you six years old? is this how we do things?" and the guy was like "you're completely right I'm renaming it to [gender detector](https://github.com/bmuller/gender_detector)" and the world was Nice and Good again.
# 
# How'd it happen? [On Github, in a pull request!](https://github.com/bmuller/gender_detector/pull/14) Neat, right?
# 
# But yeah: apparently Python didn't get the message.
# 
# The sexmachine package doesn't work on Python 3 because it's from 300 BC, so we're going to use a Python 3 fork with the less problematic name [gender guesser](https://pypi.python.org/pypi/gender-guesser/).
# 
# #### Use `pip` or `pip3` to install gender-guesser.

# In[38]:


get_ipython().system('pip install gender-guesser')


# #### Run this code to test to see that it works

# In[39]:


import gender_guesser.detector as gender

detector = gender.Detector(case_sensitive=False)
detector.get_gender('David')


# In[40]:


detector.get_gender('Jose')


# In[41]:


detector.get_gender('Maria')


# #### Use it on a dataframe
# 
# To use something fancy like that on a dataframe, you use `.apply`. Check it out: 

# In[42]:


df['firstname'].fillna('').apply(lambda name: detector.get_gender(name)).head(20)


# ## 29. Calculate the gender of everyone's first name and save it to a column
# 
# Confirm by see how many people of each gender we have

# In[43]:


df['gender_guess'] = df['firstname'].fillna('').apply(lambda name: detector.get_gender(name))


# In[44]:


df.gender_guess.value_counts()


# ## 30. We like our data to be in tidy binary categories
# 
# * Combine the `mostly_female` into `female` 
# * Combine the `mostly_male` into `male`
# * Replace `andy` (androgynous) and `unknown` with `NaN`
# 
# you can get NaN not by making a string, but with `import numpy as np` and then using `np.nan`.

# In[45]:


import numpy as np

df.gender_guess = df.gender_guess.replace({
    'mostly_male': 'male',
    'mostly_female': 'female',
    'andy': np.nan,
    'unknown': np.nan
})

df.gender_guess.value_counts(dropna=False)


# ## 31. Do men or women have more licenses? What is the percentage of unknown genders?

# In[46]:


male_number = len(df[df.gender_guess == "male"])
female_number = len(df[df.gender_guess == "feale"])

if male_number > female_number:
    print("There are more men with licenses than women.")
elif male_number < female_number:
    print("There are more women with licenses than men")
else:
    print("There are the same amount of men and women with licenses.")


# In[47]:


df.gender_guess.value_counts(dropna=False, normalize=True)*100

#25.3% of genders in the set are unknown.


# ## 32. What are the popular unknown- or ambiguous gender first names?
# 
# Yours might be different! Mine is a combination of actual ambiguity, cultural bias and dirty data.

# In[48]:


df[df.gender_guess.isna()].firstname.value_counts().head(20)
#Tranh, Trang, Inc, Hong, Dung, Linh, Lan, LLC, Yen, Hang, Hung, Chau, etc.
#This is mostly cultural bias, but also dirty data (LLC and Inc) and some actual ambiguity


# ## 33. Manually check a few, too 
# 
# Using [a list of "gender-neutral baby names"](https://www.popsugar.com/family/Gender-Neutral-Baby-Names-34485564), pick a few names and check what results the library gives you.

# In[49]:


gender_neutral_names = ["Cameron", "Campbell", "Carey", "Casey", "Cassidy", "Charlie", "Chris", "Dakota", "Dale"]

for name in gender_neutral_names:
    print(name)
    print(detector.get_gender(name))
    print("~*~")


# ## 34. What are the most popular licenses for men? For women?

# In[50]:


print("Top Men's License Types")
df[df.gender_guess == "male"].license_type.value_counts().head()


# In[51]:


print("Top Women's License Types")
df[df.gender_guess == "female"].license_type.value_counts().head()


# ## 35. What is the gender breakdown for Property Tax Appraiser? How about anything involving Tow Trucks?
# 
# If you're in need, remember your good friend `.fillna(False)` to get rid of NaN values, or `.na=False` with `.str.contains`.

# In[52]:


print("Gender Breakdown of Property Tax Appraisers (%)")
df[df.license_type == "Property Tax Appraiser"].gender_guess.value_counts(normalize=True)


# In[53]:


print("Gender Breakdown of Tow Truckers (%)")
df[df.license_type.str.contains("Tow").fillna(False)].gender_guess.value_counts(normalize=True)


# (By the way, what are those tow truck jobs?)

# In[54]:


df[df.license_type.str.contains("Tow").fillna(False)].license_type


# ## 33. Graph them!
# 
# And let's **give them titles** so we know which is which.

# In[55]:


print("   --- Tow Truck Operators by Gender, Percent   ---   ")
df[df.license_type.str.contains("Tow").fillna(False)].gender_guess.value_counts(normalize=True).plot(kind='barh')


# In[56]:


print("   ---   Property Tax Appraiser Breakdown by Gender, Percent   ---   ")
df[df.license_type == "Property Tax Appraiser"].gender_guess.value_counts(normalize=True).plot(kind='barh')


# ## 34. Calcuate the supposed gender bias for profession
# 
# I spent like an hour on this and then realized a super easy way to do it. Welcome to programming! I'll do this part for you.

# In[57]:


# So when you do .value_counts(), it gives you an index and a value
df[df['gender_guess'] == 'male'].license_type.value_counts().head()


# We did `pd.concat` to combine dataframes, but you can also use it to combine series (like the results of `value_counts()`). If you give it a few `value_counts()` and give it some column names it'll make something real nice.

# In[58]:


# All of the values_counts() we will be combining
vc_series = [
    df[df['gender_guess'] == 'male'].license_type.value_counts(),
    df[df['gender_guess'] == 'female'].license_type.value_counts(),
    df[df['gender_guess'].isnull()].license_type.value_counts()
]
# You need axis=1 so it combines them as columns
gender_df = pd.concat(vc_series, axis=1)
gender_df.head()


# In[59]:


# Turn "A/C Contractor" etc into an actual column instead of an index
gender_df.reset_index(inplace=True)
gender_df.head()


# In[60]:


# Rename the columns appropriately
gender_df.columns = ["license", "male", "female", "unknown"]
# Clean up the NaN by replacing them with zeroes
gender_df.fillna(0, inplace=True)
gender_df.head()


# ## 35. Add new columns for total licenses, percent known (not percent unknown!), percent male (of known), percent female (of known)
# 
# And replace any `NaN`s with `0`.

# In[61]:


gender_df['total_licenses'] = gender_df.male + gender_df.female + gender_df.unknown
gender_df['pct_known'] = (gender_df.male + gender_df.female) / gender_df.total_licenses * 100
gender_df['male_of_known'] = gender_df.male / (gender_df.male + gender_df.female) * 100
gender_df['female_of_known'] = gender_df.female / (gender_df.male + gender_df.female) * 100

gender_df.head()


# ## 35. What 10 licenses with more than 2,000 people and over 75% "known" gender has the most male owners? The most female?

# In[62]:


print("Most Male License-Holders Of Selected Licenses")
gender_df[(gender_df.total_licenses > 2000) * (gender_df.pct_known > 75)].sort_values(by='male_of_known', ascending=False).head(10)


# In[63]:


print("Most Female License-Holders Of Selected Licenses")
gender_df[(gender_df.total_licenses > 2000) * (gender_df.pct_known > 75)].sort_values(by='female_of_known', ascending=False).head(10)


# ## 36. Let's say you have to call a few people about being in a profession dominated by the other gender. What are their phone numbers?
# 
# This will involve doing some research in one dataframe, then the other one. I didn't put an answer here because I'm interested in what you come up with!

# In[64]:


#Pulling numbers from the following:
df[(df.license_type == "Cosmetology Esthetician") & (df.gender_guess == "male")]
#df[(df.license_type == "Master Electrician") & (df.gender_guess == "female")]


# In[65]:


#Calling Kathy Sue the electrician 9036543921
#and Derek Berlin the Esthetician 2104955958


# ## Okay, let's take a break for a second.
# 
# We've been diving pretty deep into this gender stuff after an initial "oh but it's not great" kind of thing.
# 
# **What issues might come up with our analysis?** Some might be about ethics or discrimination, while some might be about our analysis being misleading or wrong. Go back and take a critical look at what we've done since we started working on gender, and summarize your thoughts below.

# In[66]:


#Cultural bias/misunderstanding: Gender guesser thinks "Kim" is a female name, but a lot of the time, it's Korean. 
#There are a lot of ways gender guessing fails. It does not seem to understand many names across cultures.

#Trans and nonbinary people: They might be misgendered based on a proxy like this. 
#Nonbinary/gender non-conforming people excluded altogether as unknown

#The huge amount of unknowns
#We can't just assume the unknown gender breakdown is representative of the rest. It might throw off our sample.

#Need to look more into the data: As you mentioned before, there are reasons that so many people with Vietnamese surnames are in cosmetology. 
#The same goes for gender and professions. The gender breakdown of any profession is not devoid of the cultural and gender context of society.


# If you found problems with our analysis, **how could we make improvements?**

# In[67]:


#With this data, I'm not really sure. To cover cultural biases, we could improve the dictionary for gender-gueser.
#I looked at some documentation, and maybe specifying the country where those names are most popular would help with this. 
#They do that like "print(d.get_gender(u"Jamie", u'great_britain'))" at https://pypi.org/project/gender-guesser/
#We could also note the margin of error that gender guesser typically has, to warn people in our analysis that there are discrepancies.


# In[ ]:





# ## PART FIVE: Violations
# 
# ### 37. Read in **violations.csv** as `violations_df`, make sure it looks right

# In[68]:


violations_df = pd.read_csv("violations.csv")
violations_df.head()


# ### 38. Combine with your original licenses dataset dataframe to get phone numbers and addresses for each violation. Check that it is 90 rows, 28 columns.

# In[69]:


newdf = violations_df.merge(df, left_on='licenseno', right_on='license_number')


# In[70]:


#newdf.shape
newdf = newdf.drop(columns=['license_subtype', 'cont_ed_flag', 'year', 'month', 'day', 'gender_guess'])


# In[71]:


newdf.shape


# ## 39. Find each violation involving a failure with records. Use a regular expression.

# In[72]:


newdf[newdf.basis.str.contains("failed .* record")]


# ## 40. How much money was each fine? Use a regular expression and .str.extract
# 
# Unfortunately large and helpful troubleshooting tip: `$` means "end of a line" in regex, so `.extract` isn't going to accept it as a dollar sign. You need to escape it by using `\$` instead.

# In[73]:


newdf['fines'] = newdf.order.fillna('').str.extract("\$(\d+,?\d+,?\d+)")
newdf['fines']
#df.owner.fillna('').str.extract("^(\w+),", expand=False)


# ## 41. Clean those results (no commas, no dollar signs, and it should be an integer) and save it to a new column called `fine`
# 
# `.replace` is for *entire cells*, you're interested in `.str.replace`, which treats each value like a string, not like a... pandas thing.
# 
# `.astype(int)` will convert it into an integer for you.

# In[74]:


newdf['fines'] = newdf.fines.str.replace(",", "")
newdf['fines'] = newdf.fines.astype(int)

#newdf.order.fillna('').str.extract("(\$\d+,?\d+,?\d+)")


# ## 42. Which orders results in the top fines?

# In[75]:


newdf.groupby('order').fines.mean().sort_values(ascending=False).head(10)
#did order but it jsut seems to list fine amount. The "basis" also seemed unique to each value


# ## 43. Are you still here???
# 
# I'm sure impressed.

# In[ ]:




