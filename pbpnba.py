# module containing various functions for parsing nba play-by-play (pbp) data
import json
import pylab
import matplotlib
import urllib2
import pickle

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
	
def score_plot(playList):
	clock,homeScore,awayScore = [],[],[]

	for p in playList:
		dPlaySingle = p

		clock.append( import_time( dPlaySingle['clock'] ) )
		homeScore.append( int( dPlaySingle['home_score'] ) )
		awayScore.append( int( dPlaySingle['visitor_score'] ) )
		
	matplotlib.pyplot.plot(clock,homeScore,clock,awayScore)
	
def json2list(url,period):
	# takes in url of json, and outputs a list of :
	# {gameDate,gameID,period,lPlay}
	req = urllib2.Request(url)
	opener = urllib2.build_opener()
	f = opener.open(req)
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
	
