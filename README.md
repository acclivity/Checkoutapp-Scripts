Checkoutapp-Scripts
===================

End User scripts for the software Checkout.app


backup.py 
----------


This script can make a backup of your checkout database. This script is independent of the Checkout application, but has the following requirements:

* Your checkout application must be running, but no need to be logged into a store.

* Python 2.6 or higher.

* The script needs access to the Postgresql 8.3 that is embedded in the Checkout.app application.

The output file will be a compatible .checkoutdatabase file that is compressed with gzip, but can be used in the Manage Checkout Store... feature to restore your store.

How do I run the script:

* Open the Apple Terminal.app.
* First let the terminal know where the PostgreSQL 8.3 is located, you can do this right here in the terminal app or you can add it to your ~/.bashprofile.

    `PATH=/Applications/Checkout.app/Contents/Resources/postgres83/bin:$PATH`

* Setup the login for the PostgreSQL **admin** user by doing the following:
 
    `touch ~/.pgpass >> localhost:5505:*:admin:admin`
    
  This script will create for the current logged in user, the file ~/.pgpass and add a line localhost:5505:*:admin:admin, in case the file exist it will append the line to the end.
  You have to run this command only once.
  
Now your are ready to run the backup script:

    python backup.py "My Store name" ~/testbackup.checkoutbackup
    
In case you want to automate the backup and would like to run it once a day for example you can use cron, or use the GUI application [Cronnix](http://code.google.com/p/cronnix/) to set it up.
  