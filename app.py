from flask import Flask , render_template, request, redirect, url_for
from datetime import datetime
from pprint import pprint

import json
import requests


app = Flask(__name__)

@app.route('/')
def hello_world():
	return render_template("index.html")

@app.route('/handle_data', methods=['POST'])
def handle_data():
	company = request.form['company']
	scripcode = request.form['scripcode']
	print(company,scripcode)


# -----------READING NSE DATA
	url = 'https://www.nseindia.com/api/chart-databyindex?index=' + company + 'EQN'
	headers = { 'referer' :'https://www.nseindia.com/get-quotes/equity?symbol=' + company,
	'Content-Type' : 'application/json; charset=utf-8',
	'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
	'x-requested-with': 'XMLHttpRequest'
	}

	nse = requests.get(url, headers=headers)
	nse_text = nse.text

	nsedata = json.loads(nse_text)
	#print(type(nsedata["grapthData"]))


	l = nsedata["grapthData"]



	#-------------- READ NSE DATA , NOW BSE DATA

	bse_url = 'https://api.bseindia.com/BseIndiaAPI/api/StockReachGraph/w?scripcode=' + str(scripcode) + '&flag=0&fromdate=&todate=&seriesid='
	bse = requests.get(bse_url)
	bse_text = bse.text

	bse_data = json.loads(bse_text)
	#print(type(bsedata))

	#------------ READ BSE DATA 


	dat = bse_data["Data"]
	dat_dict = json.loads(dat)

	bse_final_list = []
	bse_temp_list = []
	for i in dat_dict :
		#print(i['dttm'])
		date_obj = datetime.strptime(i['dttm'],'%a %b %d %Y %H:%M:%S')
		ms = date_obj.timestamp() * 1000
		ms = int(ms) + 19800000
		bse_temp_list.append(ms)
		bse_temp_list.append(i['dttm'])
		bse_temp_list.append(float(i['vale1']))
		bse_final_list.append(bse_temp_list)
		bse_temp_list = []


	'''
	print("------------------------------------")
	print(len(bse_final_list))
	print(len(l))
	'''
	pprint(l)
	print("-------------------------")
	pprint(bse_final_list)

	labels = []
	values = []
	diff_final_list  = []
	diff_temp_list = []
	for j in bse_final_list :
		for k in l :
			if j[0] == k[0] :


				ts = int(j[0])/1000
				print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))

				diff_temp_list.append(j[0])
				diff = abs( float(j[2]) - float(k[1]) )

				labels.append(j[0])
				values.append(round(diff,2))


				diff_temp_list.append(round(diff,2))
				diff_final_list.append(diff_temp_list)
				diff_temp_list = []
	pprint(diff_final_list)
	print(labels)
	print(values)






	return render_template('graph.html', labels=labels , values=values)
	# your code
	# return a response
	#return "Done"



if __name__ == "__main__" :
	app.run(debug=True)
