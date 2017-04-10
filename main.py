import os, os.path
import sys
import shutil
import glob
import datetime
import cPickle
import click
import re
import difflib
import ntpath
import webbrowser

@click.group()
def donna():
    pass

@donna.command()
def init(**kwargs):
	"creates two folders one for staging and one for committing"
	try:
		os.mkdir('commit/')
		os.mkdir('stage/')
		os.mkdir('versions/')
		file_path_commit = os.path.join(os.getcwd(),'commit')
		log = os.path.join(file_path_commit,'commit_log.p')
		target = open(log,'wb')
		target.close()
		file_path_commit = os.path.join(os.getcwd(),'versions')
		log = os.path.join(file_path_commit,'version_log.p')
		target = open(log,'wb')
		target.close()
	except OSError as e:
		print e
		print "Error"
	
@donna.command()
@click.argument('files', nargs=-1)
def stage(files):
	"moves files added to the stage into a new folder stage"
	try:
		for file in files:
        	
			full_name = os.path.join(os.getcwd(),file)
			print file
			print full_name
			# print os.path.isfile(full_name)
	    	
		    	if (os.path.isfile(full_name)):
		     		print "yes" + full_name
     				shutil.copy(full_name, os.path.join(os.getcwd(),'stage',file))
		     	else:
		     		print "no"+ full_name
	except OSError as e:
	   	print e

@donna.command()
@click.argument('msg')
def commit(**kwargs):
	"commit files from the stage into a new folder commit"
	try:
		version_file_path = os.path.join(os.getcwd(),'versions/version_log.p')
		f=open(version_file_path,"r+b")
		luck=0
		try:
			dict3=cPickle.load(f)
		except EOFError as e:
			luck =1
		f.close()
		f=open(version_file_path,"r+b")
		max3=0
		present_version=0
		if(luck==1):
			present_version = 1
		else:
			ndict1=cPickle.load(f)
			max3=len(list(ndict1))
			current_version = max3
			present_version = current_version + 1
		f.close()
		version_path = os.getcwd()+'/versions/v_'+str(present_version)
		os.mkdir(version_path)
		luck1=0
		f1 = open(version_file_path,"r+b")
		ndict2={}
		try:
			ndict2=cPickle.load(f1)
		except EOFError as e:
			luck1 =1
		newDict1={}
		max1=0
		if luck1==1:
			max1=1
		else:
			max1=len(list(ndict2))+1
			newDict1.update(ndict2)
		key1=max1
		value1=str(present_version)+" "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M")+"\n"
		
		newDict1.update({key1:value1})
		f1.close()
		f1 = open(version_file_path,"w+b")
		cPickle.dump(newDict1,f1,-1)
		f1.close()
		stage_path = os.path.join(os.getcwd(),'stage')
		commit_path = os.path.join(os.getcwd(),'commit')
		files = os.listdir(stage_path)
		print files
		for each_file in files:
			shutil.copy(each_file, commit_path)
			shutil.copy(each_file, version_path)
		file_path_commit = os.path.join(os.getcwd(),'commit')
		log = os.path.join(file_path_commit,'commit_log.p')
		luck=0
		target = open(log,"r+b")
		ndict3={}
		try:
			ndict3=cPickle.load(target)
		except EOFError as e:
			luck =1
		newDict2={}	
		max2=0
		if luck==1:
			max2=1
		else:
			max2=len(list(ndict3))+1
			newDict2.update(ndict3)
		key2=max2
		value2=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")+str("  ")+kwargs['msg']+"\n"
		newDict2.update({key2:value2})
		target.close()
		target = open(log,"w+b")
		cPickle.dump(newDict2,target,-1)
		target.close()
	except OSError as e:
	   	print e

@donna.command()
@click.option('--log', prompt='To display commit log enter cl; To display version log enter vl; To display both enter vc', help='The log to display.')
def display(log):
	if log=="cl":
		disC()
	elif log=="vl":
		disV()
	elif log=="vc":
		disC()
		disV()
	else:
		print "Please enter valid option!"

@donna.command()
@click.argument('folder1')
@click.argument('folder2')	
def diff(**kwargs):
    dir1 = kwargs['folder1']
    dir2 = kwargs['folder2']
    in_dir1, in_dir2 ,in_dir3,in_dir4= compare_directories(dir1, dir2)
    f = open("1.html",'w')
    for relative_path in in_dir1:
        for relative_path2 in in_dir2:
            fn1 = open(os.path.join(os.path.dirname(__file__), dir1, relative_path))
            fn2 = open(os.path.join(os.path.dirname(__file__), dir2, relative_path2))
            fname1 = path_leaf(relative_path)
            fname2 = path_leaf(relative_path2)
            if(fname1 == fname2):
                fn1.flush()
                data1 = fn1.read()
                fn1.flush()
                data2 = fn2.read()
                data1 = data1.splitlines()
                data2 = data2.splitlines()
                d = difflib.HtmlDiff()
                diff = difflib.unified_diff(data1,data2, lineterm='')
                data3 = '\n'.join(list(diff))

                print >> f, d.make_file(data1,data2)
    print "Files present Only in Folder1"
    for relative_path in in_dir3:
        fn1 = open(os.path.join(os.path.dirname(__file__), dir1, relative_path))
        fn1.flush()
        fname1 = path_leaf(relative_path)
        print fname1
        data1 = fn1.read()
        fn1.flush()
        data2 = ""
        data1 = data1.splitlines()
        d = difflib.HtmlDiff()
        diff = difflib.unified_diff(data1,data2, lineterm='')
        data3 = '\n'.join(list(diff))
        print >> f, d.make_file(data1,data2)
    
    print "Files present Only in Folder2"
    for relative_path in in_dir4:
        fn2 = open(os.path.join(os.path.dirname(__file__), dir2, relative_path))
        fn2.flush()
        fname2 = path_leaf(relative_path)
        print fname2

        data2 = fn2.read()
        data1 = ""
        data2 = data2.splitlines()
        d = difflib.HtmlDiff()
        diff = difflib.unified_diff(data1,data2, lineterm='')
        data3 = '\n'.join(list(diff))
        print >> f, d.make_file(data1,data2)        
    f.close()
    webbrowser.open('file://' + os.path.realpath('1.html'))
def disC():
	version_file_path = os.path.join(os.getcwd(),'commit/commit_log.p')
	f=open(version_file_path,'rb')
	try:
		fileDict=cPickle.load(f)
		print "Commit Log"
		for i in list(fileDict):
			print fileDict[i]
	except EOFError as e:
			print ""
	f.close()
def disV():
	version_file_path = os.path.join(os.getcwd(),'versions/version_log.p')
	f=open(version_file_path,'rb')
	try:
		fileDict=cPickle.load(f)
		print "Version Log"
		for i in list(fileDict):
			print fileDict[i]
	except EOFError as e:
			print ""
	f.close()
def build_files_set(rootdir):
	    root_to_subtract = re.compile(r'^.*?' + rootdir + r'[\\/]{0,1}')
	    files_set = set()
	    for (dirpath, dirnames, filenames) in os.walk(rootdir):
	        for filename in filenames + dirnames:
	            full_path = os.path.join(dirpath, filename)
	            relative_path = root_to_subtract.sub('', full_path, count=1)
	            files_set.add(relative_path)
	    return files_set
def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def compare_directories(dir1, dir2):
    files_set1 = build_files_set(dir1)
    files_set2 = build_files_set(dir2)
    return (files_set1, files_set2, files_set1-files_set2, files_set2-files_set1)
if __name__ == '__main__':
    donna()
