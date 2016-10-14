               

<span data-bind="if: hasRMapDiSCO()" class="scripted">
  <p>DiSCO ID: <span data-bind="text: discoId"></span></p>
</span>
<span data-bind="if: canCreateRMapDiSCO()" class="scripted">
  <!-- ko if: discoCreationInProgress() -->
    <p>
      <i class="fa fa-spinner fa-lg fa-spin"></i>
        <span class="text-info">Creating RMap DiSCO. Please wait...</span>
    </p>
  <!-- /ko -->

  <!-- ko ifnot: discoCreationInProgress() -->
  <p>
  <a data-bind="click: askCreateRMapDiSCO, visible: !discoCreationInProgress()">Create RMap DiSCO</a>
  </p>
  <!-- /ko -->
</span>
