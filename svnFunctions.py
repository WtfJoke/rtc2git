import os
import configuration
import shouter
import shell
from gitFunctions import Commiter

class svnCommiter:

    @staticmethod
    def getcommitcommand(changeentry, comment):
        msg = (comment, "[RTC commit", changeentry.date, "by", changeentry.getgitauthor() + "]")
        return "svn commit -m %s" % (shell.quote(" ".join(msg)))

    @staticmethod
    def addandcommit(changeentry):
        config = configuration.get()
        if config.svnrepodir:
            shouter.shout("[SVN] current dir=%s svndir=%s" % (os.getcwd(), config.svnrepodir))
            # 1 - rsync current git dir to svn dir
            gitrepodir = os.getcwd()
            cmd = "rsync -r %s %s" % (
                os.path.join(gitrepodir, config.component2load, "*"),
                config.svnrepodir)
            shouter.shout("[SVN] %s" % cmd)
            shell.execute(cmd)
            # 2 - chdir to svnrepo, add and commit
            os.chdir(config.svnrepodir)
            cmd = "svn add --force * --auto-props --parents --depth infinity -q"
            shouter.shout("[SVN] %s" % cmd)
            shell.execute(cmd)
            comment = Commiter.getcommentwithprefix(changeentry.comment)
            cmd = svnCommiter.getcommitcommand(changeentry, comment)
            shouter.shout("[SVN] %s" % cmd)
            shell.execute(cmd)
            shell.execute("svn update")
            # 3 - go back to current dir
            os.chdir(gitrepodir)

