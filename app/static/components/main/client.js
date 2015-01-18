define(["./client.ui"], function(ClientUI){

  var Client = Ext.extend(ClientUI,{
    constructor: function  (config) {
      config = config || {};
      Ext.apply(this, config);
      Client.superclass.constructor.call(this);
    },

    initComponent: function(){
    Client.superclass.initComponent.call(this);
      var self = x = this;
    
      self._search.on({
        click: function() {
          var params = self._frmFilter.serializeDirty();
          self._grd.fetch(params);
        }
      });
    }
  });

  return Client;
});
