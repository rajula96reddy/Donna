import os, os.path
import argparse
import sys
import shutil
import glob
import datetime
def init():
	"creates two folders one for staging and one for committing"
	try:
		os.mkdir('commit/')
		os.mkdir('stage/')
		os.mkdir('versions/')
		file_path_commit = os.path.join(os.getcwd(),'commit')
		log = os.path.join(file_path_commit,'commit_log.txt')
		target = open(log,'w')
		target.close()
		file_path_commit = os.path.join(os.getcwd(),'versions')
		log = os.path.join(file_path_commit,'version_log.txt')
		target = open(log,'w')
		target.close()

	except OSError as e:
		print e
		print "Error"
		# e

def stage():
	"moves files added to the stage into a new folder stage"
	try:
		print sys.argv
		src_files = sys.argv[1:len(sys.argv)]
		print src_files
		for file in src_files:
			print file
			full_name = os.path.join(os.getcwd(),file)
			print full_name
			# print os.path.isfile(full_name)
	    	
		    	if (os.path.isfile(full_name)):
		     		print "yes" + full_name
     				shutil.copy(full_name, os.path.join(os.getcwd(),'stage',file))
		     	else:
		     		print "no"+ full_name
	except OSError as e:
	   	print e

def commit():
	"commit files from the stage into a new folder commit"
	try:
		version_file_path = os.path.join(os.getcwd(),'versions/version_log.txt')
		
		with open(version_file_path) as f:
			lines = f.readlines()
		if(len(lines)==0):
			present_version = 1
		else:
			current_version = int(lines[-1][0])
			present_version = current_version + 1
		version_path = os.getcwd()+'/versions/v_'+str(present_version)
		os.mkdir(version_path)
		f = open(version_file_path,'a')
		f.write(str(present_version)+" ")
		f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
		f.write("\n")
		f.close()
		stage_path = os.path.join(os.getcwd(),'stage')
		commit_path = os.path.join(os.getcwd(),'commit')
		# print file_path
		files = os.listdir(stage_path)
		print files
		for each_file in files:
			shutil.copy(each_file, commit_path)
			shutil.copy(each_file, version_path)
		    #  	else:
		    #  		print "no"+ full_name
		file_path_commit = os.path.join(os.getcwd(),'commit')
		log = os.path.join(file_path_commit,'commit_log.txt')
		target = open(log,'a')
		target.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")+str("  "))
		target.write(sys.argv[1])
		target.write("\n")
		target.close()


	except OSError as e:
	   	print e

def test():
	print sys.argv
	# print "I`am there"
	file_path = os.path.join(os.getcwd(),'commit')
	log = os.path.join(file_path,'commit_log.txt')
	target = open(log,'a')
	# date = os.popen('date')
	target.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")+str("  "))
	# target.write(" ")
	target.write(sys.argv[1])
	target.write("\n")
	target.close()
	print log

# parser= argparse.ArgumentParse()
# parser.add_argument("init")
# args = parser.parse_args()

# def __init__():
# stage()
# init()
# stage()
commit()
# test()