INTRODUCTION:
------------

This module contains script files to create a domain.


REQUIREMENTS:
------------

This module requires the following modules:

  * Python 3 Libraries
  * requests
  * sys
  * json
  * time

 * The scripts must be run outside sddc-manager environment.

 * DNS resolution must be done for sddc-manager.


USAGE:
-----

Sample specification file "domain_creation_spec_vxrail.json" will be used for domain creation operation.
For more information on the provided sample file, please refer to API reference documentation.

Usage:  python create_domain.py <hostname> <username> <password>
