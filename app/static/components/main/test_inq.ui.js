define([], function(){
  var Test_inqUI = Ext.extend(Ext.Container,{
    initComponent: function(){
      Ext.applyIf(this,{
  "xtype":"container",
  "layout":"auto",
  "autoWidth":true,
  "autoDestroy":true,
  "model":"ord_deal_inq",
  "plugins":[
    {
      "xclass":"Ext.plugin.ActAsInquiry"
    }
  ],
  "cmp_id":"inqWrapper",
  "items":[
    {
      "xtype":"fieldset",
      "layout":"anchor",
      "animCollapse":true,
      "labelAlign":"right",
      "autoHeight":true,
      "autoDestroy":true,
      "padding":5,
      "border":false,
      "items":[
        {
          "xtype":"container",
          "layout":"hbox",
          "autoWidth":true,
          "autoDestroy":true,
          "layoutConfig":{
            "pack":"start",
            "align":"stretchmax"
          },
          "defaults":{
            "margins":"0 2.5"
          },
          "items":[
            {
              "xtype":"container",
              "layout":"anchor",
              "autoWidth":true,
              "autoDestroy":true,
              "style":"{ height: 100%; margin: 0em 0em; }",
              "defaults":{
                "margins":"0 0"
              },
              "col_index":0,
              "items":[
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
                  "store":(this.ss = new Ext.data.JsonStore({        remoteFilter: true,        remoteGroup: false,        groupField: 'sec_symbol',        proxy: { type: 'rest', url: '/inq/ord_deal_inq', reader: { type: 'json', root: 'data' } },        fields: [{"type": "string", "name": "client_code"}, {"type": "string", "name": "sec_symbol"}, {"type": "integer", "name": "qty"}, {"type": "string", "name": "x_order_no"}, {"type": "string", "name": "confirm_no"}, {"type": "float", "name": "commission"}, {"type": "float", "name": "fee"}, {"type": "string", "name": "ae_code"}, {"type": "string", "name": "order_no"}, {"type": "string", "name": "fullname_lc"}, {"type": "float", "name": "net_amount"}, {"type": "date", "name": "order_date"}]    })) ,
                  "height":200,
                  "autoDestroy":true,
                  "margin":5,
                  "plugins":[
                    {
                      "xclass":"Ext.plugin.MultiSortGrid"
                    }
                  ],
                  "features":[
                    {
                      "ftype":"groupingsummary"
                    }
                  ],
                  "columns":[
                    {
                      "xtype":"gridcolumn",
                      "header":"Client Code",
                      "dataIndex":"client_code",
                      "sortable":false,
                      "width":"auto",
                      "autoDestroy":true,
                      "cmp_id":"clientCode"
                    },
                    {
                      "xtype":"gridcolumn",
                      "header":"Symbol",
                      "dataIndex":"sec_symbol",
                      "sortable":false,
                      "width":"auto",
                      "autoDestroy":true,
                      "cmp_id":"secSymbol"
                    },
                    {
                      "xtype":"numbercolumn",
                      "align":"right",
                      "sortable":false,
                      "format":"0,000",
                      "header":"Qty",
                      "dataIndex":"qty",
                      "width":"auto",
                      "autoDestroy":true,
                      "summaryType":"sum",
                      "cmp_id":"qty"
                    },
                    {
                      "xtype":"gridcolumn",
                      "header":"X Order No",
                      "dataIndex":"x_order_no",
                      "sortable":false,
                      "width":"auto",
                      "autoDestroy":true,
                      "cmp_id":"xOrderNo"
                    },
                    {
                      "xtype":"gridcolumn",
                      "header":"Confirm No",
                      "dataIndex":"confirm_no",
                      "sortable":false,
                      "width":"auto",
                      "autoDestroy":true,
                      "cmp_id":"confirmNo"
                    },
                    {
                      "xtype":"numbercolumn",
                      "align":"right",
                      "sortable":false,
                      "format":"0,000.00",
                      "header":"Commission",
                      "dataIndex":"commission",
                      "width":"auto",
                      "autoDestroy":true,
                      "summaryType":"avg",
                      "cmp_id":"commission"
                    },
                    {
                      "xtype":"numbercolumn",
                      "align":"right",
                      "sortable":false,
                      "format":"0,000.00",
                      "header":"Fee",
                      "dataIndex":"fee",
                      "width":"auto",
                      "autoDestroy":true,
                      "cmp_id":"fee"
                    },
                    {
                      "xtype":"gridcolumn",
                      "header":"Ae Code",
                      "dataIndex":"ae_code",
                      "sortable":false,
                      "width":"auto",
                      "autoDestroy":true,
                      "summaryType":"count",
                      "cmp_id":"aeCode"
                    },
                    {
                      "xtype":"gridcolumn",
                      "header":"Order No",
                      "dataIndex":"order_no",
                      "sortable":false,
                      "width":"auto",
                      "autoDestroy":true,
                      "cmp_id":"orderNo"
                    },
                    {
                      "xtype":"gridcolumn",
                      "header":"Fullname",
                      "dataIndex":"fullname_lc",
                      "sortable":false,
                      "width":"auto",
                      "autoDestroy":true,
                      "cmp_id":"fullnameLc"
                    },
                    {
                      "xtype":"numbercolumn",
                      "align":"right",
                      "sortable":false,
                      "format":"0,000.00",
                      "header":"Net Amount",
                      "dataIndex":"net_amount",
                      "width":"auto",
                      "autoDestroy":true,
                      "cmp_id":"netAmount"
                    },
                    {
                      "xtype":"datecolumn",
                      "format":"d/m/Y",
                      "header":"Order Date",
                      "dataIndex":"order_date",
                      "sortable":false,
                      "width":"auto",
                      "autoDestroy":true,
                      "cmp_id":"orderDate"
                    }
                  ],
                  "tbar":{
                    "xtype":"toolbar",
                    "autoDestroy":true,
                    "items":[
                      {
                        "xtype":"button",
                        "text":"PDF",
                        "autoDestroy":true,
                        "cmp_id":"exportPdf"
                      },
                      {
                        "xtype":"button",
                        "text":"CSV",
                        "autoDestroy":true,
                        "cmp_id":"exportCsv"
                      },
                      {
                        "xtype":"button",
                        "text":"EXCEL",
                        "autoDestroy":true,
                        "cmp_id":"exportXlsx"
                      },
                      {
                        "xtype":"tbfill",
                        "autoDestroy":true
                      },
                      {
                        "xtype":"button",
                        "text":">",
                        "autoDestroy":true,
                        "title":"Expand",
                        "cmp_id":"expand"
                      }
                    ]
                  },
                  "bbar":{
                    "xtype":"pagingtoolbar",
                    "start":0,
                    "limit":20,
                    "displayInfo":true,
                    "dock":"bottom",
                    "displayMsg":"Displaying {0} - {1} of {2}",
                    "autoDestroy":true,
                    "pageSize":100,
                    "store":this.ss
                  },
                  "cmp_id":"grd"
                }
              ]
            },
            {
              "xtype":"container",
              "layout":"anchor",
              "autoWidth":true,
              "autoDestroy":true,
              "style":"{ height: 100%; margin: 0em 0em; }",
              "defaults":{
                "margins":"0 0"
              },
              "col_index":1,
              "items":[
                {
                  "xtype":"form",
                  "autoHeight":true,
                  "layout":"anchor",
                  "border":false,
                  "autoDestroy":true,
                  "labelWidth":10,
                  "fbar":{
                    "xtype":"toolbar",
                    "autoDestroy":true,
                    "items":[
                      {
                        "xtype":"button",
                        "text":"Search",
                        "autoDestroy":true,
                        "cmp_id":"search"
                      },
                      {
                        "xtype":"button",
                        "text":"Clear Filter",
                        "autoDestroy":true,
                        "cmp_id":"clearFilter"
                      }
                    ]
                  },
                  "cmp_id":"frmFilter",
                  "items":[
                    {
                      "xtype":"fieldset",
                      "layout":"anchor",
                      "animCollapse":true,
                      "labelAlign":"right",
                      "autoHeight":true,
                      "title":"Filter",
                      "autoDestroy":true,
                      "border":true,
                      "width":420,
                      "defaults":{
                        "labelWidth":105
                      },
                      "cmp_id":"filter",
                      "items":[
                        {
                          "xtype":"textfield",
                          "labelAlign":"right",
                          "autoDestroy":true,
                          "submitValue":true,
                          "name":"sec_symbol",
                          "emptyText":"Sec Symbol",
                          "fieldLabel":"Sec Symbol",
                          "cmp_id":"secSymbol"
                        },
                        {
                          "xtype":"textfield",
                          "labelAlign":"right",
                          "autoDestroy":true,
                          "submitValue":true,
                          "name":"ae_code",
                          "emptyText":"Ae Code",
                          "fieldLabel":"Ae Code",
                          "cmp_id":"aeCode"
                        },
                        {
                          "xtype":"fieldcontainer",
                          "layout":"hbox",
                          "defaultType":"textfield",
                          "labelAlign":"right",
                          "autoDestroy":true,
                          "submitValue":true,
                          "name":"order_date",
                          "fieldLabel":"Order Date",
                          "cmp_id":"orderDate",
                          "items":[
                            {
                              "xtype":"datefield",
                              "labelAlign":"right",
                              "format":"d/m/Y",
                              "width":110,
                              "cls":"date",
                              "autoDestroy":true,
                              "name":"order_date_gte",
                              "submitValue":true,
                              "cmp_id":"orderDateGte"
                            },
                            {
                              "xtype":"splitter",
                              "autoDestroy":true
                            },
                            {
                              "xtype":"datefield",
                              "labelAlign":"right",
                              "format":"d/m/Y",
                              "width":110,
                              "cls":"date",
                              "autoDestroy":true,
                              "name":"order_date_lte",
                              "submitValue":true,
                              "cmp_id":"orderDateLte"
                            }
                          ]
                        }
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
});
      Test_inqUI.superclass.initComponent.call(this);
      var self = this;
      
      // manually make auto ref
      Ext.each(self.query('*'), function(element, index){
        if(element.cmp_id) {
          self["_" + element.cmp_id] = element;
        }
      });
    }
  });

  return Test_inqUI;
});
