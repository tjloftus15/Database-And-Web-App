from flask import Flask
from flask import jsonify
from flask import make_response
from flask import request
import json

from BarBeerDrinker import database

app = Flask(__name__)
#below executes our get_bars function found in database.py
@app.route('/api/bar', methods=["GET"])
def get_bars():
	return jsonify(database.get_bars())

@app.route('/api/bar/<name>', methods=["GET"])
def find_bar(name):
	try:
		if name is None:
			raise ValueError("Bar is not specified")
		bar = database.find_bar(name)
		if bar is None:
			return make_response("No bar found with given bar name", 404)
		return jsonify(bar)
	except ValueError as e:
		return make_response(str(e), 400)
	except Exception as e:
		return make_response(str(e), 500)

@app.route('/api/beers_cheaper_than', methods=["POST"])
def find_beers_cheaper_than():
	body=json.loads(request.data)
	max_price = body['maxPrice']
	return jsonify(database.filter_beers(max_price))

@app.route('/api/menu/<name>', methods=["GET"])
def get_menu(name):
	try:
		if name is None:
			raise ValueError('Bar is not specified')
		bar = database.find_bar(name)
		if bar is None:
			return make_response("No bar found with given name", 404)
		return jsonify(database.get_bar_menu(name))
	except ValueError as e:
		return make_response(str(e), 400)
	except Exception as e:
		return make_response(str(e), 500)

@app.route('/api/menu/spenders/<name>', methods=["GET"])
def get_highest_spenders_totals(name):
	try:
		if name is None:
			raise ValueError('Bar is not specified')
		bar=database.find_bar(name)
		if bar is None:
			return make_response("No bar found with given name", 404)
		return jsonify(database.get_highest_spenders_totals(name))
	except ValueError as e:
		return make_response(str(e), 400)
	except Exception as e:
		return make_response(str(e), 500)

@app.route('/api/menu/popular/<name>', methods=["GET"])
def get_most_popular_beers(name):
	try:
		if name is None:
			raise ValueError('Bar is not specified')
		bar=database.find_bar(name)
		if bar is None:
			return make_response("No bar found with given name", 404)
		return jsonify(database.get_most_popular_beers(name))
	except ValueError as e:
		return make_response(str(e), 400)
	except Exception as e:
		return make_response(str(e), 500)

@app.route('/api/menu/manf/<name>', methods=["GET"])
def get_most_popular_manf(name):
	#try:
	if name is None:
		raise ValueError('Bar is not specified')
	bar=database.find_bar(name)
	if bar is None:
		return make_response("No bar found with given name", 404)
	return jsonify(database.get_most_popular_manf(name))
	#except ValueError as e:
	#	return make_response(str(e), 400)
	#except Exception as e:
	#	return make_response(str(e), 500)

@app.route('/api/bar/hour/<name>', methods=["GET"])
def get_busy_hour(name):
	#try:
	if name is None:
		raise ValueError('Bar is not specified')
	bar=database.find_bar(name)
	if bar is None:
		return make_response("No bar found with given name", 404)
	return jsonify(database.get_busy_hour(name))
	#except ValueError as e:
	#	return make_response(str(e), 400)
	#except Exception as e:
	#	return make_response(str(e), 500)

@app.route('/api/bar/day/<name>', methods=["GET"])
def get_busy_day(name):
	#try:
	if name is None:
		raise ValueError('Bar is not specified')
	bar=database.find_bar(name)
	if bar is None:
		return make_response("No bar found with given name", 404)
	return jsonify(database.get_busy_day(name))
	#except ValueError as e:
	#	return make_response(str(e), 400)
	#except Exception as e:
	#	return make_response(str(e), 500)



@app.route('/api/bar-cities', methods=["GET"])
def get_bar_addr():
	try:
		return jsonify(database.get_bar_addr())
	except Exception as e:
		return make_response(str(e), 500)

#gets all beers in database
@app.route('/api/beer', methods=["GET"])
def get_beers():
	try:
		return jsonify(database.get_beers())
	except Exception as e:
		return make_response(str(e), 500)

#gets all foods in database
@app.route('/api/food', methods=["GET"])
def get_foods():
	try:
		return jsonify(database.get_foods())
	except Exception as e:
		return make_response(str(e), 500)

#gets all items (food ^ items) in database
@app.route('/api/items', methods=["GET"])
def get_all_items():
	try:
		return jsonify(database.get_all_items())
	except Exception as e:
		return make_response(str(e), 500)


@app.route('/api/items/top-bar/<name>', methods=["GET"])
def get_top_selling_bars(name):
	try:
		if name is None:
			raise ValueError('Bar is not specified')
		item=database.find_item(name)
		if item is None:
			return make_response("No bar found with given name", 404)
		return jsonify(database.get_top_selling_bars(name))
	except ValueError as e:
		return make_response(str(e), 400)
	except Exception as e:
		return make_response(str(e), 500)

@app.route('/api/items/top-buyer/<name>', methods=["GET"])
def get_top_buyers(name):
	try:
		if name is None:
			raise ValueError('Bar is not specified')
		item=database.find_item(name)
		if item is None:
			return make_response("No bar found with given name", 404)
		return jsonify(database.get_top_buyers(name))
	except ValueError as e:
		return make_response(str(e), 400)
	except Exception as e:
		return make_response(str(e), 500)	

@app.route('/api/items/top-month/<name>', methods=["GET"])
def get_top_months(name):
	try:
		if name is None:
			raise ValueError('item is not specified')
		item=database.find_item(name)
		if item is None:
			return make_response("No item found with given name", 404)
		return jsonify(database.get_top_months(name))
	except ValueError as e:
		return make_response(str(e), 400)
	except Exception as e:
		return make_response(str(e), 500)	

@app.route('/api/drinker/trans/time/<name>', methods=["GET"])
def get_drinker_trans_by_time(name):
	try:
		if name is None:
			raise ValueError('drinker is not specified')
		drinker=database.find_item(name)
		if item is None:
			return make_response("No drinker found with given name", 404)
		return jsonify(database.get_drinker_trans_by_time(name))
	except ValueError as e:
		return make_response(str(e), 400)
	except Exception as e:
		return make_response(str(e), 500)	

@app.route('/api/drinker/trans/<name>', methods=["GET"])
def get_drinker_transactions(name):
	#try:
	if name is None:
		raise ValueError('drinker is not specified')
	drinker=database.find_drinker(name)
	if drinker is None:
		return make_response("No drinker found with given name", 404)
	return jsonify(database.get_drinker_transactions(name))
	#except ValueError as e:
	#	return make_response(str(e), 400)
	#except Exception as e:
	#	return make_response(str(e), 500)	

@app.route('/api/drinker/likes/<name>', methods=["GET"])
def get_drinker_likes(name):
	#try:
	if name is None:
		raise ValueError('drinker is not specified')
	drinker=database.find_drinker(name)
	if drinker is None:
		print("drinker is none")
		return make_response("No drinker found with given name", 404)
	return jsonify(database.get_drinker_likes(name))
	#except ValueError as e:
	#	return make_response(str(e), 400)
	#except Exception as e:
	#	return make_response(str(e), 500)	

#gets all beer manuf
@app.route('/api/item-manufacturer', methods=["GET"])
def get_item_manufacturer():
	try:
		return jsonify(database.get_item_manufacturer(None))
	except Exception as e:
		return make_response(str(e), 500)

#find out who makes a certain beer
@app.route('/api/item-manufacturer/<beer>', methods=["GET"])
def get_manufacturers_making(beer):
	try:
		return jsonify(database.get_item_manufacturer(beer))
	except Exception as e:
		return make_response(str(e), 500)

#get the likes of a drinker
@app.route('/api/likes', methods=["GET"])
def get_likes():
	try:
		drinker=request.args.get("drinker")
		if drinker is None:
			raise ValueError("Drinker is not specified")
		return jsonify(database.get_likes(drinker))
	except Exception as e:
		return make_response(str(e), 500)

#get all the drinkers
@app.route('/api/drinker', methods=["GET"])
def get_drinkers():
	try:
		return jsonify(database.get_drinkers())
	except Exception as e:
		return make_response(str(e), 500)

#get a certain drinker's info
@app.route('/api/drinker/<name>', methods=["GET"])
def get_drinker(name):
	#try:
	if name is None:
		raise ValueError("Drinker is not specified")
	return jsonify(database.get_drinker_info(name))
	#except ValueError as e:
	#	return make_response(str(e), 400)
	#except Exception as e:
	#	return make_response(str(e), 500)


#find what bars sell a given beer
@app.route('/api/bars-selling/<beer>', methods=["GET"])
def find_bars_selling(beer):
	#try:
	if beer is None:
		raise ValueError("Item is not specified")
	return jsonify(database.get_bars_selling(beer))
	#except ValueError as e:
		#return make_response(str(e), 400)
	#except Exception as e:
		#return make_response(str(e), 500)

#find how many people frequent each bar
@app.route('/api/frequents-data', methods=["GET"])
def get_bar_frequents_count():
	try:
		return jsonify(database.get_bar_frequents_count())
	except Exception as e:
		return make_response(str(e), 500)

#find how many people frequent each bar
@app.route('/api/drinker/freq/<name>', methods=["GET"])
def get_drinker_freq_bars(name):
	#try:
	if name is None:
		raise ValueError('drinker is not specified')
	drinker=database.find_drinker(name)
	if drinker is None:
		print("drinker is none")
		return make_response("No drinker found with given name", 404)
	return jsonify(database.get_drinker_freq_bars(name))
	#except ValueError as e:
	#	return make_response(str(e), 400)
	#except Exception as e:
	#	return make_response(str(e), 500)

@app.route('/api/drinker/spending/<name>', methods=["GET"])
def get_drinker_high_spending(name):
	#try:
	if name is None:
		raise ValueError('drinker is not specified')
	drinker=database.find_drinker(name)
	if drinker is None:
		print("drinker is none")
		return make_response("No drinker found with given name", 404)
	return jsonify(database.get_drinker_high_spending(name))
	#except ValueError as e:
	#	return make_response(str(e), 400)
	#except Exception as e:
	#	return make_response(str(e), 500)

@app.route('/api/drinker/order/<name>', methods=["GET"])
def get_drinker_most_ordered(name):
	#try:
	if name is None:
		raise ValueError('drinker is not specified')
	drinker=database.find_drinker(name)
	if drinker is None:
		print("drinker is none")
		return make_response("No drinker found with given name", 404)
	return jsonify(database.get_drinker_most_ordered(name))
	#except ValueError as e:
	#	return make_response(str(e), 400)
	#except Exception as e:
	#	return make_response(str(e), 500)

@app.route('/api/drinker/day/<name>', methods=["GET"])
def get_drinker_days_spending(name):
	#try:
	if name is None:
		raise ValueError('drinker is not specified')
	drinker=database.find_drinker(name)
	if drinker is None:
		print("drinker is none")
		return make_response("No drinker found with given name", 404)
	return jsonify(database.get_drinker_days_spending(name))
	#except ValueError as e:
	#	return make_response(str(e), 400)
	#except Exception as e:
	#	return make_response(str(e), 500)

@app.route('/api/drinker/week/<name>', methods=["GET"])
def get_drinker_weeks_spending(name):
	#try:
	if name is None:
		raise ValueError('drinker is not specified')
	drinker=database.find_drinker(name)
	if drinker is None:
		print("drinker is none")
		return make_response("No drinker found with given name", 404)
	return jsonify(database.get_drinker_weeks_spending(name))
	#except ValueError as e:
	#	return make_response(str(e), 400)
	#except Exception as e:
	#	return make_response(str(e), 500)

@app.route('/api/drinker/month/<name>', methods=["GET"])
def get_drinker_month_spending(name):
	#try:
	if name is None:
		raise ValueError('drinker is not specified')
	drinker=database.find_drinker(name)
	if drinker is None:
		print("drinker is none")
		return make_response("No drinker found with given name", 404)
	return jsonify(database.get_drinker_month_spending(name))
	#except ValueError as e:
	#	return make_response(str(e), 400)
	#except Exception as e:
	#	return make_response(str(e), 500)


@app.route('/api/mod/<q>', methods=["GET"])
def get_query_table(q):
	print(q)
	if q is None:
		print("Nothing found")
		raise ValueError('Query is not specified')
	return jsonify(database.perform_query(q))




