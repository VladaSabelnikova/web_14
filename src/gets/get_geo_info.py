from get_country import get_country
from get_coord import get_coordinates


def get_geo_info(city_name, type_info):
    output = None
    if type_info == 'country':
        output = get_country(city_name)
    elif type_info == 'coordinates':
        output = get_coordinates(city_name)

    return output
