<link rel='stylesheet' href='/static/css/rmap.css' type='text/css' />

<div class="panel panel-default">
    <!-- Collapsible section header - copied from the Citations section -->
    <div class="panel-heading clearfix">
        <h3 class="panel-title"  style="padding-top: 3px">RMap Graph</h3>
        <div class="pull-right">
            <button class="btn btn-link project-toggle">
		<i class="fa fa-angle-down"></i>
	    </button>
        </div>
    </div>

    <!-- Display a square panel containing a (currently) fixed RMap viewer -->
    <div class="rmap-panel panel-body" style="display:none">
	<!-- This div sets aside the proper space for a square RMap -->
	<div class="rmap-square"></div>
        <!-- Must use two-part iframe element or parent page does not finish loading -->
        <iframe class="rmap" src="https://dev.rmap-project.org/appdev/resources/http%3A%2F%2Fosf.io%2Fndry9/widget">
        </iframe>
    </div>

</div>

