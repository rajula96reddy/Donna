import difflib
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("a")
parser.add_argument("b")
args = parser.parse_args()
# print args
with open(args.a,'r') as myfile1:
	data1 = myfile1.read()
	# print data1
with open(args.b,'r') as myfile2:
	data2 = myfile2.read()
	# print data2

data1 = data1.splitlines()
data2 = data2.splitlines()
d = difflib.HtmlDiff()
diff = difflib.unified_diff(data1,data2, lineterm='')
# print '\n'.join(list(diff))
data3 = '\n'.join(list(diff))
if(data3 == ""):
	print "Nothing has been changed.Please change something."
else:
	print "File:" + args.b + " has been modified"

f = open("1.html",'w')
print >> f, d.make_file(data1,data2)
f.close()

# for line in difflib.unified_diff(data1,data2,fromfile = args.a,tofile = args.b):
		# print line

