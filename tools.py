import random
import pymongo


def split_seq(seq, size):
    newseq = []
    random.shuffle(seq)
    while seq:
        temp_seq=[]
        for i in range(size):
            if seq:
                value = seq.pop()
                temp_seq.append(value)
        newseq.append(temp_seq)
    return newseq

def getFromMongo(base='photos', coll=None, split=False):
    conn = pymongo.Connection('localhost', 27017)
    db = conn[base]
    coll = db[coll]
    photo = [i for i in coll.find()]
    if split:
        collection = split_seq(photo, split)
    else:
        collection = photo
    conn.close()
    return collection

