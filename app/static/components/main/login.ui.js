define([], function(){
  var LoginUI = Ext.extend(Ext.Container,{
    "layout": "auto",
  "autoWidth": true,
  "autoDestroy": true,
  "id": "form-wrapper",
  "padding": 10,
  "style": "background-color: #ccc;",
  "cmp_id": "formWrapper",
    initComponent: function(){
      Ext.applyIf(this,{
  "xtype":"container",
  "layout":"auto",
  "autoWidth":true,
  "autoDestroy":true,
  "id":"form-wrapper",
  "padding":10,
  "style":"background-color: #ccc;",
  "cmp_id":"formWrapper",
  "items":[
    {
      "xtype":"form",
      "autoHeight":true,
      "layout":"anchor",
      "border":false,
      "autoDestroy":true,
      "id":"frm-login",
      "style":"background-color: #ccc;",
      "cmp_id":"frmLogin",
      "items":[
        {
          "xtype":"fieldset",
          "layout":"anchor",
          "animCollapse":true,
          "labelAlign":"right",
          "autoHeight":true,
          "title":"",
          "autoDestroy":true,
          "id":"fis-login",
          "border":false,
          "style":"width: 100%; margin: 150px 40%;",
          "defaults":{
            "labelWidth":87
          },
          "cmp_id":"fisLogin",
          "items":[
            {
              "xtype":"textfield",
              "labelAlign":"right",
              "autoDestroy":true,
              "id":"username",
              "hideLabel":true,
              "width":"100%",
              "fieldStyle":"padding: 20px 20px; font-size: 1.3em;",
              "submitValue":true,
              "name":"username",
              "emptyText":"Username",
              "fieldLabel":"Username",
              "cmp_id":"username"
            },
            {
              "xtype":"textfield",
              "width":"100%",
              "inputType":"password",
              "autoDestroy":true,
              "id":"password",
              "hideLabel":true,
              "fieldStyle":"padding: 20px 20px; font-size: 1.3em;",
              "submitValue":true,
              "name":"password",
              "emptyText":"Password",
              "fieldLabel":"Password",
              "cmp_id":"password"
            },
            {
              "xtype":"button",
              "text":"Login",
              "autoDestroy":true,
              "id":"login",
              "style":"padding: 0.3em; width: 100%; margin-top: 0.5em;",
              "cmp_id":"login"
            }
          ]
        }
      ]
    }
  ]
});
      LoginUI.superclass.initComponent.call(this);
      var self = this;
      
      // manually make auto ref
      Ext.each(self.query('*'), function(element, index){
        if(element.cmp_id) {
          self["_" + element.cmp_id] = element;
        }
      });
    }
  });

  return LoginUI;
});