import cloudshell.api.cloudshell_api as cs_api
from cloudshell.api.common_cloudshell_api import CloudShellAPIError

_host = 'qualias-maa-02.force10networks.com'
_user = 'admin'
_pwrd = 'admin'
_domm = 'Global'

target = 'MAA-S4810-3993'
BREAK = '=-'*56
try:
    session = cs_api.CloudShellAPISession(_host, _user, _pwrd, _domm)

    details = session.GetResourceDetails(target)
    dom_list = []
    for dom in details.Domains:
        dom_list.append(dom.Name)

    print BREAK
    print details.Name
    print '> Address: {}'.format(details.Address)
    print '> Full Add: {}'.format(details.FullAddress)
    print '> Family: {}'.format(details.ResourceFamilyName)
    print '> Model: {}'.format(details.ResourceModelName)
    print '> Folder: {}'.format(details.FolderFullPath)
    print '> Domains: {}'.format(', '.join(dom_list))
    print BREAK

    reservations = session.GetResourceAvailability(resourcesNames=[target]).Resources[0].Reservations
    print '# of Reservations: {}'.format(len(reservations))
    if len(reservations) > 0:
        for r in reservations:
            print '  {:26}  Owner:  {:16}  ID:  {}'.format(r.ReservationName, r.Owner, r.ReservationId)
            print '     Start: {:16}  End: {:16}'.format(r.StartTime, r.EndTime)
    print BREAK

    x = 0
    stop = len(details.ResourceAttributes)
    while x < stop:
        left = details.ResourceAttributes[x]
        left_msg = ''
        right_msg = ''
        if left.Type.upper() == 'PASSWORD':
            left_msg = '- {}: {}'.format(left.Name,
                                         session.DecryptPassword(left.Value).Value)
        else:
            left_msg = '- {}: {}'.format(left.Name, left.Value)

        x += 1

        if x < stop and len(left_msg) < 56:
            right = details.ResourceAttributes[x]
            if right.Type.upper() == 'PASSWORD':
                right_msg = '- {}: {}'.format(right.Name,
                                              session.DecryptPassword(right.Value).Value)
            else:
                right_msg = '- {}: {}'.format(right.Name, right.Value)

            x += 1

        print '{:55}{:55}'.format(left_msg, right_msg)

    print BREAK

except CloudShellAPIError as err:
    print err.message
