// Name ActAsInquiry 
// Desc: ExtJS Plugin for sharing code of inquiry components
// Author: Jing 2014-09-30
// 
// ---------------
Ext.define("Ext.plugin.ActAsInquiry", {
    alias: 'plugin.actasinquiry',

    init: function(comp){
        var model = comp.model
        var self = comp;

        var offset_x = 20;
        var offset_y = 25;
        
        self.on({
          afterrender:  function() {
             // set calced height 
              var h = $(document).height();
              var y = self._grd.getPosition()[1];
              var _h = h - y - offset_y;
              self._grd.setHeight(_h);

              // set width
              var w = $(document).width();
              var x = self._grd.getPosition()[0];
              var _w = w - x - offset_x - self._frmFilter.getWidth();
              self._grd.setWidth(_w);
          }
        });

        self._exportPdf.on({
          click: function(){
              if(self._frmFilter.isValid()){
                  var params = self._frmFilter.serializeNotBlank();
                  Ext.apply(params, { export_pdf: true} )
                  var url = "/inq/" + model + "?" + Ext.urlEncode(params)
                    console.log(url)
                  window.open(url, "_blank");
              }
          }
        });

        self._exportXlsx.on({
          click: function(){
              if(self._frmFilter.isValid()){
                  var params = self._frmFilter.serializeNotBlank();
                  Ext.apply(params, { model: model} )
                  var url = "/inq/export_xl?" + Ext.urlEncode(params)
                    console.log(url)
                  window.open(url, "_blank");
              }
          }
        });

        self._search.on({
          click:  function() {
              var params = self._frmFilter.serializeNotBlank();
             self._grd.fetch(Ext.apply({model: model}, params)); 
          }
        });

        self._clearFilter.on({
              click: function(){
                  self._frmFilter.reset();        
              }
        });

        self._expand.on({
              click: function(){
                  self.isExpand = !!!self.isExpand;
                  self.oldGridSize = self.oldGridSize || self._grd.getWidth();
                  if(self.isExpand){
                      self._frmFilter.hide();
                      self._expand.setText("<");
                      // calc proper width
                      var doc_w = $(document).width();
                      var pos_x = self._grd.getPosition()[0];
                      var size = doc_w - pos_x - 10;
                      self._grd.setSize(size);
                  } else {
                      // resume normal
                      self._frmFilter.show();
                      self._expand.setText(">");
                      self._grd.setSize(self.oldGridSize);
                  }
              }
        });
    }

});
