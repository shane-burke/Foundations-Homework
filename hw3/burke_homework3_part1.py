#Shane Burke
#November 2, 2020
#Homework 3

# pip install requests in Terminal
#code to install pretty printing from https://pypi.org/project/pprintpp/
# pip install pprintpp in Terminal
from pprintpp import pprint as pp
import requests
#print(data.keys())


#1.
print("The documentation can be found at: https://pokeapi.co/docs/v2#namedapiresource")
print('\n')

#2 and 3.
q1_pokemon = 55
url = f"https://pokeapi.co/api/v2/pokemon/{q1_pokemon}"
response = requests.get(url)
q1_data = response.json()
print("The pokemon with the ID number", q1_data['id'], "is", q1_data['name']+".")
print(q1_data['name'], "is", q1_data['height']/10, "meters tall.")

print("\n")
print("~*~*~*~*~*~")
print("\n")

#4.
id = 1
url = f"https://pokeapi.co/api/v2/version?offset=0&limit=100"
response = requests.get(url)
q4_data = response.json()
#pp(q4_data)

print("There are", q4_data['count'], "versions. They are:")

q4_test_list = list(range(1, 34))
for test in q4_test_list:
    print("---", (q4_data)['results'][test]['name'])
#Tested this out and 35 gave an error, as did 0, but this range does not.

print("\n")
print("~*~*~*~*~*~")
print("\n")

#5.
url = f"https://pokeapi.co/api/v2/type/13"
response = requests.get(url)
q5_data = response.json()
print("There are", len(q5_data['pokemon']), "electric type pokemon. They are:")
q5_list = list(range(1, len(q5_data['pokemon'])))
for electric_pokemon in q5_list:
    print("---", q5_data['pokemon'][electric_pokemon]['pokemon']['name'])

print("\n")
print("~*~*~*~*~*~")
print("\n")

#6. 
#I pretty printed pp(q5_data['names']) and saw the Korean name second in the list
print("In Korean, the electric pokemon are called", q5_data['names'][1]['name'])

print("\n")
print("~*~*~*~*~*~")
print("\n")

#7. 

pokemon = ['eevee', 'pikachu']
eevee = ['eevee']
pikachu = ['pikachu']

for pokemon_name in pokemon:
    #print(pokemon_name) 
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    response = requests.get(url, allow_redirects=True)
    data = response.json()
    #pp data.keys()
    #pp(data['stats'][5]['base_stat'])
    if pokemon_name == "eevee":
        eevee_speed = data['stats'][5]['base_stat']
    if pokemon_name == "pikachu":
        pikachu_speed = data['stats'][5]['base_stat']

if eevee_speed > pikachu_speed:
    print("Eevee has a higher speed stat (", eevee_speed, ") than Pikachu (", pikachu_speed, ").")
elif pikachu_speed > eevee_speed:
    print("Pikachu has a higher speed stat (", pikachu_speed, ") than Eevee (", eevee_speed, ").")
elif pikachu_speed == eevee_speed:
    print("Pikachu and Eevee have the same speed stat, at", pikachu_speed + ".")