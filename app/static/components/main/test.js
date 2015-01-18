define(["./test.ui"], function(TestUI){
  var Test = Ext.extend(TestUI,{
    constructor: function  (config) {
      config = config || {};
      Ext.apply(this, config);
      Test.superclass.constructor.call(this)
    },

    initComponent: function(){
    Test.superclass.initComponent.call(this);
      var self = x = this;
      // use x for debugging at console
      //

      var data = [];
      var g = ['A', 'B', 'C', 'D', 'E'];
      for(var i = 0; i < 50; i++){
        data.push({
          id: i+1,
          name: ('A String' + i),
          aday: new Date(),
          money: (Math.random() * 100000000),
          groupper: g[i%5]
        })
      }

      self.on({
        afterrender: function(){
            self._grd.addRecords(data);
        } 
      });
    
      self._testBox.on({
            blur: function(){
               alert(this.getValue()); 
            }
      });
    }
  });

  return Test;
});
