// Name MultiSortGrid
// Autor: Sarunyoo Chobpanich  1.SEP.2014
// ---------------
// This Plugin makes data in the grid filterable
//
// Usage
// -----
//
// { 
//    xtype: 'grid',
//    plugins: [{ xclass: 'Ext.plugin.MultiSortGrid'}],
//    ...
// }
//
// Features and Detail:
// do mutisort data in a grid
// able to sort locally or remotely with specific protocal parameters
// if store that the grid used is set remoteSort = true , it will do remote sort automatically
// otherwise do locally
// sort priority is determine on column order
//

Ext.define("Ext.plugin.MultiSortGrid", {
    alias: 'plugin.multiSortGrid',

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
        self.grid = hostGrid;
        hostGrid.on("afterrender", this.renderUI, this);
        hostGrid.on("columnmove", this._doSort, this);
    },

    renderUI: function() {
        var self = this;
        var g = self.grid;

        //    bind click event on every column with a function
        //    that save sort state ( not sort, asc, desc )
        //    and serialize state of all columns in to the
        //    proper params to send remotely
        //
        //    Example of proper params
        //    [
        //      { direction: 'asc', 
        //        property: 'colIndex', 
        //        priority: 1 },
        //        ...
        //        ...
        //    ]

        Ext.each(g.columns, function(col) {
           col._SORTSTATE_CONST = ['desc', 'asc', false];
           col._SORTSTATE_DISPLAY_CONST = ['↑', '↓', ''];
           col._sortClickCnt = -1;

           // prepare display container
           var container = $('#' + col.id);
           var mark = container.find('.x-column-header-text');
           var markCls = 'x-column-sort-dir';
           $("<b class='" + markCls + "' style='margin-left: 0.3em; font-weight: bold; font-size: 1.5em; color: blue;'></b>").insertAfter(mark);

           // decoratators
           col._getStateIndex = function(){
              return col._sortClickCnt % col._SORTSTATE_CONST.length;
           }

           col.getSortState = function(){
              return col._SORTSTATE_CONST[col._getStateIndex()];
           }

           col.getSortStateDisplay = function() {
              return col._SORTSTATE_DISPLAY_CONST[col._getStateIndex()];
           }

           col.updateSortStateDisplay = function(){
              var disp = col.getSortStateDisplay();
              container.find("." + markCls).text(disp);
           }

           // if headerclick it will change the state 
           col.on({
              headerclick: function(){
                  col._sortClickCnt++;
                  col.updateSortStateDisplay();
                  self.serializeSortParams();
                  self._doSort();
              }
           });
        });
    },

    _doSort: function  () {
        var self = this;
        if(self._doSortTimer) clearTimeout(self._doSortTimer);
        self._doSortTimer = setTimeout(function() {
            if(self.grid.store.remoteSort) self._doRemoteSort();
            else self._doLocalSort();
        }, 400);
    },

    _doLocalSort: function() {
        var self = this;
        var params = self.serializeSortParams();
        var store = self.grid.store;
        params = _.sortBy(params, function(r){ return r.priority; });
        ordered_sorters = _.map(params, function(o){
            return { property: o.property, direction: o.direction };
        });

        store.sort(ordered_sorters);
    },

    _doRemoteSort: function() {
        // use extraParam of proxy to send sort params to server side 
        // build sort remote params
        var params = this.serializeSortParams();
        var remoteParams = {};
        Ext.each(params, function(o){
            // TODO accept another protocal
            var k = "sort_by_" + o.property; // sort_by_column
            var v = o.direction + "_" + o.priority; // asc_1
            remoteParams[k] = v;
        });

        var store = this.grid.store;
        this._clearSortFilter();
        Ext.apply(store.proxy.extraParams, remoteParams );
        store.load();
    },

    _clearSortFilter: function() {
        var store = this.grid.store;
        for(var k in store.proxy.extraParams){
            // TODO set to config
            if(/^sort_by_/.test(k)){
                delete store.proxy.extraParams[k];
            }
        }
    },

    serializeSortParams: function() {
        var self = this;
        var params = [];
        Ext.each(self.grid.columns, function(col, i){
            var state = col.getSortState(); // direction state 
            if(state) {
                params.push({ direction: state, priority: col.getIndex(), property: col.dataIndex });
            }
        });

        return params;
    },

});
