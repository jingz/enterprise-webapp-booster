// Name FilterableGrid
// Autor: Jing 2014-08-07
// ---------------
// This Plugin makes data in the grid filterable
//
// Usage
// -----
//
// { 
//    xtype: 'grid',
//    plugins: [{ xclass: 'Ext.plugin.FilterableGrid'}],
//    columns: [{
//      xtype: 'textcolumns',
//      filterType: 'list', # it will select distinct values to be the filter list
//      filterStore: [ ['key', 'value'] ]  # if filterStore is set use this store to be the filter list
//                                         # if not select distinct values
//    }]
//    ...
// }
//
// Features:
// adding new row like the header but fill each column with proper field type
// handle sizeing when any header column is resized
// able to filter by typing text in the filter row
// able to use an operator to filter value in range
// able to filter by select value from the list
// able to filter by select value from datepicker
// able to set mode local or remote
// TODO remote
Ext.define("Ext.plugin.FilterableGrid", {
    alias: 'plugin.filterableGrid',

    // helper function for construct multiple-line string
    _buildString: function(fn){
        var reg = /\/\*([\s\S]*)\*\//im;
        if(typeof fn == 'function'){
            return reg.exec(fn.toString())[1];
        }
        return false;
    },

    init: function(hostGrid){
        var self = this;
        self.hostGrid = hostGrid;
        hostGrid.on("afterrender", this.renderUI, this);
    },

    renderUI: function() {
        var self = this;
        var g = self.hostGrid;

        g.store.on({
            add: function() { self._rebindFilterStore(); }
        });

        // 1. construct elements
        Ext.each(g.columns, function(col){
            if(col.filterType == 'list'){
                // build a filter store
                var store = self._createNewStoreForCombo([]);
                var t = Ext.create("Ext.form.ComboBox", { fieldLabel: '', store: store, 
                                                          valueField: 'value', displayField: 'text', 
                                                          mode: 'local',
                                                          style: 'margin: 0.5em; margin-top: 0px;', editable: false });
            } else {
                var t = Ext.create('Ext.form.TextField', { fieldLabel: '', style: 'margin: 0.5em; margin-top: 0px;', emptyText: '*' });
            }

            var c = Ext.create("Ext.container.Container", { layout: 'fit', renderTo: col.id });
            // add to container
            c.add(t);
            c.show();

            // 2. attach event
            t.on({ change: function(){ self._doFilter(); } });
            col.on({ resize:function() { c.doLayout(); } });
            col.getFilterValue = function() { return t.getValue(); }
            col.filterComponent = t;
        });

        // 3. render
        g.headerCt.doLayout();
    },

    _createNewStoreForCombo: function(data) {
        var d = [["", "*"]]; // init no filter option
        d = d.concat(data);
        return Ext.create("Ext.data.SimpleStore", { data: d, fields: ['value', 'text']});
    },

    _rebindFilterStore: function(){
        var self = this;
        var g = this.hostGrid;
        Ext.each(g.columns, function(col){
            if(col.filterType == 'list' && !col.filterStore){
                var uValues = [];
                g.store.data.each(function(r){
                    uValues.push(r.data[col.dataIndex]);
                });

                uValues = _.uniq(uValues);

                col.filterComponent.clearValue();
                col.picker = null;
                var data = _.map(uValues, function  (v) { return [v, v]; });
                var newStore = self._createNewStoreForCombo(data);
                col.filterComponent.bindStore(newStore);
            }
        });
    },

    _doFilter: function  () {
        var self = this;
        var g = self.hostGrid;
        setTimeout(function(){
            g.store.clearFilter();
            g.store.filter([{
                filterFn:  function (r) {
                    var isPass = true;
                    Ext.each(g.columns, function(col){
                        var v = col.getFilterValue(); 
                        var rowValue = r.data[col.dataIndex];
                        if(v){
                            if(col.xtype == "gridcolumn"){
                                isPass = isPass && self.filterText(rowValue, v);
                            }
                            if(col.xtype == "numbercolumn"){
                                isPass = isPass && self.filterNumber(rowValue, v);
                            }
                            // TODO date
                            if(col.xtype == "datecolumn"){
                                isPass = isPass && self.filterDate(rowValue, v);
                            }
                        }
                    });

                    return isPass;
                }
            }]);
        }, 250);
    },

    // return true/false
    // val = r.data[dataIndex]
    // filterVal = value from filter textbox
    // Specs
    // 1. able to set operator ">", "<", "="
    // 2. if not set mean >=
    // 3. start filter if val is not blank
    // 4. TODO suffix for thounson, million (100K) (10M)
    filterNumber: function(recVal, filterVal) {
        var optRegx = /^([><\=\!]\=?)/;
        filterVal = filterVal.replace(/\s*/,'');
        var opt = filterVal.match(optRegx);
        if(opt){
            opt = opt[1];
            valParts = filterVal.split(opt);
            filterVal = valParts[1];
        }

        if(filterVal != ""){
            // convert into float or int
            // check suffix
            if(/m$/i.test(filterVal)){
                filterVal = (+filterVal.replace(/m/i, ''))*1000000;
            } else if(/k$/i.test(filterVal)){
                filterVal = (+filterVal.replace(/k/i, ''))*1000;
            } else {
                filterVal = (+filterVal);
            }

            var recVal = +recVal;
            switch(opt){
                case ">":
                    return recVal > filterVal;
                    break;
                case "<":
                    return recVal < filterVal;
                    break;
                case ">=":
                    return recVal >= filterVal;
                    break;
                case "<=":
                    return recVal <= filterVal;
                    break;
                case "==": case "=":
                    return recVal == filterVal;
                    break;
                case "!=":
                    return recVal != filterVal;
                    break;
                default:
                    return recVal >= filterVal;
                    break;
            }
        } 
        // incase filterVal is blank
        return true;
    },

    filterText: function(recVal, filterVal) {
        var regexpVal = new RegExp(filterVal, "i");
        return regexpVal.test(recVal);
    },

    // Specs
    // possible filterVal value
    // 2013 : filter by year
    // 12 : filter by month or day
    // TODO 12/** : filter 12 day
    // TODO **/12 : filter month
    // aug : filter month 08
    // mon : filter by monday
    // 01/12 : filter day and month with current year
    // 01/12/2013 : normal case
    filterDate: function(recVal, filterVal) {
        filterVal = filterVal.trim();
        if(filterVal == '') return true;

        // convert target value to date
        if(!(recVal instanceof Date)){
            // expect format 2013-12-01
            recVal = new Date(recVal);
        }

        // filter year
        if(/^\d{4}$/.test(filterVal)){
           return recVal.format("Y") == filterVal; 
        }

        // filter day and month
        if(/^\d{2}$/.test(filterVal)){
           return Ext.util.Format.date(recVal, 'd') == filterVal || 
                  Ext.util.Format.date(recVal, 'm') == filterVal;
        }

        // filter by month acrm
        if(/^[a-z]{3}$/i.test(filterVal)){
            // months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'];
            // days = ['mon', 'tus', 'wed', 'thu', 'fri', 'sat', 'sun'];
            var dayMonthRegExp = new RegExp(filterVal, "i");
            return dayMonthRegExp.test(recVal.toString());
        }

        // full format search
        if(/^\d{2}\/\d{2}\/\d{4}$/i.test(filterVal)){
            var dateparts = filterVal.match(/^(\d{2})\/(\d{2})\/(\d{4})$/i);
            var d = dateparts[1];
            var m = dateparts[2];
            var y = dateparts[3];
            var dateStr = (y + "-" + m + "-" + d);
            return dateStr == recVal.format("Y-m-d");
        }

        return false;
    }
});
