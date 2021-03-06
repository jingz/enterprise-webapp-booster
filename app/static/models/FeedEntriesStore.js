/*
 * File: FeedEntriesStore.js
 *
 * This file was generated by Python Script
 * /extscript.rb
 *
 */

define(function(){
  var FeedEntriesStore = new Ext.data.JsonStore({
      storeId: 'feedEntriesStore',
      remoteFilter: true,
      proxy: {
        type: 'rest',
        url: '/feed_entries',
        reader: {
          type: 'json',
          root: 'data'
        }
      },
      fields: [
        { name: 'id', type: 'int' },
        { name: 'item_id', type: 'string' },
        { name: 'feed_id', type: 'int' },
        { name: 'feed', type: 'string' },
        { name: 'title', type: 'string' },
        { name: 'link', type: 'string' },
        { name: 'summary', type: 'string' },
        { name: 'mark_as_read', type: 'boolean' },
        { name: 'mark_as_goodnews', type: 'boolean' },
        { name: 'published', type: 'datetime' },
        { name: 'updated', type: 'datetime' }
      ]
  });

  return FeedEntriesStore;
});
