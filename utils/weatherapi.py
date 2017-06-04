from weather import Weather

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