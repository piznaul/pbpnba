import pbpnba
import datetime

base = "http://data.nba.com/json/cms/noseason"
#url = "http://data.nba.com/10s/json/cms/noseason/game/20121126/0021200013/pbp_1.json"
#date format:  YYYYMMDD
#date.strftime('%Y%m%d') will convert a datetime object to YYYYMMDD string.

oneDay = datetime.timedelta(days=1)
startDate = datetime.date(2012,10,30)
endDate = datetime.date.today()
currentDate = startDate

while currentDate < endDate:
	#cycle through dates - find list of gameIDs from scoreboard JSON for each day.
	sbUrl = base + '/scoreboard/' + currentDate.strftime('%Y%m%d') + '/games.json'
	gameID = pbpnba.jsonSBOpener(sbUrl)
	
	#now, with the list of gameIDs, cycle through each game (and each period) to download the pbp JSON.
	while len(gameID) != 0:
		for period in [1,2,3,4]
			pbpUrl = base + '/game/' + currentDate.strftime('%Y%m%d') + '/' + str( gameID.pop() ) + '/pbp_' + str(period) + '.json'
			periodPbpList = pbpnba.json2list(pbpUrl,period)
			#periodPbpList is a list of that quarters pbp data: list is [gameDate,gameID,period,lPlay]
	currentDate += oneDay
	