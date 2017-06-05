from weather import Weather

####################### BEGIN: model definition #######################
# REFERENCE: https://developer.yahoo.com/weather/?dataTypeRadios=JSON
class WeatherObject(object):
    def __init__(self, weather_data):
        self._weather_data = weather_data

    def last_build_date(self):
        return self._weather_data['lastBuildDate']

    def title(self):
        return self._weather_data['title']

    def description(self):
        return self._weather_data['description']

    def language(self):
        return self._weather_data['language']

    def astronomy(self):
        return self._weather_data['astronomy']

    def atmosphere(self):
        return self._weather_data['atmosphere']

    def image(self):
        return self._weather_data['image']

    def condition(self):
        return self._weather_data['item']['condition']

    def forecast(self):
        return self._weather_data['item']['forecast']

    def latitude(self):
        return self._weather_data['item']['lat']

    def longitude(self):
        return self._weather_data['item']['lng']

    def location(self):
        return self._weather_data['location']

    def units(self):
        return self._weather_data['units']

    def wind(self):
        return self._weather_data['wind']

    def print_obj(self):
        return self._weather_data

class Weather(object):
    URL = "http://query.yahooapis.com/v1/public/yql"

    def lookup_by_location(self, location):
        url = "%s?q=select* from weather.forecast " \
              "where woeid in (select woeid from geo.places(1) where text='%s')&format=json" % (self.URL, location)
        results = self._call(url)
        return results

    def _call(self, url):
        results = requests.get(url).json()
        if int(results['query']['count']) > 0:
            wo = WeatherObject(results['query']['results']['channel'])
            return wo
        else:
            print 'No results found.'

####################### END: model definition #######################

weather = Weather()

# lookup via location name
def get_weather_by_name(location_name):
    location = weather.lookup_by_location(location_name)
    # currently
    condi = location.condition()
    currently = {
    	"date": condi.get("date"),
    	"icon": condi.get("text", "").lower().replace(" ", "-"),
    	"temperature": condi.get("temp", -1),
    	"text": condi.get("text", ""),
    }
    # hourly
    hourly = {}
    # daily
    daily = {"data": location.forecast()[0:7]}
    for i, _ in enumerate(daily["data"]):
    	daily["data"][i]["icon"] = daily["data"][i].get("text", "").lower().replace(" ", "-")
    # put them together
    return {
    	"location": location.location(),
    	"currently": currently,
    	"hourly": hourly,
    	"daily": daily,
    	"units": location.units(),
    }

def fahrenheit2Celsius(f):
    return (f-32) * (5/9.0)