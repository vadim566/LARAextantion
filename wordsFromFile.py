#author David Musaev 27/11/2021 ver 1.0 python 3.9
#This pyScript will prefix strings inside files in dirctory you will choose matching to condition
import os
import sys
import inspect
from os import listdir
from os.path import isfile,join

#returning a list with files in dir_path
def getWords(dir_path,prefix_word):
    try:
        files_in_dir=[f for f in listdir(dir_path) if isfile(join(dir_path,f))]
    except:
        "something wrong with the directory, put in the full path"
    finally:
        word_list=[]
        for file_name in files_in_dir:
            if prefix_word+'_' in file_name:
                word_list.append(file_name.split(file_name+'_', 1)[1])
        return word_list


