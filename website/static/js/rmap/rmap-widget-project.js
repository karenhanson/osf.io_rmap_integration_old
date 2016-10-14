'use strict';

var discoDisplayElement = "#rmapmessage";


$.get(window.contextVars.node.urls.api + "rmap",
    function(data) 
    {
        var discoId=data.disco_id;
        //var discoUrl = getDiscoUrl(discoId);
        if (discoId!==null && discoId.length()>0){
            $(discoDisplayElement).text(discoId);
        }
    });

 