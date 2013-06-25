<?php

# Attributes

# DB object
$sqlConn = null;


$sqlGetDataRange = "SELECT date_time AS DATE, paramvalue AS PARAMVALUE "
                    . "FROM surveys " 
                    . "WHERE date_time >= strftime('%Y-%m-%d %H:%M:%S','<from>') AND "
                    . "      date_time <= strftime('%Y-%m-%d %H:%M:%S','<to>') AND "
                    . "      paramid = '<pluginid>';";


$sqlGetParamRange = "SELECT date_time AS DATE, paramvalue AS PARAMVALUE "
                    . "FROM surveys " 
                    . "WHERE paramvalue >= <from> AND paramvalue <= <to> AND "
                    . "      paramid = '<pluginid>';";

$sqlGetDataParamRange = "SELECT date_time AS DATE, paramvalue AS PARAMVALUE "
                        . "FROM surveys " 
                        . "WHERE paramvalue >= <fromv> AND paramvalue <= <tov> AND "
                        . "      date_time >= strftime('%Y-%m-%d %H:%M:%S','<fromd>') AND "
                        . "      date_time <= strftime('%Y-%m-%d %H:%M:%S','<tod>') AND "
                        . "      paramid = '<pluginid>';";


# Init database connection
function Init_DB() 
{
    try 
    {
        # Create databases and open connections
        $GLOBALS['sqlConn'] = new PDO("sqlite:" . $GLOBALS['dbpath']);
    
    }
    catch(PDOException $e) 
    {
        # Print PDOException message
        exit ($e->getMessage());        
    }
    
}






# retrieve measures into data range
function Get_Data_Range($fromData, $toData, $pluginid)
{
    # update sql command
    $sqlText = str_replace("<from>", $fromData, $GLOBALS['sqlGetDataRange']); 
    $sqlText = str_replace("<pluginid>", $pluginid, $sqlText); 
    $sqlText = str_replace("<to>", $toData, $sqlText);
    
    $sqlStm = $GLOBALS['sqlConn']->query($sqlText);
    
    return $sqlStm->fetchAll();
}


# retrieve measures into range
function Get_Param_Range($fromVal, $toVal, $pluginid)
{
    # update sql command
    $sqlText = str_replace("<from>", $fromVal, $GLOBALS['sqlGetParamRange']);
    $sqlText = str_replace("<pluginid>", $pluginid, $sqlText); 
    $sqlText = str_replace("<to>", $toVal, $sqlText);
    
    $sqlStm = $GLOBALS['sqlConn']->query($sqlText);
    
    return $sqlStm->fetchAll();
}


# retrieve measures into range
function Get_DataParam_Range($fromData, $toData, $fromVal, $toVal, $pluginid)
{
    # update sql command
    $sqlText = str_replace("<fromd>", $fromData, $GLOBALS['sqlGetDataParamRange']);
    $sqlText = str_replace("<pluginid>", $pluginid, $sqlText); 
    $sqlText = str_replace("<tod>", $toData, $sqlText);
    $sqlText = str_replace("<fromv>", $fromVal, $sqlText);
    $sqlText = str_replace("<tov>", $toVal, $sqlText);
    
    $sqlStm = $GLOBALS['sqlConn']->query($sqlText);
    
    return $sqlStm->fetchAll();
}


# Close database connection
function Close_DB() 
{
    $GLOBALS['sqlConn'] = null;
    
}




?>