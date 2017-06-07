#-*- coding: utf-8 -*-
from flask import Flask, render_template, send_from_directory, jsonify
import urllib2
import xml.etree.ElementTree as ET
import subprocess
import random

import config
from utils import weatherapi, twitterbot

app = Flask(__name__, static_url_path='/static', template_folder='./')

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/<path:path>')
def serve_static(path):
	return send_from_directory('static', path)

@app.route('/get_weather')
def get_weather():
	location = config.location
	result = weatherapi.get_weather_by_name(location)
	return jsonify(result)

@app.route('/get_quote')
def get_quote():
	who = random.choice(config.twitters)
	result = twitterbot.getTweet(who, config.proxies)
	if result.get("error"):
		print "get twitter of", who, "error:", result["error"]
		return jsonify({})
	else:
		return jsonify(result)

@app.route('/get_news_headlines')
def get_news_headlines():
	xml_response = urllib2.urlopen('http://feeds.bbci.co.uk/news/rss.xml?edition=us').read()
	xml_root = ET.fromstring(xml_response)
	results = []

	for item in xml_root[0].findall('item'):
		item_info = {}
		item_info['title'] = item[0].text
		item_info['description'] = item[1].text
		results.append(item_info)

	return jsonify({'headlines': results})

@app.route('/get_todo')
def get_todo():
	return jsonify({"hourly":[{"begin_time":"12:00", "end_time":"13:00", "content":"testing"}]})

if __name__ == '__main__':
	app.run(debug=DEBUG, port=PORT, host=HOST)
