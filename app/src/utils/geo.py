from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from typing import Tuple


class GeoParser:

    @staticmethod
    def get_geo_coordinates(town_name: str) -> Tuple:
        """ Return geographical coordinates.
        """
        geolocator = Nominatim(user_agent = "get_coordinates")
        location = geolocator.geocode(town_name)
        if location:
            return location.latitude, location.longitude
        return None
        

    @staticmethod
    def get_geo_distance(geo_point1: Tuple[str, str], geo_point2: Tuple[str, str]) -> float:
        """ Return distance in kilometers.
        """
        return geodesic(geo_point1, geo_point2).kilometers