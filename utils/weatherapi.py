import requests

####################### BEGIN: model definition #######################
# REFERENCE: https://developer.yahoo.com/weather/?dataTypeRadios=JSON
class WeatherObject(object):
    def __init__(self, weather_data):
        self._weather_data = weather_data

    def last_build_date(self):
        return self._weather_data['lastBuildDate']

    def astronomy(self):
        return self._weather_data['astronomy']

    def atmosphere(self):
        return self._weather_data['atmosphere']

    def condition(self):
        return self._weather_data['item']['condition']

    def forecast(self):
        return self._weather_data['item']['forecast']

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

    def lookup_by_location(self, location, celsius=True):
        url = "%s?format=json&q=select* from weather.forecast " \
              "where woeid in (select woeid from geo.places(1) where text='%s')" % (self.URL, location)
        if celsius:
        	url = url + " and u='c'"
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
def get_weather_by_name(location_name, celsius=True):
    location = weather.lookup_by_location(location_name, celsius)
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