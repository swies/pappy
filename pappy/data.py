from os.path import *

class Data(object):
    datadir = join(dirname(dirname(__file__)), "data")
    max_user = 56554
    max_repo = 123344

    def __init__(self):
        self.user_repos = []
        for i in range(self.max_user+1):
            self.user_repos.append([])

        self.repo_users = []
        for i in range(self.max_repo+1):
            self.repo_users.append([])

        for l in open(join(self.datadir, "data.txt")):
            user, repo = [ int(x) for x in l.split(":") ]
            self.user_repos[user].append(repo)
            self.repo_users[repo].append(user)

        self.popular_repos = []
        for i in range(len(self.repo_users)):
            self.popular_repos.append( (self.numusers(i), i) )
        self.popular_repos.sort(reverse = True)

    def numusers(self, repo):
        return len(self.repo_users[repo])
