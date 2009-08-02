#!/usr/bin/env python
"""
less naive recommender based on popularity

doesn't recommend repos a user is already watching
"""

users = 56554
repos = 123344

user_watches = []
for i in range(users+1):
    user_watches.append([])
repo_watch_count = [ (0, None) ] * (repos+1)


maxuser = 0

for l in open("data/data.txt"):
    user, repo = [ int(x) for x in l.split(":") ]
    user_watches[user].append(repo)
    repo_watch_count[repo] = ( repo_watch_count[repo][0]+1, repo )

repo_watch_count.sort(reverse = True)
popular_repos = [ x[1] for x in repo_watch_count[:1000] ]

results = open("results.txt", "w")
for l in open("data/test.txt"):
    u = int(l)
    recs = []
    for r in popular_repos:
        if r not in user_watches[u]:
            recs.append(r)
        if len(recs) >= 10:
            break
    if len(recs) != 10:
        print "Ran out of popular repos for user %d (%d recs)!" % (u, len(recs))
    results.write("%d:%s\n" % (u, ",".join([str(x) for x in recs])))
