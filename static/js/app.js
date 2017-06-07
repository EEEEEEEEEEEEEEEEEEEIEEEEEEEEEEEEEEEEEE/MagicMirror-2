(function() {

	$(document).ready(function() {

		var monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

		// Fade in once weather loads
		$('.container').hide();

		// TIME
		function checkTime(i) {
			return (i < 10) ? "0" + i : i;
    	}

	    function startTime() {
	    	var today, h, h_mod, m, s, am_pm;

			today = new Date();
			h = checkTime(today.getHours());
			m = checkTime(today.getMinutes());
			s = checkTime(today.getSeconds());

			am_pm = h < 12 ? 'am' : 'pm';
			h_mod = h < 12 ? h : h - 12;

			if (h == 0) {
				h_mod = 12;      	
			} else if (h < 12) {
				h_mod = h;
			} else {
				h_mom = h - 12;
			}

			$(".full-date").html(monthNames[today.getMonth()] + " " + today.getDate());
			$(".timer-hour").html(h_mod);
			$(".timer-min").html(m);
			$(".timer-suffix").html(am_pm);
			t = setTimeout(function () {
					startTime()
				}, 500);
	    }

	    // WEATHER
	    function getWeather() {
			$.get("/get_weather", function (data) {
				formatWeather(data);
				$('.container').fadeIn(1500);
			});
		}

		function formatWeather(weather) {
			var days = ['Sun', 'Mon', 'Tu', 'Wed', 'Th', 'Fri', 'Sat'];			
			var dayOfWeek = new Date().getDay();
			var arrangedDays = (days.splice(dayOfWeek)).concat(days);

			// current weather
			$('.current-temp').html(Math.round(weather.currently.temperature));
			$('.current-temp-units').addClass(weatherIcons[weather.units.temperature]);
			$('.current-weather-icon').addClass(weatherIcons[weather.currently.icon]);
			$('.current-weather-text').html(weather.currently.text);
			console.log(weather.currently.text)
			//$('.prob-rain').html(Math.round(weather.daily.data[0].precipProbability * 100));

			console.log(weather);
			// hourly change weather
			/*
			for (var j = 1; j <= 12; j+=3) {
				var time = new Date(weather.hourly.data[j].time * 1000);
				var hour = time.getHours();

				if (hour > 12) {
					hour = hour - 12 + 'PM';
				} else if (hour === 0) {
					hour = 12 + 'AM';
				} else {
					hour += 'AM';
				}

				$('.hourly-change-container').append("<div class='hourly-change'></div>");
				$('.hourly-change').last().append("<span class='hourly-change-label'>" + hour + " </span>");
				$('.hourly-change').last().append("<span class='" + weatherIcons[weather.hourly.data[j].icon] + "'</span>");
				$('.hourly-change').last().append("<span> " + Math.round(weather.hourly.data[j].temperature) + "º /</span>");
				$('.hourly-change').last().append("<span> " + Math.round(weather.hourly.data[j].precipProbability * 100) + "%</span>");
			}*/

			// daily weather
			for (var i = 0; i < 7; i++) {
				$('.weekly-forecast-container').append("<div class='weekly-forecast-day'></div>");
				$('.weekly-forecast-day').last().append("<span class='day-label'>" + arrangedDays[i] + " </span>");
				$('.weekly-forecast-day').last().append("<span class='" + weatherIcons[weather.daily.data[i].icon] +"'></span>");
				$('.weekly-forecast-day').last().append("<span> " + Math.round(weather.daily.data[i].high) + "º</span> / <span>" + Math.round(weather.daily.data[i].low) + "º </span>");
			}
			t = setTimeout(function () {
					getWeather()
				}, 1000*60*60);
		}

		// QUOTES
		function getQuote() {
			$.get("/get_quote", function (data) {
				$('.quote-content').html(data.content);
				$('.quote-author').html(data.author);

				setTimeout(function () {
					getQuote()
				}, 1000*60);
				
			});
		}

		// NEWS TICKER
		function getNews() {
			$.get("/get_news_headlines", function (data) {
				var headlines = data.headlines.slice(0, 10); // just get the first 10 because they get crappy after that
				$('.marquee').hide();
				
				headlines.forEach(function(headline) {
					$('.marquee').append("<li>" + headline.description + "</li>");
					$('.marquee').append("<li class='wi wi-hurricane'></li>");
				});

				setTimeout(function() {
					$('.marquee').show();

					// https://jsfiddle.net/ymdahi/sj2Lcq6x/
					$('.marquee').marquee({
				        duration: 8000,
				        duplicate: false
					    });
						}, 1000);
				
			});
		}

		startTime();
		getWeather();
		getQuote();
		getNews();
	});

})();
