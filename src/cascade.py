class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


class Cascade(object):
    def __init__(self):
        pass

    def print_help(self):
        print 'Help Menu:'
        print 'Basic Usage, enter either a Device Name or Address and it will perform a look-up '
        print 'in your CloudShell Installation for said device'
        print 'Flags:'
        print ' -h :  print this {}{}{}elp menu'.format(color.BOLD, 'H', color.END)
        print ' -b :  {}{}{}rief form, will only return base details of the device'.format(color.BOLD, 'B', color.END)
        print ' -a :  show {}{}{}ttributes, option to add to a brief version'.format(color.BOLD, 'A', color.END)
        print ' -k :  open {}{}{}imono, will decrypt password type attribute values'.format(color.BOLD, 'K', color.END)
        print ' -r :  show {}{}{}eservation details, option to brief version'.format(color.BOLD, 'R', color.END)
        print ' -x :  e{}{}{}tended reservation list, displays all for the next 30 days (default is 5 entries)'.format(color.BOLD, 'X', color.END)
        print ' -c :  {}{}{}onfiguration, will show current connection configuration'.format(color.BOLD, 'C', color.END)
        print ' -s :  {}{}{}et configuration by option:'.format(color.BOLD, 'S', color.END)
        print '       Configuration Options:'
        print "       'host x' set CloudShell host name/address to x"
        print "       'user x' set CloudShell user name to x for login"
        print "       'password x' set CloudShell user password to x for login"
        print "       'port x' set CloudShell API Port ID"
        print '         Example:'
        print '         > python csinspect.py -s host localhost -s user admin -s password admin -s port 9425'
