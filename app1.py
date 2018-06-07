from pycricbuzz import Cricbuzz
import re
import sched, time
import os
from threading import Timer
import subprocess

s = sched.scheduler(time.time, time.sleep)

previous_run = 0;
previous_wicket=0

def do_something(sc): 
	print "Doing stuff..."
	global previous_run
	global previous_wicket
	
    # do your stuff

	c = Cricbuzz()
	matches = c.matches()
	for match in matches:
		print match
		if(match['srs'] == 'Indian Premier League, 2018'):
			# print match
			score = c.livescore(match['id'])['batting']['score']
			print score
			print c.commentary(match['id'])
			runs = int(score[0]['runs'])
			wicket = int(score[0]['wickets'])
			overs = (score[0]['overs'])
			print "---------------------"
			break
	
	diff_wicket = wicket - previous_wicket
	print "Diff wicket" + str(diff_wicket)
	if(diff_wicket>0):
		print "OUTTTTTTT"
		timer_video("Out", overs)
		
	diff_runs = runs - previous_run
	print "Diff Runs " + str(diff_runs)
	if(diff_runs>=4):
		print 4
		timer_video("Boundry",overs)
		## do something
	elif(diff_runs==3):
		print 3
		## do another thing
	elif(diff_runs==2):
		print 2
		## do third thing
	elif(diff_runs==1):
		print 1
	
	previous_run = runs
	previous_wicket = wicket
	s.enter(2, 1, do_something, (sc,))

def timer_video(str1,str2):
	filename = str1+"_"+str2
	timer = 270.0
	t1 = Timer(timer, download_video,[filename])
	t1.start() # after 30 seconds, "hello, world" will be printed
	
def download_video(arg):
	print "hello, world"
	
	print arg
	
	stream_url = 'https://hssports22-i.akamaihd.net/hls/live/642231/ipl2018e1/ENGM13KKRDD16APRIL/lr_Layer4/lr_Layer4.m3u8'

	download_command_interval= "ffmpeg -i " + stream_url +" -c copy -flags +global_header -f segment -segment_time 60 -segment_format_options movflags=+faststart -reset_timestamps 1 test%d.mp4"
	video_filename = "MyVideo"
	download_command_duration= "ffmpeg -i " + stream_url +" -t 60 -y -c:a copy "+ arg +".mp4"

	subprocess.Popen(download_command_duration)
	

s.enter(2, 1, do_something, (s,))
s.run()