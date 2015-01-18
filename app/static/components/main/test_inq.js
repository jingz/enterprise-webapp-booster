define(["./test_inq.ui"], function(Test_inqUI){
    var Test_inq = Ext.extend(Test_inqUI,{
        constructor: function  (config) {
            config = config || {};
            Ext.apply(this, config);
            Test_inq.superclass.constructor.call(this)
        },

        initComponent: function(){
            Test_inq.superclass.initComponent.call(this);
            var self = x = this;
        }

    });

    return Test_inq;
});
