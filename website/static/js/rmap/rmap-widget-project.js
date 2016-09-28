

function init(displayElement) {
    // For the "Create RMap DiSCO" button, override the behavior from
     function createNodeDisco()
    {
        // Trim leading and trailing slashes from node ID
        // Perform POST to create DiSCO and get its ID
         $.post(window.contextVars.node.urls.api + "/rmap",
            function(data)
            {
                // If successful, set the widget's source to make the graph appear.
                discoId = data;
                var discoUrl = getDiscoUrl(discoId);
                $("#message").text(discoUrl);
                $("#graph").show();
                $("#createButton").attr("disabled", "disabled");
            },
            "text");
            
        $("#confirmCreate").modal("hide");
    }

    // Initialize the page state after it has been created.
    
    var discoId = "";
    
    
    $.get(window.contextVars.node.urls.api + "/rmap",function(data) {
        discoid=data;
        if (data!=null && data.length()>0){
            $(displayElement).text(discoUrl);
        }
    }
   
   }
   
   module.exports = init;
 