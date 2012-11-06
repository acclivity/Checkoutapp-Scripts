Checkoutapp-Scripts
===================

End User scripts for the software Checkout.app


backup.py 
----------


This script can be called to make backup of your checkout database. This script is independent of the Checkout, but has the following requirements:

* Your checkout application must be running, but no need to be logged into a store.

* The script needs access to the Postgresql 8.3 that is embedded in the Checkout.app application.

The output file will be a compatible .checkoutdatabase file that is gzip compressed but can be used in the Manage Checkout Store... feature to restore your store.

How do I run the script:

* Open the Apple Terminal.app.
* First let the terminal know where the Postgresql 8.3 is located, you can do this right here in the terminal app or you can add it to your ~/.bashprofile.

    `PATH=/Applications/Checkout.app/Contents/Resources/postgres83/bin:$PATH`

* Setup for the user that is running the login for the **admin** user by doing the following:
 
    `touch ~/.pgpass >> localhost:5505:*:admin:admin`
    
  This script will create for the current logged in user, the file ~/.pgpass and add a line localhost:5505:*:admin:admin, in case the file exist it will append the line to the end.
  This command has to be runed only once for the user.
  
Now your are ready to run the backup script:

    python backup.py "My Store name" ~/testbackup.checkoutbackup
  