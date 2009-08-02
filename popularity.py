#!/usr/bin/env python
"""naive recommender based on popularity"""

repos = 123344
counts = [ (0, None) ]*(repos+1)

for l in open("data/data.txt"):
    user, repo = [ int(x) for x in l.split(":") ]
    counts[repo] = ( counts[repo][0]+1, repo )

counts.sort(key = lambda x: x[0], reverse = True)
popular = ",".join([ str(x[1]) for x in counts[:10] ])

r = open("results.txt", "w")
for l in open("data/test.txt"):
    r.write(l.strip()+":"+popular+"\n")
