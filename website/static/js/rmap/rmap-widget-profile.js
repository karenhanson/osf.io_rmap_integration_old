

function init(displayElement){

    var discoid = '';

    // Call the RMap server to create DiSCO data for the given OSF entity.
    // Returns the new RMap ID for the DiSCO that was created
    // or an empty string if the operation failed.
    function createProfileDisco()
    {
        // Trim leading and trailing slashes from node ID
        // Perform POST to create DiSCO and get its ID
         $.post("/api/v1/rmap",
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
    
    
    $.get("/api/v1/rmap",function(data) {
        discoid=data;
        if (data!=null && data.length()>0){
            $(displayElement).text(discoUrl);
        }
    }
    
}
    
   module.exports = init;
   
   
   