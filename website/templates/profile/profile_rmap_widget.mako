<link rel='stylesheet' href='/static/css/rmap.css' type='text/css' />

<!-- Define the pop-up dialog where users confirm they want to create a DiSCO.-->
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
                <!--if on a project page create node disco, if on a profile page create user disco-->
                
                % if 'write' in user['permissions']:
                <button type="submit" class="btn btn-danger" onclick="createProfileDisco()">Create</button>
                % endif
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
        <!-- This div sets aside the proper space for a square RMap -->
        <!--<div class="rmap-square"></div>-->
        <p>RMap is ... blah blah</p>
        <span class="text-info" id="rmapmessage"></span>
    </div>

</div>
