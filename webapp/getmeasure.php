<?php
error_reporting(E_ERROR);

include "conf/config.php";

$req=$_GET["m"] . "\r\n";

 
try
{
    # Create a TCP/IP socket.
    $socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
}
catch (Exception $e)
{
    echo "ER1";
    exit();
}    

if ($socket === false) 
{
    # can't create socket
    echo "ER1";
    exit();
} 



try
{
    # try to connect server
    $result = socket_connect($socket, $service_host, $service_port);
}
catch (Exception $e)
{
    echo "ER2";
    exit();
}    

if ($result === false) 
{
    # can't create socket
    echo "ER2";
}


try
{
    # send request data
    $wb = socket_write($socket, $req, strlen($req));
}
catch (Exception $e)
{
    echo "ER3";
    exit();
}  



try
{
    # get response data
    $out = socket_read($socket, 256);
}
catch (Exception $e)
{
    echo "ER4";
    exit();
} 


# close socket
socket_close($socket);

# return measure
echo str_replace("\r\n", "", $out); 

?>