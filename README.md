Checkoutapp-Scripts
===================

End-user scripts for point-of-sale software Checkout.app


backup.py 
----------


This script can make a backup of a Checkout store. This script can run independently of the Checkout application, but has the following requirements:

* a running Checkout.app (perhaps on a separate computer). There is no need to log in to a specific store.

* Python 2.6 or 2.7.

* postgresql 8.3, included in Checkout.app or installed manually

The output file is  .checkoutbackup file that is compressed with gzip and can be used in the "Manage Checkout Store..." interface to restore your store.

Preparation steps:

* Open Terminal.app.
* If Checkout.app is not installed in /Applications/, the postgresql 8.3 "bin" directory must be in the PATH environment variable:

    `export PATH=/Applications/Checkout.app/Contents/Resources/postgres83/bin:$PATH`

Now your are ready to run the backup script:

    python backup.py "My Store name" ~/testbackup.checkoutbackup
    
If you wish to automate the backup, running it once-a-day for example, you can use cron, or use the GUI application [Cronnix](http://code.google.com/p/cronnix/) to set it up.
  