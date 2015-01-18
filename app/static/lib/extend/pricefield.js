// Name : Pricefield plugin 
// Description : A textfield plugin to act like price field.
// Version : 1.0
//
// Usage :
// {
//      xtype: 'textfield',
//      plugins: [
//          { xclass: 'Ext.plugin.Price' }
//      ],
//      priceConfig: {
//         symbolBeforeAmount: true,
//         currencySymbol: '\u0E3F', //  use '\u20AC' for euro sign (= unicode)
//         decimalSeparator: '.',
//         decimalPrecision: 2,
//         thousandsSeparator: ',',
//         negativeAmountClass: 'negative-number',
//         hiddenCls: 'number',
//         allowNegative: true
//      }
// }
//
// original source : http://www.sencha.com/forum/showthread.php?105951-Form-field-currency-plugin
// modified for work with ExtJS 4.2.x

Ext.define("Ext.plugin.Price", {
    alias: 'plugin.price',

    init: function(textField) {
        Ext.apply(textField, {
            onRender: Ext.Function.createSequence(textField.onRender, function() {
                // default option
                var defaultConfig = {
                    symbolBeforeAmount: true,
                    currencySymbol: '\u0E3F', //  use '\u20AC' for euro sign (= unicode)
                    decimalSeparator: '.',
                    decimalPrecision: 2,
                    thousandsSeparator: ',',
                    negativeAmountClass: 'negative-number',
                    hiddenCls: 'number',
                    allowNegative: true
                }

                this.priceConfig = Ext.apply(defaultConfig, this.priceConfig || {});

                var c = this.priceConfig;

                if(c.allowNegative){
                  this.maskRe =  new RegExp( '[\\-\\d\\'+ c.decimalSeparator+( c.thousandsSeparator.trim()!==""? "\\"+ c.thousandsSeparator:"")+']','i' );
                }else{
                  this.maskRe =  new RegExp( '[\\d\\'+ c.decimalSeparator+( c.thousandsSeparator.trim()!==""? "\\"+ c.thousandsSeparator:"")+']','i' );
                }

                this.setFieldStyle("{ text-align: right; }");

                var name = this.name || this.el.dom.name;

                this.validator = function(theVal){
                    if (isNaN(parseFloat(this.formatHiddenValue(theVal))) && theVal != "") {
                        return c.invalidAmountText || false;
                    }
                    return true;
                };

                this.hiddenField = this.el.insertSibling({
                     tag:'input'
                    ,type:'hidden'
                    ,name:name
                    ,cls: c.hiddenCls 
                    //,value:this.formatHiddenValue(this.value)
                });

                this.hiddenName = name; // otherwise field is not found by BasicForm::findField
                this.el.dom.removeAttribute('name');

                this.on('keyup', this.updateHidden, this);
                this.on('focus', this.cleanForEdit, this);
                this.on('blur', this.updateShown, this);
            }),

            _getValue: Ext.form.TextField.prototype.getValue,

            setValue: function(theValue){
                Ext.form.TextField.superclass.setValue.call(this, theValue);
                this.updateShown();
            },

            updateShown: function(){
                if (this.isValid() && this._getValue() && this._getValue().trim() !== ""){
                    // alias 
                    var c = this.priceConfig;
                    var newValue = "";
                    var currentValue = parseFloat(this.formatHiddenValue(this._getValue()));

                    // max precision
                    var dummyZero = "000000000000000000";
                    var toShowFormat = '0'+ c.thousandsSeparator+'0.' + dummyZero.substring(0, c.decimalPrecision);
                    if (c.decimalSeparator === ',' ) {
                        toShowFormat = '0'+ c.thousandsSeparator + '0,00/i';
                    }

                    var absValue = Math.abs(currentValue);
                    if (c.symbolBeforeAmount === true ) {
                        newValue = c.currencySymbol.trim() + " " +
                                    (currentValue < 0 ? "-": "") +
                                    Ext.util.Format.number(absValue, toShowFormat);
                    }
                    else {
                        newValue = Ext.util.Format.number(absValue, toShowFormat) +
                                    " " + (currentValue < 0 ? "-": "") +
                                        c.currencySymbol.trim();
                    }

                    var input = this.el.query('input')[0];
                    if (currentValue < 0) {
                        input.className += (" " + c.negativeAmountClass);
                    }
                    else {
                        input.className = input.className.replace(new RegExp(c.negativeAmountClass), "").trim();
                    }

                    this.setRawValue(newValue);
                    this.updateHidden();
                 }
            },

            updateHidden:function() {
                this.hiddenField.dom.value = ( this.isValid() ? this.formatHiddenValue(this._getValue()) :"" );
            },

            formatHiddenValue: function(rawAmount){
                if (!rawAmount) { return; }
                var conf = this.priceConfig;
                if(conf){
                    rawAmount = String(rawAmount).replace(conf.currencySymbol,'');
                    rawAmount = String(rawAmount).replace(new RegExp(conf.thousandsSeparator,"g"), '');
                    rawAmount = String(rawAmount).replace(conf.decimalSeparator,'.');
                }
                return rawAmount.trim();
            },

            getValue: function  () {
                return parseFloat(this.formatHiddenValue(this._getValue()));
            },

            cleanForEdit:function(textField) {
                var conf = this.priceConfig;
                this.setRawValue(String(this._getValue()).replace(conf.currencySymbol,'').trim());
                this.setRawValue(String(this._getValue()).replace(new RegExp(conf.thousandsSeparator, "g"),'').trim());
            },

            reset: function() {
               this.setRawValue(0); 
            }
        });
    }
});
