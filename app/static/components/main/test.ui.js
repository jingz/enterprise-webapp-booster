define([], function(){
  var TestUI = Ext.extend(Ext.Container,{
  "layout": "auto",
  "autoWidth": true,
  "autoDestroy": true,
  "cls": "view-wrapper",
    initComponent: function(){
      Ext.applyIf(this,{
  "xtype":"container",
  "layout":"auto",
  "autoWidth":true,
  "autoDestroy":true,
  "cls":"view-wrapper",
  "items":[
    {
      "xtype":"form",
      "autoHeight":true,
      "layout":"anchor",
      "border":false,
      "autoDestroy":true,
      "cmp_id":"frm",
      "items":[
        {
          "xtype":"fieldset",
          "layout":"anchor",
          "animCollapse":true,
          "labelAlign":"right",
          "autoHeight":true,
          "title":"Info",
          "autoDestroy":true,
          "defaults":{
            "labelWidth":87
          },
          "cmp_id":"info",
          "items":[
            {
              "xtype":"textfield",
              "labelAlign":"right",
              "autoDestroy":true,
              "submitValue":true,
              "name":"test_box",
              "emptyText":"Test Box",
              "fieldLabel":"Test Box",
              "cmp_id":"testBox"
            },
            {
              "xtype":"textfield",
              "labelAlign":"right",
              "autoDestroy":true,
              "submitValue":true,
              "name":"test_xxx",
              "emptyText":"Test Xxx",
              "fieldLabel":"Test Xxx",
              "cmp_id":"testXxx"
            }
          ]
        }
      ]
    },
    {
      "xtype":"grid",
      "title":null,
      "columnLines":true,
      "sm":"",
      "selector":"row",
      "viewConfig":{
        "forceFit":true,
        "emptyText":"No record"
      },
      "frame":false,
      "width":"auto",
      "loadMask":true,
      "store":(this._zaJqlpotTifxcRDExQ = new Ext.data.JsonStore({            storeId: "_zaJqlpotTifxcRDExQ",            pageSize: 25,            proxy: {              url: "",              type: "memory",              reader: { type: "json", root: "data" }            },            fields: [{ name: 'id' },{ name: 'name' },{ name: 'aday' },{ name: 'money' },{ name: 'groupper' }]          }))        ,
      "height":500,
      "autoDestroy":true,
      "features":[
        {
          "ftype":"grouping"
        },
        {
          "ftype":"summary"
        }
      ],
      "plugins":[
        {
          "xclass":"Ext.plugin.FilterableGrid"
        }
      ],
      "columns":[
        {
          "xtype":"gridcolumn",
          "header":"Id",
          "dataIndex":"id",
          "sortable":false,
          "autoDestroy":true,
          "cmp_id":"id"
        },
        {
          "xtype":"gridcolumn",
          "header":"Name",
          "dataIndex":"name",
          "sortable":false,
          "autoDestroy":true,
          "cmp_id":"name"
        },
        {
          "xtype":"datecolumn",
          "format":"d/m/Y",
          "header":"Aday",
          "dataIndex":"aday",
          "sortable":false,
          "autoDestroy":true,
          "cmp_id":"aday"
        },
        {
          "xtype":"numbercolumn",
          "align":"right",
          "sortable":false,
          "format":"0,000",
          "header":"Money",
          "dataIndex":"money",
          "autoDestroy":true,
          "cmp_id":"money"
        },
        {
          "xtype":"gridcolumn",
          "header":"Groupper",
          "dataIndex":"groupper",
          "sortable":false,
          "autoDestroy":true,
          "cmp_id":"groupper"
        }
      ],
      "bbar":{
        "xtype":"pagingtoolbar",
        "start":0,
        "limit":20,
        "displayInfo":true,
        "dock":"bottom",
        "displayMsg":"Displaying {0} - {1} of {2}",
        "autoDestroy":true,
        "store":this._zaJqlpotTifxcRDExQ
      },
      "cmp_id":"grd"
    }
  ]
});
      TestUI.superclass.initComponent.call(this);
      var self = this;
      
      // manually make auto ref
      Ext.each(self.query('*'), function(element, index){
        if(element.cmp_id) {
          self["_" + element.cmp_id] = element;
        }
      });
    }
  });

  return TestUI;
});
