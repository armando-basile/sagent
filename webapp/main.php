<?php

include "core/base.php";

$htmlwelcome="";
$mReq="";
$dfReq="";
$dtReq="";
$vfReq="";
$vtReq="";
$minReq="";
$maxReq="";

# get sensor requested
if (isset($_GET["s"])) { $mReq=$_GET["s"]; }
if (isset($_GET["df"])) { $dfReq=$_GET["df"]; }
if (isset($_GET["dt"])) { $dtReq=$_GET["dt"]; }
if (isset($_GET["vf"])) { $vfReq=$_GET["vf"]; }
if (isset($_GET["vt"])) { $vtReq=$_GET["vt"]; }
if (isset($_GET["min"])) { $minReq=$_GET["min"]; }
if (isset($_GET["max"])) { $maxReq=$_GET["max"]; }



# check for request
if($mReq == "")
{
    # send welcome page and exit
    $htmlwelcome = file_get_contents($themepath . "/welcome.html");
    $htmlwelcome = str_replace("<!-- THEME -->", $theme , $htmlwelcome);
    $htmlwelcome = str_replace("<!-- WELCOME -->",  $LANGTEXT_welcome , $htmlwelcome);
    echo $htmlwelcome;
    exit();
}


# get html code from template
$htmlmain = file_get_contents($themepath . "/main.html");
$htmlreport = "";

# update html code with dynamic data
$htmlmain = str_replace("<!-- THEME -->", $theme , $htmlmain);
$htmlmain = str_replace("<!-- SENSORNAME -->", $mReq , $htmlmain);
$htmlmain = str_replace("<!-- SENSORMIN -->", $minReq , $htmlmain);
$htmlmain = str_replace("<!-- SENSORMAX -->", $maxReq , $htmlmain);
$htmlmain = str_replace("<!-- DATEFROM -->", $LANGTEXT_datefrom , $htmlmain);
$htmlmain = str_replace("<!-- DATETO -->", $LANGTEXT_dateto , $htmlmain);
$htmlmain = str_replace("<!-- VALUEFROM -->", $LANGTEXT_valuefrom , $htmlmain);
$htmlmain = str_replace("<!-- VALUETO -->", $LANGTEXT_valueto , $htmlmain);
$htmlmain = str_replace("<!-- SEARCH -->", $LANGTEXT_search , $htmlmain);
$htmlmain = str_replace("<!-- GRAPHDOWNLOAD -->", $LANGTEXT_graphdownload , $htmlmain);

# get graphic template
$graphtemp = file_get_contents($basedir . "/js/flotr-template.html");

# update graphic and add to page html code
$graphtemp = str_replace("<!-- GRAPHTITLE -->", $mReq , $graphtemp);

# update graphic axis labels
$graphtemp = str_replace("<!-- GRAPHXTITLE -->", $LANGTEXT_graphlabelx , $graphtemp);
$graphtemp = str_replace("<!-- GRAPHYTITLE -->", $LANGTEXT_graphlabely , $graphtemp);

# init database
Init_DB();

# check for date range requested
if ($dfReq == "")
{
    # set date range on last week
    $dtReq = date("Y-m-d H:i:s");
    $dfReq = date("Y-m-d H:i:s", strtotime($dtReq."- 7 days"));
}

# check for value range requested
if ($vfReq != "")
{
    # data and measure range requested
    $dataFromDb = Get_DataParam_Range($dfReq, $dtReq, $vfReq, $vtReq, $mReq);
}
else 
{
    # only data range requested
    $dataFromDb = Get_Data_Range($dfReq, $dtReq,  $mReq);    
}
# update graphic title
$daterange = $LANGTEXT_graphdaterange . " [" . $dfReq . " - " . $dtReq . "]";
$valuerange = $LANGTEXT_graphvaluerange . " [" . $vfReq . " - " . $vtReq . "]";
$graphtemp = str_replace("<!-- GRAPHSUBTITLE -->", $daterange . "  " . $valuerange , $graphtemp);


# update fields content
$htmlmain = str_replace("<!-- dfReq -->", $dfReq , $htmlmain);
$htmlmain = str_replace("<!-- dtReq -->", $dtReq , $htmlmain);
$htmlmain = str_replace("<!-- vfReq -->", $vfReq , $htmlmain);
$htmlmain = str_replace("<!-- vtReq -->", $vtReq , $htmlmain);


# update graphic measures
$graphLimitTop = "{\r\n" .
    "data: [ "; 

$graphMeasure = "{\r\n" .
    "data: [ ";

$graphLimitBottom = "{\r\n" .
    "data: [ ";

$graphDTValues = "";

# loop for all item in recordset
for ($p=0; $p<count($dataFromDb); $p++)
{
    $graphLimitBottom .= "[" . $p . ", " . $minReq . "], ";
    $graphMeasure .= "[" . $p . ", " . $dataFromDb[$p][1] . "], ";
    $graphLimitTop .= "[" . $p . ", " . $maxReq . "], ";
    $graphDTValues .= "'" . $dataFromDb[$p][0] . "', ";
}

if (count($dataFromDb) > 0)
{
    $graphLimitBottom = substr($graphLimitBottom, 0, count($graphLimitBottom)-3);
    $graphMeasure = substr($graphMeasure, 0, count($graphMeasure)-3);
    $graphLimitTop = substr($graphLimitTop, 0, count($graphLimitTop)-3);
}


$graphLimitBottom .= "],\r\n" .
    "shadowSize:0, \r\n" .
    "mouse: {track:false}, \r\n" . 
    "color: \"red\", \r\n" .
    "},\r\n";

$graphMeasure .= "],\r\n" .
    "label: \"Measure\", \r\n" .
    "lines: {show: true, fill: false}, \r\n" . 
    "color: \"blue\", \r\n" .
    "points: {show: true}, \r\n " .  
    "},\r\n";

$graphLimitTop .= "],\r\n" .
    "shadowSize:0, \r\n" .
    "mouse: {track:false}, \r\n" . 
    "color: \"red\", \r\n" . 
    "},\r\n";




$graphtemp = str_replace("<!-- DATAVALUES -->", $graphLimitTop . $graphMeasure . $graphLimitBottom , $graphtemp);
$graphtemp = str_replace("<!-- DATETIMEVALUES -->", $graphDTValues, $graphtemp);

$htmlmain = str_replace("<!-- GRAPHDATA -->", $graphtemp , $htmlmain);

echo $htmlmain;    



?>