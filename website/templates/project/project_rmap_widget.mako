               

<span data-bind="if: hasRMapDiSCO()" class="scripted">
  <p>
      RMap DiSCO ID: <a data-bind="text:disco, attr: {href: discoUrl}" target="_blank"></a>
      <span data-bind="if: canUpdateRMapDiSCO()" class="scripted">
          (<a data-bind="click: askUpdateRMapDiSCO, visible: !discoCreationInProgress()">update</a>
          &nbsp;|&nbsp;<a data-bind="click: askRemoveRMapDiSCO, visible: !discoRemoveInProgress()">remove</a>)
      </span>
  </p>
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
