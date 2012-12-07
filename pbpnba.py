# module containing various functions for parsing nba play-by-play (pbp) data
import json
import pylab
import matplotlib
import urllib2
import pickle
import numpy


# function to convert unicode time remaining in pbp feed to 
# seconds elapsed.
def import_time(unicode_input):
	quarterLength = 12*60
	if len(unicode_input) == 0:
		# clock countdown has not started yet, time elapsed is 0.
		minute = 0
		second = 0
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
	d2 = d['sports_content']
	dGame = d2['game']
	
	
	# output of 'play' key of dGame is a list, not a dict.
	# individual plays are ordered 0..N
	lPlay = dGame['play']
	gameDate = dGame['date']
	gameID = dGame['id']
	listOutput = [gameDate, gameID, period, lPlay]
	return listOutput
	
def jsonSBOpener(url):
	# takes in url of scoreboard json, and outputs a list of gameIDs for that date.
	try:
		req = urllib2.Request(url)
		opener = urllib2.build_opener()
		f = opener.open(req)
		d = json.load(f)
		d2 = d['sports_content']
		d3 = d2['games']
		d4 = d3['game']
		gameID = []
		while len(d4) != 0:
			gameID.append( d4.pop()['id'] )
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
				clock.append( cTemp )
				homeScore.append( hTemp )
				awayScore.append( aTemp )
				d = pickle.load(fileID)
	#need adjust each period's clock, in order to have a total running game time.
	#then it can be flattened.
	#may require switching first to numpy.array() object.
	return (flatten(clock), flatten(homeScore), flatten(awayScore)) 		
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
