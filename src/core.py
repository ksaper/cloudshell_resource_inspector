from json import loads as json_loads
from json import dumps as json_dumps
import time
import logging
import cloudshell.api.cloudshell_api as cs_api
from cloudshell.api.common_cloudshell_api import CloudShellAPIError
from base64 import b64decode, b64encode

LOG_DICT = {"DEBUG": 10, "INFO": 20, "WARNING": 30, "WARN": 30, "ERROR": 40, "CRITICAL": 50, "CRIT": 50}
LBREAK = '{}='.format('=-'*55)
DEFAULT_RES_TO_DISPLAY = 5
FILTER_DICT = {"CUR": "Current", "FUTURE": "Future"}
MAX_RANGE = (30 * 24 * 60 * 60)  # 30 days in Seconds


class CloudShellResourceInspector(object):

    def __init__(self):
        self.config_file = ''
        self.open_k = False
        self.long_form = True
        self.show_attributes = False
        self.show_res = False
        self.show_all_res = False
        self.filter = ''
        self.config = self._initialize()
        self.session = None

    def _initialize(self, config_file='./src/config.json', log_file='./src/logs/csri.log',
                    log_level='ERROR'):
        """

        :param config_file:
        :return:
        """
        logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                            filename=log_file, level=LOG_DICT[log_level])

        self.config_file = config_file
        return json_loads(open(self.config_file).read())

    def open_session(self):
        """

        :return:
        """
        cs_session = None
        try:
            cs_session = cs_api.CloudShellAPISession(b64decode(self.config['host']),
                                                     b64decode(self.config['user']),
                                                     b64decode(self.config['pwrd']),
                                                     domain='Global',
                                                     port=str(self.config['port'])
                                                     )
        except CloudShellAPIError as err:
            logging.CRITICAL(err.message)

        return cs_session

    def set_flags(self, open_k=True, long_form=True, atts=True, show_res=True, filter='All', show_all_res=False):
        self.open_k = open_k
        self.long_form = long_form
        self.show_attributes = atts
        self.show_res = show_res
        self.show_all_res = show_all_res
        self.filter = FILTER_DICT.get(filter, 'Both')

    def print_config(self):
        print LBREAK
        print ' Inspector Configs:'
        print ' Host: {}'.format(b64decode(self.config['host']))
        print ' User: {}'.format(b64decode(self.config['user']))
        print ' Password: <**!**>'
        print ' Port: {}'.format(self.config['port'])
        print LBREAK

    def modify_configs(self, host='', user='', password='', port=''):
        changed = False
        if host != '':
            self.config['host'] = b64encode(host)
            changed = True
        if user != '':
            self.config['user'] = b64encode(user)
            changed = True
        if password != '':
            self.config['pwrd'] = b64encode(password)
            changed = True
        if port != '':
            self.config['port'] = int(port.strip())
            changed = True

        if changed:
            new_config = json_dumps(self.config, indent=4, separators=(',', ': '))
            with open(self.config_file, 'w') as f:
                f.write(new_config)
                f.close()
            print '!- Config Changed:'
            self.print_config()

    def look_for(self, term):
        key_term = ''
        address_lookup = None
        name_lookup = None
        try:
            name_lookup = self.session.FindResources(resourceFullName=term, exactName=False,
                                                     includeSubResources=False).Resources
        except CloudShellAPIError as err:
            logging.error(err.message)
        try:
            address_lookup = self.session.FindResources(resourceAddress=term, exactName=False,
                                                        includeSubResources=False).Resources
        except CloudShellAPIError as err:
            logging.error(err.message)

        if not name_lookup and not address_lookup:
            print 'Unable to locate "{}" resource by name or address'.format(term)
        elif len(name_lookup) == 1 and not address_lookup:
            key_term = name_lookup[0].FullName
        elif len(address_lookup) == 1 and not address_lookup:
            key_term = address_lookup[0].FullName
        elif len(name_lookup) > 1:
            names = []
            for each in name_lookup:
                names.append(each.FullName)
            print 'Multiple matches for {}'.format(term)
            print ', '.join(names)
        elif len(address_lookup) > 1:
            names = []
            for each in address_lookup:
                names.append(each.FullName)
            print 'Multiple matches for {}'.format(term)
            print ', '.join(names)
            
        return key_term

    def _time_to_ISO8601(self, dts_in):
        # in_tup = time.strptime(dts_in, '%m/%d/%Y %H:%M')
        # return time.strftime('%Y-%m-%d %H:%M', time.localtime(time.mktime(in_tup) - time.timezone))
        #
        date, time = dts_in.split(' ', 1)
        MM, DD, YYYY = date.split('/')
        return '%s-%s-%s %s UTC' % (YYYY, MM, DD, time)

    def _handle_password(self, value):
        val = '<**!**>'
        if self.open_k:
            val = self.session.DecryptPassword(value).Value
        return val

    def run_main(self, search_term=''):
        name = self.look_for(term=search_term)
        if name:
            try:
                details = self.session.GetResourceDetails(resourceFullPath=name)

                start_time = time.strftime('%d/%m/%Y %H:%M',
                                           time.localtime(time.mktime(time.localtime()) + time.timezone))
                stop_time = time.strftime('%d/%m/%Y %H:%M',
                                          time.localtime(time.mktime(time.localtime()) + time.timezone + MAX_RANGE))

                reservations = self.session.GetResourceAvailabilityInTimeRange(resourcesNames=[name],
                                                                               startTime=start_time,
                                                                               endTime=stop_time,
                                                                               showAllDomains=True
                                                                               ).Resources[0].Reservations

                dom_list = []
                for dom in details.Domains:
                    dom_list.append(dom.Name)

                status = []
                if details.Excluded:
                    status.append('EXCLUDED')

                for res in reservations:
                    res_status = self.session.GetReservationDetails(res.ReservationId).ReservationDescription
                    if res_status.Status.upper() != 'PENDING':
                        status.append('Reserved')
                        break

                print '\n{}'.format(LBREAK)
                print details.Name
                if len(status) > 0:
                    print '> Status: {}'.format(' '.join(status))
                else:
                    print '> Status: Available'
                print '> Domains: {}'.format(', '.join(dom_list))
                print '{:55}{:55}'.format('> Address: {}'.format(details.Address),
                                          '> Full Address:'.format(details.FullAddress))
                print '{:55}{:55}'.format('> Family: {}'.format(details.ResourceFamilyName),
                                          '> Model: {}'.format(details.ResourceModelName))
                print '> Folder Path: {}'.format(details.FolderFullPath)
            except StandardError as err:
                e_msg = 'Error in Core lookup:\n{}'.format(err.message)
                print e_msg
                logging.error(e_msg)

            # List Reservations
            if self.show_res or self.long_form or self.show_all_res:
                try:
                    print LBREAK
                    p_res_list = dict()

                    print 'Total Reservations: {}\n'.format(len(reservations))
                    for res in reservations:
                        # add filters
                        p_res_list[res.StartTime] = self.session.GetReservationDetails(res.ReservationId).\
                            ReservationDescription

                    i = 0
                    if self.show_all_res:
                        j = len(p_res_list.keys())
                    else:
                        if len(p_res_list.keys()) < DEFAULT_RES_TO_DISPLAY:
                            j = len(p_res_list)
                        else:
                            j = DEFAULT_RES_TO_DISPLAY

                    res_keys = sorted(p_res_list.keys())
                    while i < j:
                        k = res_keys[i]
                        print 'Name: {:33} Owner: {}'.format(p_res_list[k].Name, p_res_list[k].Owner)
                        print '  - Status: {:29}Start: {:25} End: {}'.format(p_res_list[k].Status.upper(),
                                                                             self._time_to_ISO8601(p_res_list[k].StartTime),
                                                                             self._time_to_ISO8601(p_res_list[k].EndTime))
                        print '  - ID: {}'.format(p_res_list[k].Id)
                        i += 1

                except StandardError as err:
                    e_msg = 'Error in Reservation retrieval:\n{}'.format(err.message)
                    print e_msg
                    logging.error(e_msg)

            # for attributes
            if self.show_attributes or self.long_form:
                print LBREAK
                print 'Attributes:\n'
                try:
                    attributes = sorted(self.session.GetResourceDetails(resourceFullPath=name).ResourceAttributes,
                                        key=lambda attribute: attribute.Name)
                    # attributes = self.session.GetResourceDetails(resourceFullPath=name).ResourceAttributes
                    x = 0
                    while x < len(attributes):
                        left_msg = ''
                        right_msg = ''

                        # do left side
                        left = attributes[x]
                        if left.Type.upper() == 'PASSWORD':
                            left_msg = '- {}: {}'.format(left.Name.split('.')[-1], self._handle_password(left.Value))
                        else:
                            left_msg = '- {}: {}'.format(left.Name.split('.')[-1], left.Value)
                        x += 1
                        # do right side
                        if x < len(attributes):
                            right = attributes[x]
                            if len(left_msg) < 55:
                                if right.Type.upper() == 'PASSWORD':
                                    right_msg = '- {}: {}'.format(right.Name.split('.')[-1], self._handle_password(right.Value))
                                else:
                                    right_msg = '- {}: {}'.format(right.Name.split('.')[-1], right.Value)
                                x += 1

                        print '{:55}{:55}'.format(left_msg, right_msg)
                except StandardError as err:
                    e_msg = 'Error in Attribute retrieval\n{}'.format(err.message)
                    print e_msg
                    logging.error(e_msg)

            # end line
            print '{}\n'.format(LBREAK)
            print ' -! Complete'
