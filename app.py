from os import listdir
from os.path import isfile, join
from tqdm import tqdm
import xmltodict
import math
import pprint

PATH = 'exoplanets/systems'

print("Find planet XMLs")
planets = [f for f in tqdm(listdir(PATH)) if isfile(join(PATH, f))]
           
print("Parsing Planet XML")

planet_dicts = []

for planet in tqdm(planets):
    planet_file = join(PATH, planet)
    with open(planet_file, 'r', encoding='utf-8') as file:
        planet_xml = file.read()
        planet_dict = xmltodict.parse(planet_xml)
    planet_dicts.append(planet_dict)

def calculate_temperature(mass, distance, albedo=29, greenhouse=1):
    # Borrowed from https://astro.sitehost.iu.edu/ala/PlanetTemp
    pi = math.pi
    sigma = 5.6703*pow(10, -5)
    L = 3.846*pow(10, 33)*pow(mass, 3)
    D = distance*1.496*pow(10, 13)
    A = albedo/100
    T = greenhouse*0.5841
    X = math.sqrt((1-A)*L/(16*pi*sigma))
    T_eff = math.sqrt(X)*(1/math.sqrt(D))
    T_eq = pow(T_eff, 4)*(1+(3*T/4))
    T_sur = T_eq/0.9
    T_kel = math.sqrt(math.sqrt(T_sur))
    T_kel = round(T_kel)
    celsius = T_kel-273
    return T_kel

habitable_planets = []

print("Calculating average temperature")
for planet in tqdm(planet_dicts):
    try:
        sun_mass = planet['system']['star']['mass']['#text']
    except Exception as e:
        sun_mass = None
    try:
        semi_major_axis = planet['system']['star']['planet']['semimajoraxis']['#text']
    except Exception as e:
        semi_major_axis = None
    try:
        planet_name = planet['system']['star']['planet']['name'][0]
    except Exception as e:
        planet_name = None
    temperature = None
    if sun_mass and semi_major_axis:
        temperature = calculate_temperature(float(sun_mass), float(semi_major_axis))
    if temperature and temperature > 278 and temperature < 313:
        habitable_planet = {
            "name": planet_name,
            "sun_mass": sun_mass,
            "semi_major_axis": semi_major_axis,
            "temp_k": temperature
        }
        habitable_planets.append(habitable_planet)

print(f"You found {len(habitable_planets)} habitable planets in a 5 to 40 degree range")
for hab_plan in habitable_planets:
    pprint.pprint(hab_plan, indent=2)
