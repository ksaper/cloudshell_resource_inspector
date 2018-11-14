#!/usr/bin/env python
from core import CloudShellResourceInspector, LBREAK
from cascade import Cascade
import sys


local = CloudShellResourceInspector()

# print '~~~~~~~~~~~~~~~~~'
# print sys.argv
# print '~~~~~~~~~~~~~~~~~'

tar = ''
has_tar = False
ready = True
set_configs = False
show_configs = False
flags = dict()
args = sys.argv
# args = 'csinpsect.py NYC_01 -k'.split(' ')

if '-h' in args:
    print LBREAK
    Cascade().print_help()
    print LBREAK
else:
    try:
        x = 1
        while x < len(args):
            current_item = args[x].upper()
            if '-' in current_item:
                if 'S' in args[x].upper():
                    set_configs = True
                    x += 1
                    flags[args[x].upper()] = args[x+1]
                    x += 2
                elif 'C' in current_item:
                    show_configs = True
                    x += 1
                else:
                    my_key = args[x].split('-')[1]
                    flags[my_key.upper()] = True
                    x += 1
            else:
                tar = args[x]
                has_tar = True
                x += 1

    except StandardError as err:
        ready = False
        print LBREAK
        print 'Input Error'
        print err.message

if ready:

    # print '~~~~~~~~~~~~~~~~~~~~~'
    # print flags
    # print '~~~~~~~~~~~~~~~~~~~~~'

    local.set_flags(open_k=flags.get('K', False), long_form=not(flags.get('B', False)),
                    atts=flags.get('A', False), show_res=flags.get('R', False),
                    show_all_res=flags.get('X', False))
    if set_configs:
        local.modify_configs(host=flags.get('HOST', ''), user=flags.get('USER', ''),
                             password=flags.get('PASSWORD', ''), port=flags.get('PORT', ''))
    if show_configs:
        local.print_config()

    if has_tar:
        local.session = local.open_session()
        # my_device = local.look_for(tar)
        local.run_main(tar)
    else:
        '!- Error:  No search term available'
    # except StandardError as err:
    #     print '!- Error Stopped'
