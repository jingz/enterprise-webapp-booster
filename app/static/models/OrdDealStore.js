/*
 * File: OrdDealStore.js
 *
 * This file was generated by Python Script
 * /extscript.rb
 *
 */

define(function(){
  var OrdDealStore = new Ext.data.JsonStore({
      storeId: 'ordDealStore',
      remoteFilter: true,
      proxy: {
        type: 'rest',
        url: '/inq',
        reader: {
          type: 'json',
          root: 'data'
        }
      },
      fields: [
        { name: 'id', type: 'int' },
        { name: 'client_account_id', type: 'int' },
        { name: 'ord_id', type: 'int' },
        { name: 'deal_id', type: 'int' },
        { name: 'client_code', type: 'string' },
        { name: 'market', type: 'string' },
        { name: 'broker_no', type: 'string' },
        { name: 'sb_no', type: 'string' },
        { name: 'sb_order_no', type: 'string' },
        { name: 'branch_code', type: 'string' },
        { name: 'order_no', type: 'string' },
        { name: 'x_order_no', type: 'string' },
        { name: 'x_match_no', type: 'string' },
        { name: 'confirm_no', type: 'string' },
        { name: 'securities_id', type: 'int' },
        { name: 'sec_symbol', type: 'string' },
        { name: 'trustee_id', type: 'string' },
        { name: 'side', type: 'string' },
        { name: 'board', type: 'string' },
        { name: 'price', type: 'float' },
        { name: 'condition_price', type: 'string' },
        { name: 'matched_price', type: 'float' },
        { name: 'qty', type: 'float' },
        { name: 'confirm_qty', type: 'float' },
        { name: 'order_status', type: 'string' },
        { name: 'condition', type: 'string' },
        { name: 'order_type', type: 'string' },
        { name: 'special_order_type', type: 'string' },
        { name: 'basket_no', type: 'string' },
        { name: 'pc_flag', type: 'string' },
        { name: 'pt_type', type: 'string' },
        { name: 'sbl_type', type: 'string' },
        { name: 'order_date', type: 'date' },
        { name: 'order_date_time', type: 'datetime' },
        { name: 'cancel_date_time', type: 'datetime' },
        { name: 'change_date_time', type: 'datetime' },
        { name: 'deal_date', type: 'date' },
        { name: 'deal_time', type: 'datetime' },
        { name: 'ae_code', type: 'string' },
        { name: 'front_user_code', type: 'string' },
        { name: 'cancel_user_code', type: 'string' },
        { name: 'approve_user_code', type: 'string' },
        { name: 'set_trader_id', type: 'string' },
        { name: 'channel_code', type: 'string' },
        { name: 'front_trading_system', type: 'string' },
        { name: 'net_amount', type: 'float' },
        { name: 'commission', type: 'float' },
        { name: 'fee', type: 'float' },
        { name: 'clearing_fee', type: 'float' },
        { name: 'trading_fee', type: 'float' },
        { name: 'settlement_fee', type: 'float' },
        { name: 'vat', type: 'float' },
        { name: 'withholding_tax', type: 'float' },
        { name: 'manual_commission_flag', type: 'boolean' }
      ]
  });

  return OrdDealStore;
});
        
