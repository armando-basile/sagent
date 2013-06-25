<?php

include "core/base.php";

# get html code from template
$htmltop = file_get_contents($themepath . "/top.html");

# update html code with dynamic data
$htmltop = str_replace("<!-- TOPRELEASE -->", $relstring . "<br />" . $relbuild , $htmltop);
$htmltop = str_replace("<!-- TOPHEADER -->", $LANGTEXT_title , $htmltop);
$htmltop = str_replace("<!-- TOPSUBHEADER -->", $LANGTEXT_desc , $htmltop);
$htmltop = str_replace("<!-- THEME -->", $theme , $htmltop);

$langs = glob($basedir . "/langs/*.php");
$htmllangs = "";

for ($l=0; $l<count($langs); $l++)
{
    $itemname = str_replace(".php", "", basename($langs[$l]));
    
    if ($language == $itemname)
    {
        $htmllangs .= "<option selected>" . $itemname . "</option>\r\n";
    }
    else 
    {
        $htmllangs .= "<option>" . $itemname . "</option>\r\n";
    }     
}

$htmltop = str_replace("<!-- LANGUAGES -->", $htmllangs , $htmltop);

echo $htmltop;    
?>