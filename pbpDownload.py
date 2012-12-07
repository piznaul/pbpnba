import pbpnba
import datetime
import pickle

base = "http://data.nba.com/json/cms/noseason"
#url = "http://data.nba.com/10s/json/cms/noseason/game/20121126/0021200013/pbp_1.json"
#date format:  YYYYMMDD
#date.strftime('%Y%m%d') will convert a datetime object to YYYYMMDD string.

oneDay = datetime.timedelta(days=1)
startDate = datetime.date(2012,10,30)
endDate = datetime.date.today()
currentDate = startDate

f = open('pbp2012', 'a')

while currentDate < endDate:
	#cycle through dates - find list of gameIDs from scoreboard JSON for each day.
	sbUrl = base + '/scoreboard/' + currentDate.strftime('%Y%m%d') + '/games.json'
	gameID = pbpnba.jsonSBOpener(sbUrl)
	
	if gameID != 'SBError':
		#now, with the list of gameIDs, cycle through each game (and each period) to download the pbp JSON.
		while len(gameID) != 0:
			gameIDSingle = str( gameID.pop() )
			for period in [1,2,3,4]: #not sure what do to about OT - how are they signified in the JSON filename?
				pbpUrl = base + '/game/' + currentDate.strftime('%Y%m%d') + \
					'/' + gameIDSingle + '/pbp_' + str(period) + '.json'
				periodPbpList = pbpnba.json2list(pbpUrl,period)
				#periodPbpList is a list of that quarters pbp data: 
				#list is [gameDate,gameID,period,lPlay]
				pickle.dump(periodPbpList,f)
				if mod(int(gameIDSingle[-2:]),10) == 0 and period == 4:
					print currentDate.strftime('%Y%m%d') + ' ' + gameIDSingle + \
						' ' + str( period )

		currentDate += oneDay
	else: #no games on this day. move to next.
		currentDate += oneDay


f.close()	