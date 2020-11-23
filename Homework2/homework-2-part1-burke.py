#Shane Burke
#Oct 28, 2020
#Homework 2, Part 1

print(f'----- Part One: Lists -----')
numbers = [22, 90, 0, -10, 3, 22, 48]

#To save a list sorted in a descending order for later use
numbers_descending = (sorted(numbers, reverse=True))

print(f'Here are our numbers: {numbers}')
print(f'We have {len(numbers)} numbers.')
print(f'The fourth number is {numbers[3]}.')
print(f'The sum of the second and fourth elements is {numbers[1] + numbers[3]}.')
print(f'The second largest value is {numbers_descending[1]}.')
print(f'The last element is {numbers[-1]}.')
print(f'Sum of all divided by 2: {sum(numbers)/2}.')

#Calculating the median: 
#If even, the average of the two middle numbers, found with len and len +1. 
#If odd, just the middle number's value, found by the lengh divided by 2, rounded up.
if len(numbers) % 2 == 0 :
    median = (numbers_descending[int((((len(numbers_descending))/2)))] + numbers_descending[int(((len(numbers_descending))/2)+1)]) /2
else:
    median = numbers_descending[round((len(numbers_descending))/2)]

#Calculating the mean: sum of numbers over number count
mean = sum(numbers)/len(numbers)

#Mean and median comparison statements
if median > mean:
    print(f'The median of {median} is higher than the mean of {mean}.')
elif median == mean:
    print(f'The median and the mean both {median}.')
elif median < mean:
    print(f'The mean of {mean} is higher than the median of {median}.')

#----------------------------------------------------------------------------

print(f'----- Part Two: Dictionaries -----')

print("--- a) Movies:")
movie = {
    'title': 'Paris is Burning',
    'year' : 1990,
    'director' : 'Jennie Livingston' }

print("My favorite movie is",movie['title'], "which was released in", movie['year'], "and was directed by", movie['director']+".")

movie['budget']= 500000
movie['revenue'] = 3779620
difference = abs(movie['revenue'] - movie['budget'])

if movie['budget'] > movie['revenue'] :
    print(f'The movie budget was {difference:,} dollars higher than the revenue.')
elif movie['budget'] < movie['revenue'] :
    print(f'The movie revenue was {difference:,} dollars higher than the budget.')
elif movie['budget'] == movie['revenue'] :
    print(f'The movie revenue was the same as the budget.')

if movie['budget'] > movie['revenue'] :
    print(f'That was a bad investment.')
elif movie['revenue'] > (5 * (movie['budget'])) :
    print(f'That was a great investment.')
else:
    print(f'That was an okay investment.')

print("--- b) NYC:")

nyc_boroughs = {
    'Bronx' : 1.4,
    'Brooklyn' : 2.6,
    'Manhattan' : 1.6,
    'Queens' : 2.3,
    'Staten Island' : .47
}

print("The population of Brooklyn is", nyc_boroughs['Brooklyn'], "million.")
print("The population of all five boroughs is", sum(nyc_boroughs.values()), "million.")
print(round((nyc_boroughs['Manhattan']/sum(nyc_boroughs.values())) * 100), "percent of NYC's population lives in Manhattan.")




