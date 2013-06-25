<?php

include "conf/config.php";
include "db.php";

$relstring = "rel. 0.1.3.0";
$relbuild  = "build 2013-06-20";
$themepath = $basedir . "/themes/" . $theme;
$language = $deflanguage;

# check for cookie language
if (isset($_COOKIE['language']))
{
    # check for file presence
    $tmplanguage = $_COOKIE['language'];
    if (file_exists($basedir . "/langs/" . $tmplanguage . ".php"))
    {
        $language = $tmplanguage;
    }
}


# chech for language file presence and include it
if (file_exists($basedir . "/langs/" . $language . ".php"))
{
    # language file exist  
    include $basedir . "/langs/" . $language . ".php";
}
else 
{
    # language file doesn't exists
    exit("selected language file <b>" . $basedir . "/langs/" . $language . ".php" 
         . "</b> doesn't exists, please check config file conf/config.php");    
}



# chech for theme folder presence
if (!file_exists($themepath))
{
    # theme folder doesn't exists
    exit("selected theme folder <b>" . $themepath . "</b> " 
         . "doesn't exists, please check config file conf/config.php");
}



# try to connect for db file
# Init_DB();


?>