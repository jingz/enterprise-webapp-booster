define(["./feed_list.ui"], function(Feed_listUI){
  var Feed_list = Ext.extend(Feed_listUI,{
    constructor: function  (config) {
      config = config || {};
      Ext.apply(this, config);
      Feed_list.superclass.constructor.call(this)
    },

      initComponent: function(){
        Feed_list.superclass.initComponent.call(this);
        var self = x = this;
        // use x for debugging at console

        self._search.on({
          click: function(){
            var params = self._frm.serialize();
            self._grd.fetch(params);
          }
        });

        self._add.on({
          click: function() {
            self._feedFrm.submit({
              url: '/feeds/',
              method: 'POST',
              success: function(res) {
                console.log(res);
                if(res.success && res.message)
                  App.Notify.succ('Adding feed success');
                else {
                  App.Notify.erro(res.message);
                  self._feedFrm.reset();
                }
              }
            });
          }
        });

      }
  });

  return Feed_list;
});
