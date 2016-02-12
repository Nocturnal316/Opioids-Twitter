# make_at_multidigraph.py
# by Chris Homan
#
# Constructs a directed multiedge graph on Twitter users, where each
# edges edge is a message from user1 with a mention of user2 ("@user2").
#
# usage:
# python make_at_multidigraph.py JSON_FILE
# E.g.
# python make_at_multidigraph.py oneyear.filtered.json

import nltk
import sys
import re
import json
import networkx as nx
import pickle

G = nx.MultiDiGraph()            
def main():
    lmtzr = nltk.stem.wordnet.WordNetLemmatizer()
    
    # Add nodes in the graph
    f = file (sys.argv[1])
    while True:
        line = f.readline()
        if line == "":
            break
        j = json.loads(line)
        G.add_node(j["user"]["screen_name"])
    
    # Add a multi-edge for each @
    f.seek (0)
    
    while True:
        line = f.readline()
        if line == "":
            break
        j = json.loads(line)
        
        tokens = nltk.word_tokenize(j["text"].encode('ascii', 'ignore') )
        for i, x in enumerate(tokens):
            try:
                if x == "@":
                    from_user = j["user"]["screen_name"]
                    to_user = tokens[i+1]
                    if to_user in G and from_user in G and to_user != from_user:
                        G.add_edge (from_user, to_user, tokens = tokens)
            except IndexError:
                pass
        
    f.close()

    f = file ("at_multidigraph.pkl", "w")
    
    pickle.dump(G, f)

    f.close()
    
if __name__ == "__main__":
    main()
