define(["./feed_entries.ui"], function(Feed_entriesUI){
  var Feed_entries = Ext.extend(Feed_entriesUI,{
    constructor: function  (config) {
      config = config || {};
      Ext.apply(this, config);
    Feed_entries.superclass.constructor.call(this)
    },

    initComponent: function(){
    Feed_entries.superclass.initComponent.call(this);
      var self = x = this;
      // use x for debugging at console
    
      self._search.on({
        click: function(){
            var params = self._frm.serializeNotBlank();
            self._grd.fetch(params);    
        }
      });

      self._markAllAsRead.on({
            click: function() {
                var recs = self._grd.getAllRecords();
                Ext.each(recs, function(rec, i){
                    rec.data.mark_as_read = true; 
                    rec.commit();
                    rec.dirty = true;
                });
            }
      });

      self._save.on({
        click:  function () {
            var mod_recs = self._grd.getModifiedRecords()
            mod_recs = _.map(mod_recs, function(r){ return r.data });
            console.log(mod_recs);
            $.ajax({
                url: "/feed_entries/chunk",
                type: "PUT",
                data: Ext.encode({ records: mod_recs }),
                success: function(res) {
                   console.log(res); 
                   if(res.success){
                       var params = self._frm.serializeNotBlank();
                       self._grd.fetch(params);
                   }
                }
            });
        }
      });
    
    }
  });

  return Feed_entries;
});
