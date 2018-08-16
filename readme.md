# CloudShell Resource Inspector

## Purpose

This is a simple command line tool geared towards CloudShell Admins.  

The primary use case is to quickly look up a CloudShell resource and determine current status, 
reservations associated with, and attribute information on the device; including the option to decrypt stored passwords values.  

By pushing it to a command line interface, it removes the need to open or otherwise run the Resource Manager program.
As a python script, it's easy to integrate into whatever the preferred user platform is.  

This is a **Read-Only** for devices.  

## Sample Print Out
```bazaar
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
NYC_01
> Status: Reserved
> Domains: AMR
> Address: 110.10.11.101                               > Full Address:                                        
> Family: CS_ComputeServer                             > Model: GenericServer                                 
> Folder Path: Servers/Dev
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
Total Reservations: 4

Name: Daily_build_1                      Owner: jcruz
  - Status: STARTED                      Start: 2018-05-24 17:15 UTC      End: 2018-05-24 19:25 UTC
  - ID: c8e3889b-bcdd-4c5f-85cc-0450837a4567
Name: Daily_build_1                      Owner: jcruz
  - Status: PENDING                      Start: 2018-05-25 17:15 UTC      End: 2018-05-25 19:15 UTC
  - ID: 32b50857-0b75-41a0-8ccc-04acf39abf20
Name: Daily_build_1                      Owner: jcruz
  - Status: PENDING                      Start: 2018-05-26 17:15 UTC      End: 2018-05-26 19:15 UTC
  - ID: bea2c45c-ab94-4d7e-907d-118a695fa046
Name: Daily_build_1                      Owner: jcruz
  - Status: PENDING                      Start: 2018-05-27 17:15 UTC      End: 2018-05-27 19:15 UTC
  - ID: 2d12bb98-edf6-438c-aa9c-bb85c1495d0a
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
Attributes:

- Location:                                            - Model:                                               
- Vendor:                                              - Backup Location:                                     
- Backup Password: <**!**>                             - Backup Type: File System                             
- Backup User:                                         - CLI Connection Type:                                 
- CLI TCP Port: 0                                      - Console Password: <**!**>                            
- Console Port: 123                                    - Console Server IP Address:                           
- Console User:                                        - Contact Name:                                        
- Disable SNMP: False                                  - Enable Password: <**!**>                             
- Enable SNMP: False                                   - OS Architecture:                                     
- OS Distribution:                                     - OS Type: Ubuntu                                      
- OS Version: 10.15                                    - Password: <**!**>                                    
- Power Management: True                               - SNMP Read Community: <**!**>                         
- SNMP V3 Password: <**!**>                            - SNMP V3 Private Key:                                 
- SNMP V3 User:                                        - SNMP Version: v2c                                    
- SNMP Write Community: <**!**>                        - Sessions Concurrency Limit: 1                        
- Storage Capacity:                                    - System Name:                                         
- User: root                                           - Tag:                                                 
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
```

## Data read out

There are 3 sections for the base query:
1. Summary
2. Reservations
3. Attributes

### Summary
The Name will be listed first followed by these entries:
- Status:  Available, Reserved, Excluded
- Domains:  A list of domains that the resource belongs to
- Address:  Short address (it's specific address)
- Full Address:  Includes parent address information
- Family:  Which family type the resource belongs to
- Model:  Which model type (of above family) the resource belongs to
- Folder Path:  The current folder path in CloudShell the resource is located

### Reservations
The Reservation Section will return the total number of Current and Future Reservations for the resource, looking forward 30 days.  
If there are no current or future reservations, the system will only return one line:  
`Total Reservations: 0`  
Otherwise the `Total Reservations: X` will return with a series of entries for each reservation that the resource participates in.  
Entries will be displayed in ascending order by start time.  In our example print out there are 4 entries.  
Initially the number of entries displayed is limited to the first 5.  
However there is an optional flag to display all Reservations Entries (`-x`).  

Each Reservation Block contains the following items:  
- Name: Name of the reservation, as displayed in CloudShell
- Status: Current status of the reservation (Pending, Started, Setup, Teardown) 
*Key to identifying possible suck reservations when combined with 'End Time' 
- Start:  Scheduled start time of the reservation, ISO8601 (YYYY-MM-DD HH:MM), all times UTC
- End: Scheduled end time of the reservation, ISO8601 (YYYY-MM-DD HH:MM), all time UTC
- ID: UUID of the reservation, allows for copy paste lookups

### Attributes
The final section will display all attributes listed on the resource.  
It will list all attributes by a short name, and their current value.  
All password type attributes by default list all values as `<**!**>`, even if blank.  

Attribute names are sorted by full name.

+ **Full Name vs. Short Name:**  
     With the introduction of Gen2 Shells, attributes were given unique name spaces based on source.  
     All Gen2 Attributes names are `source_name.attribute_name`.   
     Example: `CS_ComputeServer.Vendor` is used to store the vendor name.  
     The source prefix is either the Family or Model name, depending upon the origin.  
     Models inherit attributes from the their Family.    
     In Gen1 Shells and items created directly in Resource Manager, attribute names do not have a source prefix.  
     Attributes are sorted by the long name, but display only as short name.  
     This really only effect resources based on Gen2 shells, in that names will be sorted in 2 blocks.  
     The example print out is of a Gen2 based resource.

## Options
The inspector can also be run with a number of options.

+ -h:  **H**elp Menu
+ -b:  **B**rief Mode, will only return the Summary Block
+ -a:  **A**ttributes added to Brief Mode
+ -k:  **K**imono, open kimono mode decrypting attribute values
+ -r:  **R**eservations added to Brief Mode
+ -x:  e**X**tended list of current and pending reservations (shows all for 30 days), default is the first 5
+ -c:  **C**onfiguration, returns the current configuration setting for the script (password value masked)
+ -s:  **S**et a parameter with in the Configuration
    + host:  Host Name or IP of the CloudShell instance to be used
    + user:  Admin User name to use
    + password:  Associated Password to be used
    + port:  Port ID for the CloudShell API (8029 is default)
    
### Usages:  

+ standard look up for a device named *NYC_01*: 
    > `python csinspect.py NYC_01`
+ standard look up for a devices with the address of *110.10.11.101*:
    > `python csinspect.py 110.10.11.101`
+ brief style look up:
    > `python csinspect.py NYC_01 -b`     
+ standard look up with decrypted password values:
    > `python csinspect.py NYC_01 -k`
+ standard look up with extended list of reservations:
    > `python csinspect.py NYC_01 -x`
+ brief look up with reservations added:
    > `python csinspect.py NYC_01 -b -r`
+ brief loop up with extended list of reservations added:
    > `python csinspect.py NYC_01 -b -x`
+ brief look up with attributes added:
    > `python csinspect.py NYC_01 -b -a`
+ brief look up with attributes and decrypted password values:
    > `python csinspect.py NYC_01 -b -a -k`
+ help menu:
    > `python csinspect.py -h`
+ show configurations:
    > `python csinspect.py -c`
+ set configurations:
    > `python csinspect -s host localhost -s user admin -s password d0ubl3S3cre7 -s port 9425`