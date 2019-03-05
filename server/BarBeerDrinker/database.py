from sqlalchemy import create_engine
from sqlalchemy import sql

from BarBeerDrinker import config

engine = create_engine(config.database_uri)

#get us all bars
def get_bars():
	with engine.connect() as con:
		rs = con.execute("SELECT name, address, openHour, closeHour, state FROM Bar;")
		return [dict(row) for row in rs]

#get us the information about the bar named 'name'
def find_bar(name):
	with engine.connect() as con:
		query = sql.text("SELECT name, address, openHour, closeHour, state FROM Bar WHERE name= :name;")
		rs = con.execute(query, name=name)
		result = rs.first() #this specifies we want first result
		if result is None:
			return None
		return dict(result)

def find_item(name):
	with engine.connect() as con:
		query = sql.text("SELECT name, type, manufacturer FROM Item WHERE name= :name;")
		rs = con.execute(query, name=name)
		result = rs.first() #this specifies we want first result
		if result is None:
			return None
		return dict(result)

#we want all beers below max_price, assuming prices is saved as decimal
# below, we do the following:
#	- parameterized query to filter beers by price
#	- converting all rows to dicts
#	- making sure price value is float, since python does not explicitly convert from deciaml
def filter_beers(max_price):
		with engine.connect() as con:
			query = sql.text("SELECT s1.bar, s1.item, s1.price FROM Sells s1, Item i1 WHERE s1.price < :max_price AND i1.name=s1.item AND i1.type='beer';")
			rs=con.execute(query, max_price=max_price)
			results = [dict(row) for row in rs]
			for r in results:
				r['price']=float(r['price'])
			return results

def get_bars_selling(beer):
	with engine.connect() as con:
		query = sql.text('SELECT a.bar, a.price, b.customers \
			FROM Sells AS a \
			JOIN (SELECT bar, count(*) AS customers FROM Frequents GROUP by bar) as b \
			ON a.bar=b.bar \
			WHERE a.item = :beer\
			ORDER BY a.price;\
		')
		rs=con.execute(query, beer=beer)
		results = [dict(row) for row in rs]
		for i, _ in enumerate(results):
			results[i]['price'] = float(results[i]['price'])
		return results

def get_bar_frequents_count():
	with engine.connect() as con:
		query = sql.text('SELECT bar, count(*) as frequentCount \
			FROM Frequents \
			GROUP BY bar;\
		')
		rs=con.execute(query)
		results = [dict(row) for row in rs]
		return results

#gets list of things liked by drinker (beer ^ food)
def get_likes(drinker_name):
	with engine.connect() as con:
		query=sql.txt('SELECT item FROM Likes WHERE drinker = :name;')
		rs = con.execute(query, name=drinker_name)
		return [row['item'] for row in rs]


def get_drinker_info(drinker_name):
	with engine.connect() as con:
		query = sql.text('SELECT * FROM Drinker WHERE name = :name;')
		rs=con.execute(query, name=drinker_name)
		results = rs.first()
		if results is None:
			return None
		return dict(results)

#gets all drinkers and their info
def get_drinkers():
	with engine.connect() as con:
		rs = con.execute('SELECT name, address, state FROM Drinker;')
		return [dict(row) for row in rs]

def get_item_manufacturer(beer):
	with engine.connect() as con:
		if beer is None:
			rs=con.execute('SELECT DISTINCT manufacturer FROM Item;')
			return [row['manufacturer'] for row in rs]
		print(beer)
		query = sql.text('SELECT manufacturer FROM Item WHERE name = :beer;')
		rs = con.execute(query, beer=beer)
		result=rs.first()
		if result is None:
			return None
		if result['manufacturer'] == 'bar':
			print('the bar makes this')
			return 'the bar'
		return result['manufacturer']

#get all beer names	
def get_beers():
	with engine.connect() as con:
		rs = con.execute('SELECT name, manufacturer FROM Item WHERE type=beer;')
		return [dict(row) for row in rs]

#get all food names
def get_foods():
	with engine.connect() as con:
		rs = con.execute('SELECT name, manufacturer FROM Item WHERE type=food;')
		return [dict(row) for row in rs]

#get all items
def get_all_items():
	with engine.connect() as con:
		rs = con.execute('SELECT type, name, manufacturer FROM Item where type=\'beer\';')
		return [dict(row) for row in rs]



def get_bar_menu(bar_name):
	with engine.connect() as con:
		query=sql.text('\
			SELECT a.bar, a.item, b.type, a.price, b.manufacturer, coalesce(c.like_count, 0) as likes \
			FROM Sells as a \
			JOIN Item AS b \
			ON a.item=b.name \
            LEFT OUTER JOIN (SELECT k1.item, count(*) as like_count  FROM Likes k1  GROUP BY k1.item ) as c \
			ON a.item = c.item \
            WHERE a.bar = :bar;\
		')
		rs = con.execute(query, bar=bar_name)
		results = [dict(row) for row in rs]
		for i, _ in enumerate(results):
			results[i]['price'] = float(results[i]['price'])
		return results


def get_highest_spenders_totals(bar_name):
	with engine.connect() as con:
		with engine.connect() as con:
			query=sql.text('\
				SELECT t1.drinker, SUM(b1.total) as total \
				FROM Transaction t1, Bill b1\
				WHERE t1.billID=b1.transactionID AND bar=:bar\
				GROUP BY t1.drinker \
				ORDER BY total DESC\
				LIMIT 10;\
			')
			rs = con.execute(query, bar=bar_name)
			results = [dict(row) for row in rs]
			for i, _ in enumerate(results):
				results[i]['total'] = float(results[i]['total'])
			return results

def get_most_popular_beers(bar_name):
	with engine.connect() as con:
		with engine.connect() as con:
			query=sql.text('\
				SELECT i1.name, SUM(t1.quantity) as total \
				FROM Item i1, Transaction t1 \
				WHERE i1.name=t1.item AND i1.type=\'beer\' AND t1.bar=:bar \
				GROUP BY i1.name \
				ORDER BY total DESC\
				LIMIT 10;\
			')
			rs = con.execute(query, bar=bar_name)
			results = [dict(row) for row in rs]
			#for i, _ in enumerate(results):
			#	results[i]['total'] = float(results[i]['total'])
			return results

def get_most_popular_manf(bar_name):
	with engine.connect() as con:
		with engine.connect() as con:
			query=sql.text('\
				SELECT i1.manufacturer, SUM(t1.quantity) as total \
				FROM Item i1, Transaction t1 \
				WHERE i1.name=t1.item AND i1.type=\'beer\' AND t1.bar=:bar\
				GROUP BY i1.manufacturer \
				ORDER BY total DESC\
				LIMIT 5;\
			')
			rs = con.execute(query, bar=bar_name)
			results = [dict(row) for row in rs]
			#for i, _ in enumerate(results):
			#	results[i]['total'] = float(results[i]['total'])
			return results

def get_top_selling_bars(item_name):
	with engine.connect() as con:
		with engine.connect() as con:
			query=sql.text('\
				SELECT t1.bar, SUM(t1.quantity) as total \
				FROM Transaction t1, Bill b1\
				WHERE t1.billID=b1.transactionID AND t1.item=:item\
				GROUP BY t1.bar\
				ORDER BY total DESC\
				LIMIT 10;\
			')
			rs = con.execute(query, item=item_name)
			results = [dict(row) for row in rs]
			#for i, _ in enumerate(results):
			#	results[i]['total'] = float(results[i]['total'])
			return results

def get_top_buyers(item_name):
	with engine.connect() as con:
		with engine.connect() as con:
			query=sql.text('\
				SELECT t1.drinker, SUM(t1.quantity) as total  \
				FROM Transaction t1, Bill b1 \
				WHERE t1.billID=b1.transactionID AND t1.item=:item \
				GROUP BY t1.drinker \
				ORDER BY total DESC \
				LIMIT 10; \
			')
			rs = con.execute(query, item=item_name)
			results = [dict(row) for row in rs]
			#for i, _ in enumerate(results):
			#	results[i]['total'] = float(results[i]['total'])
			return results

def get_top_months(item_name):
	with engine.connect() as con:
		with engine.connect() as con:
			query=sql.text('\
				SELECT ASCII(b1.date) as date, SUM(t1.quantity) as total \
				FROM Transaction t1, Bill b1 \
				WHERE t1.billID=b1.transactionID AND t1.item=:item \
				GROUP BY ASCII(b1.date)\
				ORDER BY total DESC\
				LIMIT 10;\
			')
			rs = con.execute(query, item=item_name)
			results = [dict(row) for row in rs]
			#for i, _ in enumerate(results):
			#	results[i]['total'] = float(results[i]['total'])
			return results



def get_drinker_trans_by_time(drinker_name):
	with engine.connect() as con:
		with engine.connect() as con:
			query=sql.text('\
				SELECT t1.billID, t1.item, t1.bar, b1.date, b1.transTime as time\
				FROM Transaction t1, Bill b1\
				WHERE t1.billID=b1.transactionID AND t1.drinker=:drinker AND ASCII(b1.transTime)!=49\
				GROUP BY t1.bar\
				ORDER BY time DESC\
				limit 10;\
			')
			rs = con.execute(query, drinker=drinker_name)
			results = [dict(row) for row in rs]
			#for i, _ in enumerate(results):
			#	results[i]['total'] = float(results[i]['total'])
			return results

def find_drinker(drinker_name):
	with engine.connect() as con:
		with engine.connect() as con:
			query=sql.text('\
				SELECT name \
				FROM Drinker \
				WHERE name = :drinker;\
			')
			rs = con.execute(query, drinker=drinker_name)
			results = [dict(row) for row in rs]
			#for i, _ in enumerate(results):
			#	results[i]['total'] = float(results[i]['total'])
			return results

def get_drinker_likes(drinker_name):
	with engine.connect() as con:
		with engine.connect() as con:
			query=sql.text('\
				SELECT i1.name, i1.type\
				FROM Item i1, Likes l1\
				Where l1.drinker= :drinker and i1.name=l1.item \
				group by i1.name \
				order by i1.name asc\
			')
			rs = con.execute(query, drinker=drinker_name)
			results = [dict(row) for row in rs]
			#for i, _ in enumerate(results):
			#	results[i]['total'] = float(results[i]['total'])
			return results


def get_drinker_trans_by_time(drinker_name):
	with engine.connect() as con:
		with engine.connect() as con:
			query=sql.text('\
				SELECT t1.billID, t1.item, t1.bar, b1.date, b1.transTime as time\
				FROM Transaction t1, Bill b1\
				WHERE t1.billID=b1.transactionID AND t1.drinker=:drinker AND ASCII(b1.transTime)!=49\
				GROUP BY t1.bar\
				ORDER BY time DESC\
				limit 10;\
			')
			rs = con.execute(query, drinker=drinker_name)
			results = [dict(row) for row in rs]
			#for i, _ in enumerate(results):
			#	results[i]['total'] = float(results[i]['total'])
			return results

def get_drinker_transactions(drinker_name):
	with engine.connect() as con:
		with engine.connect() as con:
			query=sql.text('\
				SELECT CONCAT(  CONCAT(SUBSTR(b1.transTime FROM 1 FOR char_length(b1.transTime)-2 ), \':\' ),  SUBSTR(b1.transTime FROM char_length(b1.transTime)-1  )) AS time, t1.billID as id, t1.bar, t1.item, t1.quantity, b1.total as total, b1.date \
				FROM Bill b1, Transaction t1 \
				WHERE b1.transactionID=t1.billID AND t1.drinker = :drinker \
				ORDER BY b1.transTime ASC \
			')

			
			rs = con.execute(query, drinker=drinker_name)
			results = [dict(row) for row in rs]
			for i, _ in enumerate(results):
				results[i]['total'] = float(results[i]['total'])
			return results

def get_drinker_freq_bars(drinker_name):
	with engine.connect() as con:
		with engine.connect() as con:
			query=sql.text('\
				SELECT f1.bar, b1.state\
				FROM Frequents f1, Bar b1\
				WHERE f1.drinker = :drinker and f1.bar=b1.name\
			')
			rs = con.execute(query, drinker=drinker_name)
			results = [dict(row) for row in rs]
			return results

def get_drinker_high_spending(drinker_name):
	with engine.connect() as con:
		with engine.connect() as con:
			query=sql.text('\
				SELECT t1.bar,  sum(b1.total) as total \
				FROM Transaction t1, Bill b1 \
				where t1.drinker = :drinker AND b1.transactionID=t1.billID \
				GROUP BY t1.bar \
				ORDER BY total desc \
				LIMIT 20;\
			')
			rs = con.execute(query, drinker=drinker_name)
			results = [dict(row) for row in rs]
			for i, _ in enumerate(results):
				results[i]['total'] = float(results[i]['total'])
			return results

def get_drinker_most_ordered(drinker_name):
	with engine.connect() as con:
		with engine.connect() as con:
			query=sql.text('\
				SELECT t1.item, SUM(t1.quantity) AS total \
				FROM Transaction t1, Item i1 \
				WHERE t1.drinker=:drinker AND i1.name=t1.item AND i1.type=\'beer\'\
				GROUP BY t1.item \
				ORDER BY total DESC \
				LIMIT 20; \
			')
			rs = con.execute(query, drinker=drinker_name)
			results = [dict(row) for row in rs]
			for i, _ in enumerate(results):
				results[i]['total'] = float(results[i]['total'])
			return results

def get_drinker_days_spending(drinker_name):
	with engine.connect() as con:
		with engine.connect() as con:
			query=sql.text('\
				SELECT MOD((ASCII(substr(b1.date from INSTR(b1.date, \'/\')+1))+(ASCII(substr(b1.date from INSTR(b1.date, \'/\')+2)))), 7)+1 AS day, SUM(b1.total) AS total \
				FROM Bill b1, Transaction t1 \
				WHERE t1.billID = b1.transactionID AND t1.drinker=:drinker \
				GROUP BY day \
				ORDER BY total desc; \
			')
			rs = con.execute(query, drinker=drinker_name)
			results = [dict(row) for row in rs]
			for i, _ in enumerate(results):
				results[i]['total'] = float(results[i]['total'])
			return results


def get_drinker_weeks_spending(drinker_name):
	with engine.connect() as con:
		query=sql.text('\
			Select Round((4.25* (CONVERT(substr(b1.date from 1 for INSTR(b1.date, \'/\')-1), UNSIGNED INTEGER)-1)) + (CONVERT(substring(substring_index(b1.date, \'/\', 2) from INSTR(b1.date, \'/\')+1), UNSIGNED INTEGER) DIV 7)) as week, SUM(b1.total) AS total \
			FROM Bill b1, Transaction t1 \
			WHERE t1.billID = b1.transactionID AND t1.drinker=:drinker \
			GROUP BY week \
			ORDER BY total DESC \
			LIMIT 15; \
		')
		rs = con.execute(query, drinker=drinker_name)
		results = [dict(row) for row in rs]
		for i, _ in enumerate(results):
			results[i]['total'] = float(results[i]['total'])
			results[i]['week'] = float(results[i]['week'])
		return results

def get_drinker_month_spending(drinker_name):
	with engine.connect() as con:
		query=sql.text('\
			SELECT CONVERT(substring_index(b1.date, \'/\', 1), UNSIGNED INTEGER) AS month, SUM(b1.total) AS total\
			FROM Bill b1, Transaction t1 \
			WHERE t1.billID = b1.transactionID AND t1.drinker=:drinker \
			GROUP BY month \
			ORDER BY total DESC; \
		')
		rs = con.execute(query, drinker=drinker_name)
		results = [dict(row) for row in rs]
		for i, _ in enumerate(results):
			results[i]['total'] = float(results[i]['total'])
			results[i]['month'] = float(results[i]['month'])
		return results

def get_busy_hour(bar_name):
	with engine.connect() as con:
		query=sql.text('\
			SELECT CONVERT(substring_index(b1.transTime, \':\', 1), UNSIGNED INTEGER) AS hour, count(b1.transactionID) AS total \
			FROM Bill b1, Transaction t1 \
			WHERE b1.transactionID=t1.billID AND t1.bar=:bar AND b1.transTime!=\'12:00a\' \
			GROUP BY hour\
			ORDER BY total DESC\
		')
		rs = con.execute(query, bar=bar_name)
		results = [dict(row) for row in rs]
		for i, _ in enumerate(results):
			results[i]['total'] = float(results[i]['total'])
			results[i]['hour'] = float(results[i]['hour'])
		return results

def get_busy_day(bar_name):
	with engine.connect() as con:
	
		query=sql.text('\
			SELECT MOD((ASCII(substr(b1.date from INSTR(b1.date, \'/\')+1))+(ASCII(substr(b1.date from INSTR(b1.date, \'/\')+2)))), 7)+1 AS day, count(b1.transactionID) AS total \
			FROM Bill b1, Transaction t1 \
			WHERE t1.billID = b1.transactionID AND t1.bar=:bar AND b1.transTime!=\'12:00a\' \
			GROUP BY day \
			ORDER BY total desc; \
		')
		rs = con.execute(query, bar=bar_name)
		results = [dict(row) for row in rs]
		for i, _ in enumerate(results):
			results[i]['total'] = float(results[i]['total'])
			results[i]['day'] = float(results[i]['day'])
		return results



def perform_query(q):
	with engine.connect() as con:
		#print(q)
		qq=q
		#qq="START TRANSACTION;"+q + "ROLLBACK;"
		query=sql.text(qq)
		#print("next is query")
		#print(query)
		try:
			#rs=con.execute(q)
			#results = [dict(row) for row in rs]
			
			#if results is not None: #the query is LEGAL
				#rs=con.execute(sql.text("ROLLBACK;"))
			
			
			
			#if('Frequents' in qq):
			#	return check_freq_constraint()
			#if('Bill' in qq):
			#	return check_bill_constraint()

			#Make the insert. Now delete all entries against out query that proves pattern
			#DONE for Sells. Must fix Bill query and create Frequents query. Frequents would be easy
			if('INSERT' in qq):
				if('Sells' in qq):
					return check_beer_price_insert(q)
				if('Bill' in qq):
					return check_bill_time_insert(q)
				if('Frequents' in qq):
					return find_drinker_bar_for_constraint_insert(qq)
			
			#first check to see if the update is valid against pattern. if it is, do it. If not, report it.
			#if('UPDATE' in qq):
				
				#rs= [{'output' : 'Query not possible'}]
				#results = [dict(row) for row in rs]
				#print(results)
				#return results 
				#return check_update(q)
				#if('Sells' in qq):
				#	return check_beer_price_update(q)
			#	if('Frequents' in qq):
			#		return check_bill_time_update(q)
			#	if('Bill' in qq):
			#		return find_drinker_bar_for_constraint_update(q)
			
			#check to see if the delete actually did anything (just count entries)
			#if('DELETE' in qq):
			#	if('Sells' in qq):
			#	if('Frequents' in qq):
			#	if('Bill' in qq):

			rs=con.execute(q)
			rs=[{'output' : 'Query was successful'}]
			results = [dict(row) for row in rs]
			#print(results)
			return results
		except Exception as e:
			#rs= [{'output' : 'Query not possible. Please try again.'}]
			rs= [{'output' : 'Got error {!r}, errno is {}'.format(e, e.args[0])}]
			results = [dict(row) for row in rs]
			return results 





def find_drinker_bar_for_constraint_insert(q):
	with engine.connect() as con:
		# 'Insert into Frequents (drinker, bar) Values ()
		vpos=q.find("VALUES")+6
		
		s=q[vpos:]
		#print(s)
		dpos=s.find("(")+1
		#print("dpos:", dpos)
		bpos=s.find(",")+1
		#print("bpos:",bpos)
		cpos=bpos
		end=s.find(")")
		#print("end:", end)
		while(s[dpos]==" " and s[dpos]=="'"):
			dpos=dpos+1
		while(s[bpos]==" " and s[bpos]=="'"):
			bpos=bpos+1
		while(s[end]==" " and s[end]=="'"):
			end=end-1
		#print("after search")
		#drinker=s.substring(dpos,cpos)
		drinker=s[dpos:cpos]
		#bar=s.substring(bpos,end)
		bar=s[bpos:end]
		#print(bar)
		#print(drinker)
		bar_query=sql.text('\
			Select state from Bar Where name=:bar;\
		')
		
		drinker_query=sql.text('\
			Select state from Drinker Where name=:drinker\
		')
		try:
			bar_rs=con.execute(bar_query, bar=bar)
			drinker_rs=con.execute(drinker_query, drinker=drinker)
			if(bar_rs!=drinker_rs):
				rs=[{'output' : 'Error: Action not committed to database due to frequents constraint'}]
				#print(rs)
				return [dict(row) for row in rs]
			rs=con.execute(q)
			rs=[{'output' : 'Query, '+q+' , was successful'}]
			return [dict(row) for row in rs]
		except Exception as e:
			#print(e)
			#print("not possible")
			#rs= [{'output' : 'Query not possible. Please try again.'}]
			rs= [{'output' : 'Got error {!r}, errno is {}'.format(e, e.args[0])}]
			results = [dict(row) for row in rs]
			#print(results)
			return results 

def check_bill_time_insert(q):
	#<1200 or >45
	with engine.connect() as con:
		vpos=q.find("VALUES")+6
		s=q[vpos:]
		#print(s)
		end=s.find(")")
		cpos=end
		#print("end:", end)
		while(s[cpos]!=","):
			cpos=cpos-1
		while(s[cpos]==" "):
			cpos=cpos+1
		time=s[cpos+1:end]
		#print("cpos:",cpos)
		#print("end:",end)
		#print("time:",time)
		i=1
		while(time[i]=="0"):
			i=i+1
			if(i==len(time)-2):
				break
		
		time=time[i:len(time)-1]
		#print("time:", time)
		c=int(time)
		#print("time int:", c)
		if(c>45 and c<1200):
			rs= [{'output' : 'Error: Transaction time constraint violated. Action disallowed'}]
			results = [dict(row) for row in rs]
			#print(results)
			return results 
		try:
			rs=con.execute(q)
			rs=[{'output' : 'Query, '+q+' , was successful'}]
			return [dict(row) for row in rs]
		except Exception as e:
			#print(e)
			#print("not possible")
			#rs= [{'output' : 'Query not possible. Please try again.'}]
			rs= [{'output' : 'Got error {!r}, errno is {}'.format(e, e.args[0])}]
			results = [dict(row) for row in rs]
			#print(results)
			return results 
		

def check_beer_price_insert(q):
	#values ('bar', 'item', price)
	with engine.connect() as con:
		vpos=q.find("VALUES")+6
		s=q[vpos:]
		#print(len(s))
		#print(s)
		begin=s.find("(")
		while(s[begin]==" "):
			begin=begin+1
		
		end=s.find(")")
		cpos=end
		while(s[cpos]==" "):
			cpos=cpos-1
		while(s[cpos]!=" " and s[cpos]!=","):
			cpos=cpos-1
		while(s[cpos]==" " or s[cpos]=="," ):
			cpos=cpos+1
		price_start=cpos
		price=s[price_start:end]
		#print("price:", price)
		#print(price_start)
		#print(s[price_start:])

		while(s[cpos]!=","):
			cpos=cpos-1
		item_end=cpos-1
		#print("item_end:", item_end)
		while(s[item_end]!="'"):
			item_end=item_end-1
		
		#print(s[item_end:])
		#print("item_end:", item_end)
		cpos=item_end
		while(s[cpos]!=","):
			cpos=cpos-1
		while(s[cpos]!="'"):
			cpos=cpos+1
		item_start=cpos
		#print("item_start:",item_start)
		

		


		item=s[item_start+1:item_end]
		#price=s[price_start:end]
		#print("price:", price)
		#print("item:", item)
		p=float(price)
		#print("float price:", p)
		i=beer_ifs(item, p)
		if(i==1):
			rs= [{'output' : 'Error: Beer price ordering violated by insertion'}]
			results = [dict(row) for row in rs]
			return results 
		try:
			rs=con.execute(q)
			rs=[{'output' : 'Query, '+q+' , was successful'}]
			return [dict(row) for row in rs]
		except Exception as e:
			rs= [{'output' : 'Got error {!r}, errno is {}'.format(e, e.args[0])}]
			results = [dict(row) for row in rs]
			return results 


		


	
	#with engine.connect() as con:
	#	if(field!="price" and field=='item'):
	#		
	#	print("field:", field)
	#	while(s1[ep]==" " or s1[ep]==","):
	#		ep=ep+1
	#	attr_start=ep
	#	while(s1[ep]!=" " or s1[ep]!="'"):
	#		ep=ep+1
	#	attr_end=ep-1
	#	value=s1[attr_start:attr_end]
	#	print("value:", value)
	#	rs=[{'output' : 'Query, '+q+' , was successful'}]
	#	return [dict(row) for row in rs]
	
	



def beer_ifs(item, price):
	#print("got item:",item)
	#print("got price:",price)
	if(item=="Bud Light"):
		if(price>7.00 or price<6.75):
			return 1
		return 0
	if(item=="Budweiser"):
		if(price>6.75 or price<6.50):
			return 1
		return 0
	if(item=="Blue Moon"):
		#print("where i want to be")
		if(price>6.50 or price<6.25):
			return 1
		return 0
	if(item=="Coors Light"):
		if(price>6.25 or price<6.00):
			return 1
		return 0
	if(item=="Miller Light"):
		if(price>6.00 or price<5.75):
			return 1
		return 0
	if(item=="Miller"):
		if(price>5.75 or price<5.50):
			return 1
		return 0
	if(item=="Stella Artois"):
		if(price>5.50 and price<5.25):
			return 1
		return 0
	if(item=="Peroni"):
		if(price>5.25 or price<5.00):
			return 1
		return 0
	if(item=="Corona"):
		if(price>5.00 or price<4.75):
			return 1
		return 0
	if(item=="Shock Top"):
		if(price>4.75 or price<4.50):
			return 1
		return 0
	if(item=="Michelob Ultra"):
		if(price>4.50 or price<4.25):
			return 1
		return 0
	if(item=="Dos Equis"):
		if(price>4.25 or price<4.00):
			return 1
		return 0
	if(item=="Guiness"):
		if(price>4.00 or price<3.75):
			return 1
		return 0
	if(item=="Fat Tire"):
		if(price>3.75 or price<3.50):
			return 1
		return 0
	if(item=="Yuengling"):
		if(price>3.50 or price<3.25):
			return 1
		return 0
	if(item=="Heineken"):
		if(price>3.25 or price<3.00):
			return 1
		return 0
	if(item=="Heineken Light"):
		if(price>3.00 or price<2.75):
			return 1
		return 0
	if(item=="Modelo Especial"):
		if(price>2.75 or price<2.50):
			return 1
		return 0
	if(item=="Sam Adams Boston Lager"):
		if(price>2.50 or price<2.25):
			return 1
		return 0
	if(item=="Sam Adams Oktober Fest"):
		if(price>2.25 or price<2.00):
			return 1
		return 0
	return 1
