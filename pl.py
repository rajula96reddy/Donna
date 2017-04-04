import os
import re
import difflib
import ntpath
import webbrowser
import argparse

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
    parser = argparse.ArgumentParser()
    parser.add_argument("Folder1")
    parser.add_argument("Folder2")
    args = parser.parse_args()
    dir1 = args.Folder1
    dir2 = args.Folder2
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
    # print '\nFiles only in {}:'.format(dir2)
    # for relative_path in in_dir2:
        # print '* {0}'.format(relative_path)
    # print '\nFiles only in {}:'.format(dir2)
    # for relative_path in in_dir2:
        # print '* {0}'.format(relative_path)