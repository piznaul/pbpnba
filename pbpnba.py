# module containing various functions for parsing nba play-by-play (pbp) data
import json
import pylab
import matplotlib
import urllib2
import pickle
import numpy
import datetime


# function to convert unicode time remaining in pbp feed to 
# seconds elapsed.
def import_time(unicode_input):
	quarterLength = 12*60
	if len(unicode_input) == 0:
		# clock countdown has not started yet, time elapsed is 0.
		return int(0)
	else:
		minute = int( unicode_input[0]+unicode_input[1] )
		second = int( unicode_input[3]+unicode_input[4] )
		return quarterLength - (minute*60 + second)
	
def scoreArray(playList):
	clock,homeScore,awayScore = [],[],[]

	for p in playList:
		dPlaySingle = p

		clock.append( import_time( dPlaySingle['clock'] ) )
		homeScore.append( int( dPlaySingle['home_score'] ) )
		awayScore.append( int( dPlaySingle['visitor_score'] ) )
		
	return (clock,homeScore,awayScore)
	
def json2list(url,period):
	# takes in url of json, and outputs a list of :
	# {gameDate,gameID,period,lPlay}
	try:
		req = urllib2.Request(url)
		opener = urllib2.build_opener()
		f = opener.open(req)
	except:
		print url
	d = json.load(f)
	
	# output of 'play' key of d is a list, not a dict.
	# individual plays are ordered 0..N
	lPlay = d['sports_content']['game']['play']
	gameDate = d['sports_content']['game']['date']
	gameID = d['sports_content']['game']['id']
	listOutput = [gameDate, gameID, period, lPlay]
	return listOutput
	
def jsonSBOpener(url):
	# takes in url of scoreboard json, and outputs a list of gameIDs for that date.
	try:
		req = urllib2.Request(url)
		opener = urllib2.build_opener()
		f = opener.open(req)
		d = json.load(f)
		gameID = []
		# remove initial layers of dict
		d2 = d['sports_content']['games']['game']
		while len(d2) != 0:
			gameID.append( d2.pop()['id'] )
		return gameID
	except:
		print url
		return 'SBError'
		
def scorePlot(fileID,gameID):
	clock,homeScore,awayScore = [],[],[]
	cTemp,hTemp,aTemp = [],[],[]
	d = pickle.load(fileID)
	if d[1] == gameID:
		for period in [1,2,3,4]: #not sure what do to about OT - how are they signified in the JSON filename?
			if d[2] == period:
				(cTemp,hTemp,aTemp) = scoreArray( d[3] )
				cTempArray = numpy.array(cTemp) + 720*(period - 1)				
				clock.append( cTempArray )
				homeScore.append( hTemp )
				awayScore.append( aTemp )
				d = pickle.load(fileID)
	return (clock, flatten(homeScore), flatten(awayScore)) 		
	#matplotlib.pyplot.plot(clock,homeScore,clock,awayScore)
	
def flatten(x):
    """flatten(sequence) -> list

    Returns a single, flat list which contains all elements retrieved
    from the sequence and all recursively contained sub-sequences
    (iterables).

    Examples:
    >>> [1, 2, [3,4], (5,6)]
    [1, 2, [3, 4], (5, 6)]
    >>> flatten([[[1,2,3], (42,None)], [4,5], [6], 7, MyVector(8,9,10)])
    [1, 2, 3, 42, None, 4, 5, 6, 7, 8, 9, 10]"""

    result = []
    for el in x:
        #if isinstance(el, (list, tuple)):
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result
	
def download(filename):

	#temporary debugging
	#import pdb
	#pdb.set_trace()
	
	base = "http://data.nba.com/json/cms/noseason"

	#date format:  YYYYMMDD
	#date.strftime('%Y%m%d') will convert a datetime object to YYYYMMDD string.

	oneDay = datetime.timedelta(days=1)
	startDate = datetime.date(2014,10,30)
	endDate = datetime.date.today()
	currentDate = startDate
	
	f = open(filename, 'a')
	periodPbpList = []
	
	while currentDate < endDate:
		#cycle through dates - find list of gameIDs from scoreboard JSON for each day.
		sbUrl = base + '/scoreboard/' + currentDate.strftime('%Y%m%d') + '/games.json'
		# This produces a list of gameIDs on this specific date.
		gameID = jsonSBOpener(sbUrl)

		if gameID != 'SBError':			
			#now, with the list of gameIDs, cycle through each game (and each period) to download the pbp JSON.
			while len(gameID) != 0:
				gameIDSingle = str( gameID.pop() )
				for period in [1,2,3,4]: #not sure what do to about OT - how are they signified in the JSON filename?
					pbpUrl = base + '/game/' + currentDate.strftime('%Y%m%d') + \
						'/' + gameIDSingle + '/pbp_' + str(period) + '.json'
						
					periodPbpList.append( json2list(pbpUrl,period) )
					#periodPbpList is a list of that quarters pbp data: 
					#list is [gameDate,gameID,period,lPlay]

					if (int(gameIDSingle[-2:]) % 10) == 0 and period == 4:
						print currentDate.strftime('%Y%m%d') + ' ' + gameIDSingle + \
							' ' + str( period )

			currentDate += oneDay
		else: #no games on this day. move to next.
			currentDate += oneDay

	pickle.dump(periodPbpList,f)
	f.close()	
	return periodPbpList