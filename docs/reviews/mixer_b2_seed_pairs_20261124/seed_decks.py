"""Change exactly the two printed insert/pack seeds of each frozen B2 deck."""
import hashlib
import json
import re

ORIGINAL={"U":"b37974e5c0674947912e932c55517e9e84243293f29257183f8f70cc032f2fd7",
          "C":"d36d199388243ccd630cbd346cbcdb6f37bf8bb92ae9c8f4e73e2e98597a6a3e"}
SEEDS={"S2":49979687,"S3":67867967}

def sha(b):return hashlib.sha256(b).hexdigest()

def generate(module,raw,meta,arm):
    role=arm[-1]
    family=arm[:-1]
    seed=SEEDS[family]
    if sha(raw)!=ORIGINAL[role] or meta["deck_sha256"]!=sha(raw) or meta["seed"]!=32452843:
        raise ValueError("wrong original B2 bytes")
    if module["CAMPAIGN_SEEDS"]!=(32452843,*SEEDS.values()):
        raise ValueError("unknown generator seed series")
    insertion=(module["_insert_seed"](seed,"insA"),module["_insert_seed"](module["_next_prime"](seed+2),"insB"))
    deck=raw
    for label,prev,now in zip(("A","B"),(32452843,32452867),insertion):
        old=("fix ins%s all insert/pack seed %d distributiontemplate pdd%s"%(label,prev,label)).encode()
        new=("fix ins%s all insert/pack seed %d distributiontemplate pdd%s"%(label,now,label)).encode()
        if raw.count(old)!=1:raise ValueError("layered seed binding failed")
        deck=deck.replace(old,new)
    if len(re.findall(rb"^fix \S+ all insert/pack seed ",deck,re.M))!=2:raise ValueError("unexpected insertion")
    updated=dict(meta,seed=seed,deck_sha256=sha(deck),deck_bytes=len(deck))
    return deck,updated,insertion
