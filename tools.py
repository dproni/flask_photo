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

def db(base=None, coll=None):
    conn = pymongo.Connection('localhost', 27017)
    if base and coll:
        base = conn[base]
        coll = base[coll]
        return coll

def getFromMongo(base='photos', coll=None, split=False, search=None):
    conn = pymongo.Connection('localhost', 27017)
    db = conn[base]
    coll = db[coll]
    if search:
        photo = [i for i in coll.find(search)]
    else:
        photo = [i for i in coll.find()]
    if split:
        collection = split_seq(photo, split)
    else:
        collection = photo
    conn.close()
    return collection

