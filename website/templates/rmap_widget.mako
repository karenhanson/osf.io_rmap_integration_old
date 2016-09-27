<link rel='stylesheet' href='/static/css/rmap.css' type='text/css' />

<%page args="isUser, isRegistration, isPublic, nodeId"/>


## Define the pop-up dialog where users confirm they want to create a DiSCO.
<div class="modal fade" id="confirmCreate">
    <div class="modal-dialog">
        <div class="modal-content">

            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal"
                        aria-hidden="true">&times;</button>
                <h3 class="modal-title">Create an RMap DiSCO</h3>
            </div> <!-- end modal-header -->

            <div class="modal-body">
                <p class="text-info">
                    You are about to create a DiSCO in RMap.  A DiSCO is a list of relationships between this page
                    and it's related components such as contributors, components, and projects.  
                </p>
                <p class="text-danger">
                    Creating a DiSCO will cause your OSF data to be publicly visible on the RMap server.
                </p>
            </div> <!-- end modal-body -->

            <div class="modal-footer">
                <a href="#" class="btn btn-default" data-dismiss="modal">Cancel</a>
                <button type="submit" class="btn btn-danger" onclick="createDisco()">Create</button>
            </div> <!-- end modal-footer -->

        </div> <!-- end modal- content -->
    </div> <!-- end modal-dialog -->
</div> <!-- end modal -->


## Create the RMap panel that displays a message or the DiSCO viewing widget.
<div class="panel panel-default">

    <!-- Collapsible section header - copied from the Citations section -->
    <div class="panel-heading clearfix" id="RMap">
        <h3 class="panel-title"  style="padding-top: 5px">RMap Graph</h3>
        <div class="pull-right">
        	
            <a class="btn btn-sm btn-default" id="createButton"
                data-toggle="modal" data-target="#confirmCreate">Generate RMap DiSCO</a>
        	<button class="btn btn-link project-toggle">
                <i class="fa fa-angle-down"></i>
            </button>
        </div>
    </div>

    <!-- Display a panel containing either a square RMap viewing widget or a message -->
    <div class="rmap-panel panel-body" id="disco" style="display:none">
        <div id="graph">
            <!-- This div sets aside the proper space for a square RMap -->
            <div class="rmap-square"></div>
            <!-- Must use two-part iframe element or parent page does not finish loading -->
            <iframe class="rmap" id="widget"></iframe>
        </div>
        <!-- Display an informative message (shown if no discoID) -->
        <span class="text-info" id="message"></span>
    </div>

</div>


<script>

    // For the "Create RMap DiSCO" button, override the behavior from
    // /static/js/pages/base-page.js where any click in a collapsible panel's
    // header toggles its collapsed state.  Now, clicking the button does not
    // toggle, but always expands the panel, regardless of its previous state.
    $(document).on('click', '#createButton',
        function()
        {
            $('#disco').slideUp();
        }
    );

    // To prevent unwanted zooming in the RMap widget, this event handler
    // hides the widget before its parent panel is collapsed and shows it
    // after the parent panel is expanded.  It stops propagation of the
    // original click event and triggers a new one to control the order of
    // the showing/hiding and the panel collapse/expand.
    // TODO - This technique currently results in a pan of the widget contents,
    // and after two such pans the graph is outside of the widget viewport.
    $(document).on('click', '#RMap',
        function(event)
        {
            event.stopPropagation();
            var e = jQuery.Event("click");

            var toggle = $(this).find('.project-toggle');
            if(toggle.length > 0)
            {
                var up = toggle.find('.fa.fa-angle-up');
                var down = toggle.find('.fa.fa-angle-down');
                if(up.length > 0)
                {
                    $("#RMap").parent().trigger(e);
                    $("#widget").show();
                }
                if(down.length > 0)
                {
                    $("#widget").hide();
                    $("#RMap").parent().trigger(e);
                }
            }
        }
    );

    // Returns the RMap ID for the OSF node that is being viewed.
    // Initially this is an empty string,
    // but it could be set once a DiSCO is created for the node.
    // TODO - This is enhanced functionality that is not yet developed.
    function getDiscoIdForNode()
    {
        // TODO - Load the discoId from OSF. How do we store it for each type of node?
        // For now, return an empty ID
        return "";
    }
    
    // Returns the OSF ID for the node that is being viewed.
    function getOsfIdForNode()
    {
        // This value was determined when the page was served up.
        return ${nodeId}
    }
    
    // Call the RMap server to create DiSCO data for the given OSF entity.
    // Returns the new RMap ID for the DiSCO that was created
    // or an empty string if the operation failed.
    function addDiscoToRmap(osfId)
    {
        // Prepare values to use in POST that creates a DiSCO
        var site = "rmaptransform:8080/transforms";
        if ("${isUser}" == "True")
        {
            var target = "osf_user";
        }
        else if ("${isRegistration}" == "True")
        {
            var target = "osf_registration";
        }
        else // Projects and components
        {
            var target = "osf_node";
        }

        // Trim leading and trailing slashes from node ID
        var id = osfId.toString();
        osfId = id.slice(1, id.length-1);
        
        // Perform POST to create DiSCO and get its ID
        var url = site + "/" + target + "?id=" + osfId;
        $.post("http://192.168.99.101:7000",
            { url: url },
            function(data)
            {
                // If successful, set the widget's source to make the graph appear.
                discoId = data;
                var discoUrl = getDiscoUrl(discoId);
                $("#widget").attr("src", discoUrl);
                $("#widget").show();
                $("#graph").show();
                $("#message").hide();
                $("#createButton").attr("disabled", "disabled");
            },
            "text");
    }
    
    // Returns the URL for a widget that will display the identified DiSCO.
    function getDiscoUrl(discoId)
    {
        var site = "https://dev.rmap-project.org/appdev/discos/";
        var url = site + encodeURIComponent(discoId) + "/widget";
        return url;
    }

    // Called when the "Create" button is clicked in the confirmation pop-up dialog.
    // If there was no previous DiSCO for this OSF entity, one is created.
    // TODO - If there was a previous DiSCO, it is updated on the RMap server.
    // Hides the confirmation pop-up.
    function createDisco()
    {
        // Decide whether to create a DiSCO or update an existing one.
        if (discoId == '')
        {
            // Create a new DiSCO for this OSF entity
            var osfId = getOsfIdForNode();
            discoId = addDiscoToRmap(osfId);
            // TODO - Save DiSCO ID in OSF node.
        }
        else
        {
            // TODO - Refresh the DiSCO for this OSF entity
        }
        
        $("#confirmCreate").modal("hide");
    }


    // Initialize the page state after it has been created.
    
    var discoId = "";
    
    // Hide the Create button and set the message as needed for different types of pages
    if ("${isRegistration}" == "True")
    {
        $("#createButton").hide();
        $("#message").text("RMap DiSCOs cannot be created on demand for Registrations.");
    }
    else if ("${isUser}" == "True" || "${isPublic}" == "True")
    {
        $("#message").text("Click the button to create a DiSCO.");
    }
    else // Private pages
    {
        $("#createButton").hide();
        $("#message").text("RMap DiSCOs can only be generated for public projects and components.");
    }

    // If we don't know the DiSCO's ID, hide the widget.
    if (discoId == '')
    {
        $("#graph").hide();
    }
    // Otherwise, set the widget source from the ID and hide the message.
    else
    {
        var discoUrl = getDiscoUrl(discoId);
        document.getElementById("widget").setAttribute("src", discoUrl);
        // TODO - does setting src automatically show widget or its parent (graph)?
        $("#message").hide();
    }
   
</script>
