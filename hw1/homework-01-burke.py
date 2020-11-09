#Shane Burke
#October 26, 2020
#Homework 1

#Calculating age
yob = input("What year were you born?")
if int(yob) >= 2020:
    yob = input("So... when were you actually born?")
yob = int(yob)
age = 2020 - yob

#Calculating heartbeats with avg rate of 80 per minute
heartbeats = 80 * 60 * 24 * 365 * age

#Calculating blue whale heartbeats. It ranges from 2 to 37, but usually it's resting. Let's say an avg of 8 bpm compared to humans' 80.
bluewhale_heartbeats = heartbeats * (8/80)

#Rabbit beats - 140 to 180 bpm, we'll use 160.
rabbit_heartbeats = heartbeats * (160/80)

#Venus age, based on 225 days for an orbit around the sun
venus_age = age * (365/225)

#Neptune age, based on 60,190 days for an orbit around the sun
neptune_age = age * (365/60190)

#My age and age comparison
shane_age=26
if age > shane_age:
    compare_age = "older than"
    age_diff = abs(age - shane_age)
elif age == shane_age:
    compare_age = "the same age as"
    age_diff = abs(age - shane_age)
elif age < shane_age:
    compare_age = "younger than"
    age_diff = abs(age - shane_age)

#Democratic presidents since 1960: setting up a dictionary with nested variables for party, start, and end year
presidents = {
    'Dwight Eisenhower' : {
        'party' : 'R',
        'startyear' : 1953,
        'endyear' : 1960 },
    'John F. Kennedy' : {
        'party' : 'D',
        'startyear' : 1961,
        'endyear' : 1963, },
    'Lyndon B. Johnson' : {
        'party' : 'D',
        'startyear' : 1964,
        'endyear' : 1968 },
    'Richard Nixon' : {
        'party' : 'R',
        'startyear' : 1969,
        'endyear' : 1974 },
    'Gerald Ford' : {
        'party' : 'R',
        'startyear' : 1975,
        'endyear' : 1976 } ,
    'Jimmy Carter' : {
        'party' : 'D',
        'startyear' : 1977,
        'endyear' : 1980 },   
    'Ronald Reagan' : {
        'party' : 'R',
        'startyear' : 1981,
        'endyear' : 1988 },   
    'George H.W. Bush' : {
        'party' : 'R',
        'startyear' : 1989,
        'endyear' : 1992 },   
    'Bill Clinton' : {
        'party' : 'D',
        'startyear' : 1993,
        'endyear' : 2000 }, 
    'George W. Bush' : {
        'party' : 'R',
        'startyear' : 2001,
        'endyear' : 2008 }, 
    'Barack Obama' : {
        'party' : 'D',
        'startyear' : 2008,
        'endyear' : 2016 } , 
    'Donald Trump' : {
        'party' : 'R',
        'startyear' : 2016,
        'endyear' : 2020 } 
    }

#Calculating democratic presidents since yob. Incrementally adding if YOB is less than or equal to the last year of a president's term AND the president's party is democrat.
dem_presidents = 0
for key, value in presidents.items():
    if yob <= value['endyear'] and value['party'] == 'D':
        dem_presidents = dem_presidents+1

#Figuring out the president at year of birth with a for loop to test which start and end years YOB is between.
for key, value in presidents.items():
    if yob >= value['startyear'] and yob <= value['endyear']:
        president_yob = key

#Now to print out our story
print(f'You are {age} years old.')
print(f'Your heart has beaten approximately {heartbeats:,} times.')
print(f'A blue whale heart has beaten approximately {bluewhale_heartbeats:,.0f} times since you were born.')
print(f'A rabbit heart has beaten approximately {rabbit_heartbeats/1000000:,.1f} million times since you were born.')
print(f'You would be around {venus_age:.2f} years old on Venus and {neptune_age:.2f} years old on Neptune.')
if age_diff >0:
    print(f'You are {compare_age} me by {age_diff} years.')
elif age_diff == 0:
    print(f'You are {compare_age} me.')
if yob % 2 == 0:
    print(f'You were born in an even year.')
elif yob % 1 == 0:
    print(f'You were born in an odd year.')

print(f'There have been {dem_presidents} democratic presidents since you were born.')

print(f'The president when you were born was {president_yob}.')

