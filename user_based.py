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

    def print_stats(self):
        average_repos = sum([ len(rl) for rl in self.user_repos])/float(self.users)
        average_users = sum([ len(ul) for ul in self.repo_users])/float(self.repos)
        print "average repos per user:", average_repos
        print "average users per repo:", average_users

    def similar_users(self, user):
        similar_users = {}
        for r in self.user_repos[user]:
            for u in self.repo_users[r]:
                similar_users[u] = True
        del similar_users[user]
        sim = []
        for u in similar_users.iterkeys():
            sim.append( (self.similarity(user, u), u) )
        sim.sort(reverse = True)
        return sim

    def similarity(self, user, other):
        #return 1.0
        #return self.common_repos(user, other) / len(self.user_repos[user])
        return ( 2.0 * self.common_repos(user, other) ) / \
               ( len(self.user_repos[user]) + len(self.user_repos[other]) )

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
        #similar_users = similar_users[:10]
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
        recs = p.recommend(u)[:10]
        results.write("%d:%s\n" % (u, ",".join([str(x[1]) for x in recs])))
        n += 1
        #print n

if __name__ == "__main__":
    main()
