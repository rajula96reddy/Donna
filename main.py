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
import ast

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
    compare_files(dir1, dir2)
    
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

def compare_files(direc1,direc2):
    in_dir1, in_dir2 ,in_dir3,in_dir4= compare_directories(direc1, direc2)
    f = open("1.html",'w')
    lst = []
    files_added = []
    files_removed = []
    # print "Files present in only Folder1:"
    for relative_path in in_dir1:
        flag=0
        for relative_path2 in in_dir2:
            p1 =  os.getcwd() + '/' + direc1  + '/' + relative_path
            p2 =  os.getcwd() + '/' + direc2  + '/' + relative_path2
            # print p1
            if(os.path.isfile(p1) and  os.path.isfile(p2)):
                fn1 = open(os.path.join(os.path.dirname(__file__), direc1, relative_path))
                fn2 = open(os.path.join(os.path.dirname(__file__), direc2, relative_path2))
                fname1 = path_leaf(relative_path)
                fname2 = path_leaf(relative_path2)
                if(fname1 == fname2):
                    lst.append(fname2)
                    fn1.flush()
                    flag=1
                    data1 = fn1.read()
                    fn1.flush()
                    data2 = fn2.read()
                    data1 = data1.splitlines()
                    data2 = data2.splitlines()
                    d = difflib.HtmlDiff()
                    diff = difflib.unified_diff(data1,data2, lineterm='')
                    data3 = '\n'.join(list(diff))
                    # list1=list2=list3=list4=[]
                    list1 = Number_of_Functions(p1)
                    list2 = Number_of_Functions(p2)
                    list3,list4 = diff_functions(list1,list2)
                    # print p1
                    # print p2
                    # print dir1,dir2
                    # print dir1 +'/'+fname1
                    # print list1,list2
                    # print list3,list4
                    if(len(list4)>0):
	           			print "Functions removed in " + fname1
	           			# print list4
	           			for i in list4:
	           				print '- '+ i
					if(len(list3) > 0):
						print "Functions added in " + fname1
						for i in list3:
							print '+ ' + i                    
                    print >> f, d.make_file(data1,data2)
        p1 =  os.getcwd() + '/' + direc1  + '/' + relative_path
        if(os.path.isfile(p1) and flag != 1):
            fn1 = open(os.path.join(os.path.dirname(__file__), direc1, relative_path))
            fn1.flush()
            fname1 = path_leaf(relative_path)
            # print fname1
            files_removed.append(fname1)
            data1 = fn1.read()
            fn1.flush()
            data2 = ""
            data1 = data1.splitlines()
            d = difflib.HtmlDiff()
            diff = difflib.unified_diff(data1,data2, lineterm='')
            data3 = '\n'.join(list(diff))
            print >> f, d.make_file(data1,data2)
            fn1.close()

    
    # print "Files present Only in Folder2"
    for relative_path in in_dir4:
        p2 =  os.getcwd() + '/' + direc2 + '/' + relative_path
        flag=0
        if(os.path.isfile(p2)):
            fn2 = open(os.path.join(os.path.dirname(__file__), direc2, relative_path))
            fn2.flush()
            fname2 = path_leaf(relative_path)
            for i in lst:
                if(i == fname2):
                    flag=1
            if(flag==0):
                # print fname2
                files_added.append(fname2)
                data2 = fn2.read()
                data1 = ""
                data2 = data2.splitlines()
                d = difflib.HtmlDiff()
                diff = difflib.unified_diff(data1,data2, lineterm='')
                data3 = '\n'.join(list(diff))
                print >> f, d.make_file(data1,data2)
                fn2.close()
    f.close()
    webbrowser.open('file://' + os.path.realpath('1.html'))
    if(len(files_added)>0):
    	print "Files Added"
    	for i in files_added:
    		print '+ ' + i
    if (len(files_removed)>0):
    	print "Files Removed"
    	for i in files_removed:
			print '- ' + i
def diff_functions(list1, list2):
    list_deletions = []
    list_additions = []
    for i in list1:
        if i not in list2:
            list_deletions.append(i)
    for i in list2:
        if i not in list1:
            list_additions.append(i)
    return list_additions,list_deletions

def Number_of_Functions(file1):
    array= []
    functions = []
    i = 0
    with open(file1, "r") as ins:
        for line in ins:
            if(len(line)>1 and ((line[0]==line[1]==" " or line[0]=='\t') or (line[0]=='\n' ))):
                array[i-1] = array[i-1] + line
                # print line
            else:
                # print line
                array.append(line)
                i = i+1
    # print len(array)
    # pprint(array)
    k=0
    for j in array:
        # j = raw_string(j)
        try:
            tree1 = ast.parse(j)
            for i in ast.walk(tree1):
                if isinstance(i,ast.FunctionDef):
                    # print (i.name)
                    functions.append(i.name)
        except:
            k = k+1
    # print len(functions)
    return functions 

if __name__ == '__main__':
    donna()
