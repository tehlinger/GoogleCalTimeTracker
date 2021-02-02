import datetime
import pprint

def load():
    with open("heures.txt","r") as f:
        l = f.readlines()
        return l

def load_data():
    with open("filtered.txt","r") as f:
        l = f.readlines()
        return l

def is_useful(s):
    return (("DTSTART" in s) or\
    ("DTEND" in s) or\
    ("SUMMARY" in s) or\
    ("DESCRIPTION" in s))

def filter_data(l):
    return [i for i in l if is_useful(i)]

def extract_class(string_list):
    res = {}
    res[]

def get_only_classes(l):
    i = 0
    #for i in range(0,len(i),4):
    for i in range(0,12,4):
        class_data = l[i:i+4]
        pprint.pprint(class_data)
        print("===")

def rewrite_data():
    l = load()
    l = filter_data(l)
    with open("filtered.txt","w+") as output:
        output.writelines(l)

def get_classes():
    l = load_data()
    l = get_only_classes(l)

get_classes()
