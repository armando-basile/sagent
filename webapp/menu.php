<?php

include "core/base.php";

# get html code from template
$htmlmenu = file_get_contents($themepath . "/menu.html");
$rowsensor = file_get_contents($themepath . "/rowsensor.html");
$htmlsensors = file_get_contents($basevirtdir . "/getmeasure.php?m=LIST");
$htmlsensordata = "";

$sensorList = explode("$", $htmlsensors);
$tmpSensors = "";

# loop for each sensor in list
$tmpSensors = "";
for ($cnt=0; $cnt<count($sensorList)-1; $cnt++ )
{
    $sensorListRowItem = explode("|", $sensorList[$cnt]);
    $htmlsensordata .= "sensors[" . $cnt . "] = \"" . $sensorListRowItem[0] . "\";\r\n";
    $htmlsensordata .= "smin[" . $cnt . "] = parseFloat(\"" . str_replace(",", ".", $sensorListRowItem[1])  . "\");\r\n";
    $htmlsensordata .= "smax[" . $cnt . "] = parseFloat(\"" . str_replace(",", ".", $sensorListRowItem[2]) . "\");\r\n";

    $tmpSensors .= str_replace("<!-- SENSORNAME -->", $sensorListRowItem[0] , $rowsensor);
    $tmpSensors = str_replace("<!-- SENSORMIN -->", $sensorListRowItem[1] , $tmpSensors);
    $tmpSensors = str_replace("<!-- SENSORMAX -->", $sensorListRowItem[2] , $tmpSensors);
    $tmpSensors = str_replace("<!-- SENSORID -->", $cnt , $tmpSensors);
}

# update html code with dynamic data
$htmlmenu = str_replace("<!-- THEME -->", $theme , $htmlmenu);
#$htmltop = str_replace("<!-- TOPRELEASE -->", $relstring . "<br />" . $relbuild , $htmltop);
#$htmltop = str_replace("<!-- TOPHEADER -->", $LANGTEXT_title , $htmltop);
#$htmltop = str_replace("<!-- TOPSUBHEADER -->", $LANGTEXT_desc , $htmltop);






# update html code with sensors list
$htmlmenu = str_replace("<!-- SENSORS -->", $tmpSensors , $htmlmenu);
$htmlmenu = str_replace("<!-- SENSORS_DATA -->", $htmlsensordata , $htmlmenu);


echo $htmlmenu;    

?>