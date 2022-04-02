from geopy import Nominatim
geolocator = Nominatim(user_agent="translator")
print(geolocator.geocode("73.24 18.46"))
