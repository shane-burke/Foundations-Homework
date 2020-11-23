#Shane Burke
#October 28, 2020
#Homework 2, Part 2

print("~*~*~*~ Part Two: Lists *~*~*~*")

countries = ['Ireland', 'Canada', 'Brazil', 'Zimbabwe', 'Australia', 'Japan', 'Nepal']

#For loop printing each element of the list
for country in countries:
    print(country)

#Sorting countries alphabetically and printing to test
countries.sort()
print(countries)

#Display first element
print(countries[0])

#Display second to last
print(countries[-2])

#Removing Australia
countries.remove('Australia')
print(countries)

#Uppercase remaining countries
for country in countries:
    print(f'{country.upper()}')

print("-")
print("-")
print("~*~*~*~ Part Two: Dictionaries *~*~*~*")
tree = { 'name' : 'Post Office Tree',
       'species' : 'Sideroxylon inerme',
       'age' : 600 ,
       'location_name' : 'Mosselbay, South Africa', 
       'latitude' : -34.180363 ,
       'longitude' : 22.141382 }
#made latitude negative because it is south of the equator

print(tree['name'], "is a", tree['age'], "year old tree that is in", tree['location_name'] +".")

if tree['latitude'] < 40.7128:
    print("The", tree['name'], "in", tree['location_name'], "is south of NYC.")
elif tree['latitude'] > 40.7128:
    print("The", tree['name'], "in", tree['location_name'], "is north of NYC.")
elif tree['latitude'] == 40.7128:
    print("The", tree['name'], "in", tree['location_name'], "is at the same latitude as NYC.")

user_age = int(input("How old are you?"))
if user_age > tree['age']:
    print("You are", (user_age - tree['age']), "older than", tree['name']+".")
elif user_age < tree['age']:
    print(tree['name'], "was", (tree['age'] - user_age), "years old when you were born.")
else:
    print("You are the same age as", tree['name']+".")

print("-")
print("-")
print("~*~*~*~ Part Two: Lists of Dictionaries *~*~*~*")

places = [{'name' : 'Moscow', 'latitude' : 55.7558, 'longitude' : 37.6173 },
{'name' : 'Tehran', 'latitude' : 35.6892, 'longitude' : 51.3890},
{'name' : 'Falkland Islands', 'latitude' : -51.7963, 'longitude' : -59.5236 },
{'name' : 'Seoul', 'latitude' : 37.5665, 'longitude' : 126.978},
{'name' : 'Santiago', 'latitude' : -33.4489 , 'longitude' : -70.6693}]

#Comparing to equator with a for loop calling the dictionary values
for city in places:
    if city['latitude'] > 0:
        print(city['name'], "is north of the equator.")
    elif city['latitude'] < 0:
        print(city['name'], "is south of the equator.")
    else:
        print(city['name'], "is on the equator.")
    if city['name'] == 'Falkland Islands':
        print("The Falkland Islands are a biogeographical part of the mild Antarctic zone.")

#Comparing to post office tree
for city in places:
    if city['latitude'] > tree['latitude']:
        print(city['name'], "is north of", tree['name']+".")
    elif city['latitude'] < tree['latitude']:
        print(city['name'], "is south of", tree['name']+".")
    else:
        print(city['name'], "is at the same latitude as tree['name'].")

