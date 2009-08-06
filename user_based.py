#!/usr/bin/env python
"""
recommendations by user similarity
"""

class Pappy(object):
    datafile = "data/data.txt"
    users = 56554
    repos = 123344

    def __init__(self):
        self.user_repos = []
        for i in range(self.users+1):
            self.user_repos.append([])

        self.repo_users = []
        for i in range(self.repos+1):
            self.repo_users.append([])

        for l in open(self.datafile):
            user, repo = [ int(x) for x in l.split(":") ]
            self.user_repos[user].append(repo)
            self.repo_users[repo].append(user)

        self.popular_repos = []
        for i in range(len(self.repo_users)):
            self.popular_repos.append( (len(self.repo_users[i]), i) )
        self.popular_repos.sort(reverse = True)

    def print_stats(self):
        mean_repos = sum([ len(rl) for rl in self.user_repos])/float(self.users)
        mean_users = sum([ len(ul) for ul in self.repo_users])/float(self.repos)
        print "mean repos per user:", mean_repos
        print "mean users per repo:", mean_users

    def similar_users(self, user):
        similar_users = {}
        for r in self.user_repos[user]:
            for u in self.repo_users[r]:
                similar_users[u] = True
        sim = []
        for u in similar_users.iterkeys():
            if u == user:
                continue
            sim.append( (self.similarity(user, u), u) )
        sim.sort(reverse = True)
        return sim

    def similarity(self, user, other):
        # let's try making that simple % common metric symmetric
        # current best!
        return ( self.common_repos(user, other)**2.0 ) / \
               ( len(self.user_repos[user]) * len(self.user_repos[other]) )

        # divides common repos by other count
        #return self.common_repos(user, other) / len(self.user_repos[other])
       
        #return self.jaccard(user, other)

        #return self.manhattan(user, other)

        #return self.new_similarity(user, other)
       
        # an odd attempt at a symmetric % common similarity
        #return ( 2.0 * self.common_repos(user, other) ) / \
        #       ( len(self.user_repos[user]) + len(self.user_repos[other]) )

        # % of our repos that other watches, real simple, but more
        # effective to divide by other count
        #return self.common_repos(user, other) / len(self.user_repos[user])

        #return self.common_repos(user, other)
        #return 1.0

    def jaccard(self, user, other):
        common = self.common_repos(user, other)
        userlen = len(self.user_repos[user])
        otherlen = len(self.user_repos[other])
        return common / ( userlen + otherlen - common )
    
    def manhattan(self, user, other):
        common = self.common_repos(user, other)
        userlen = len(self.user_repos[user])
        otherlen = len(self.user_repos[other])
        return userlen + otherlen - ( 2 * common )

    def new_similarity(self, user, other):
        """
        --- this is sort of a bust ---

        the idea here is that when doing a user-based recommendation we
        should find users whose whole watch list is quite similar to ours

        so let's take the fraction of user watches the other has
        and multiply by a control for the number of repositories watched

        it may also be good to limit to the first 10 or 20 similar users
        (after filtering for any 1.0 values) when generating recommendations
        if this metric doesn't go to zero fast enough
        """
        control_k = 1.0 # higher means slower rolloff
        diff = len(self.user_repos[user]) - len(self.user_repos[other])
        control = float(control_k)/(control_k + abs(diff))
        shared = self.common_repos(user, other) / len(self.user_repos[user])
        return control*shared

    def common_repos(self, user, other):
        """
        number of common repos between user and other
        """
        s = 0.0
        for r in self.user_repos[user]:
            if r in self.user_repos[other]:
                s += 1.0
        return s

    def recommend(self, user):
        repos = {}
        similar_users = self.similar_users(user)
        print len(similar_users), similar_users[:5]
        #similar_users = similar_users[:32]
        for sim, o in similar_users:
            for r in self.user_repos[o]:
                if repos.has_key(r):
                    repos[r].append(sim)
                else:
                    repos[r] = [ sim ]

        recs = []
        for r, sims in repos.iteritems():
            if r in self.user_repos[user]:
                continue
            recs.append( (sum(sims), r) )
        recs.sort(reverse = True)
        return recs

def main():
    p = Pappy()

    results = open("results.txt", "w")
    n = 0
    for l in open("data/test.txt"):
        u = int(l)
        recs = [ x[1] for x in p.recommend(u)[:10] ]
        for c, r in p.popular_repos: # pad with popular repositories
            if len(recs) >= 10:
                break
            if r not in recs and r not in p.user_repos[u]:
                recs.append(r)
        recs = recs[:10]
        results.write("%d:%s\n" % (u, ",".join([ str(x) for x in recs ])))
        n += 1
        print n

if __name__ == "__main__":
    main()
