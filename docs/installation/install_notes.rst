===============================================
Installation Notes
===============================================

Notes on how to install:

1. install all requirements in apt-packages.txt
2. install all requirements in requirements.txt (highly recommend that you have a virtualenv and use pip)
3. Make sure to set the Linux kernel overcommit memory setting to 1. Add vm.overcommit_memory = 1 to /etc/sysctl.conf and then reboot or run the command sysctl vm.overcommit_memory=1 for this to take effect immediately.
