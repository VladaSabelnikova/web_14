from get_country import get_country
from get_coord import get_coordinates
from typing import Union


def get_geo_info(
    city_name: str,
    type_info: str
) -> Union[str, Union[tuple[float, float], Exception, None]]:

    output = None
    if type_info == 'country':
        output = get_country(city_name)
    elif type_info == 'coordinates':
        output = get_coordinates(city_name)

    return output
