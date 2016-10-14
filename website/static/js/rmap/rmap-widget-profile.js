
var discoDisplayElement = "#rmapmessage";

// Call the RMap server to create DiSCO data for the given OSF entity.
// Returns the new RMap ID for the DiSCO that was created
// or an empty string if the operation failed.
var createProfileDisco = function() {
        // Trim leading and trailing slashes from node ID
        // Perform POST to create DiSCO and get its ID
         $.post("/api/v1/rmap",
            function(data)
            {
            alert(data);
            alert(data.disco_id);
                // If successful, set the widget's source to make the graph appear.
                var discoId = data;
                //var discoUrl = getDiscoUrl(discoId);
                $("#message").text(discoId);
                $("#graph").show();
                $("#createButton").attr("disabled", "disabled");
            },
            "text");
            
        $("#confirmCreate").modal("hide");
};

// Initialize the page state after it has been created.

$.get("/api/v1/rmap",
    function(data) {
        var discoId=data.disco_id;
        //var discoUrl = getDiscoUrl(discoId);
        if (discoId!==null && discoId.length()>0){
            $(discoDisplayElement).text(discoId);
        }
    });
    
module.exports = {
    createProfileDisco: createProfileDisco
};
   
   
   