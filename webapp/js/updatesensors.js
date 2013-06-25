    var httpRequest = null;
    var sensors = new Array();
    var smin = new Array();
    var smax = new Array();
    
    /*
    sensors[0] = "cpu0_temperature";
    smin[0] = 35;
    smax[0] = 39;
    sensors[1] = "cpu1_temperature";
    smin[1] = 35;
    smax[1] = 39;            
    */
    
    // read response from server
    function GetMeasure(sid)
    {
        // check for response status
        if (httpRequest.readyState === 4)
        {
            // update value
            var measure = httpRequest.responseText.replace("\r\n","");            
            var measurenum = parseFloat(measure.replace(",", "."));
            
            document.getElementById("S" + sid).innerHTML = measure;
            
            // update background color if out of limits
            if ((measurenum < smin[sid]) || (measurenum > smax[sid]))
            {
                document.getElementById("S" + sid).style.backgroundColor = "red";
            }
            else
            {
                document.getElementById("S" + sid).style.backgroundColor = "green";
            }

            
            // check for other measure to update
            if (sid < (sensors.length - 1))
            {
                // send request
                var url = "getmeasure.php?m=" + sensors[sid+1];                    
                httpRequest.open ("GET", url, true);    // async
                httpRequest.onreadystatechange = function() { GetMeasure(sid+1); };
                httpRequest.send ("m=" + sensors[sid+1]);
            }
            else
            {
                // recall full sensors update function after some seconds
                window.setTimeout("UpdateMeasures()", 8000);
            }                    
            
        }
    }
    
    
    // send request to update first sensor data
    function UpdateMeasures()
    {
        // check for httpRequest object 
        if (!httpRequest) 
        {
            httpRequest = CreateHTTPRequestObject ();   // defined in ajax.js
        }
        if (httpRequest) 
        {          
            // send request
            var url = "getmeasure.php?m=" + sensors[0];                    
            httpRequest.open ("GET", url, true);    // async
            httpRequest.onreadystatechange = function() { GetMeasure(0); };
            httpRequest.send ("m=" + sensors[0]);
        }
    }
            