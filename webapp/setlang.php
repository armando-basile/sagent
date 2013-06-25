<?php

$newlang=$_GET["lang"];

setcookie('language', $newlang, time() + (86400 * 365)); // 86400 = 1 day
header("Location: index.html");
exit;

?>
