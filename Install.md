## Dependencies to install ##
  * php5
  * php5-sqlite
  * php-net-socket
  * python-daemon
  * python-lockfile
  * pyusb
  * python-serial
> <br />

## Installation on Fedora/Mageia/OpenSUSE based distro ##

**ENGINE**
  * you need to install python dependencies, as above <br /> _python-daemon python-lockfile pyusb python-serial_

  * create folder for application files: <br />_# mkdir /var/sagent_

  * copy _engine_ contents files and folders under created folder _/var/sagent_ ( _sensors_ folder contains plugins python script that drive hardware sensor to read measure. _notifiers_ folder contains plugins python script used to notify out of range values)

  * copy _init\_script/sagentd_ into _/etc/init.d_ folder

  * give execute permission to file: <br /> _# chmod 775 /etc/init.d/sagentd_

  * verify that _SCRIPT\_FILE_ and _PID\_FILE_ parameters into _/etc/init.d/sagentd_ link correctly to the _agent.py_ python application script

  * add new service: <br /> _# chkconfig --add sagentd_

**WEB APP**

  * you need to install php dependencies, as above <br /> _php-socket php-pdo\_sqlite_

  * create _/var/www/webapps/sagent_ folder

  * copy files from _webapp_ to _/var/www/webapps/sagent_ folder

  * change owner of folder to apache user and group:<br /> _# chown -R apache:apache /var/www/webapps/sagent_

  * edit conf/config.php to configure parameters:<br /> _$basedir, $basevirtdir, $dbpath, $service\_host, $service\_port_

  * create under _/etc/httpd/conf/webapps.d/_ config file _sagent.conf_ with web application data as follow:<br />
```
     Alias /sagent "/var/www/webapps/sagent"

     <Directory "/var/www/webapps/sagent">
         Options Indexes FollowSymLinks
         Order allow,deny
         Allow from all
     </Directory>
```

  * restart apache service:<br /> _# service httpd restart_

  * if http://localhost/sagent have db access problem try to change permissions on db file:<br /> _# chmod 666 /var/tmp/sagent.sqlite_





<br />

## Installation on Debian/Ubuntu/Mint based distro ##

**ENGINE**
  * you need to install python dependencies, as above <br /> _python-daemon python-lockfile python-usb python-serial_

  * create folder for application files: <br />_# mkdir /var/sagent_

  * copy _engine_ contents files and folders under created folder _/var/sagent_ ( _sensors_ folder contains plugins python script that drive hardware sensor to read measure. _notifiers_ folder contains plugins python script used to notify out of range values)

  * copy _init\_script/sagentd_ into _/etc/init.d_ folder

  * give execute permission to file: <br /> _# chmod 775 /etc/init.d/sagentd_

  * verify that _SCRIPT\_FILE_ and _PID\_FILE_ parameters into _/etc/init.d/sagentd_ link correctly to the _agent.py_ python application script

  * add new service: <br /> _# update-rc.d sagentd defaults_

**WEB APP**
  * you need to install php dependencies, as above <br /> _php5 php5-sqlite php-net-socket_

> work in progress...


<br />