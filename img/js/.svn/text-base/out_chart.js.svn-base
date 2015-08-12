"use strict";
var OutChart = {
        ShowBtcE:function(){
                $.getJSON('/foreign/stock/btce/btc_usd/minute/0&callback=?',
                 function(Data){         
                $('#chart_trade').hide("slow");
                Highcharts.setOptions({
                        global : {
                                useUTC : false
                        }
                });
                
                // Create the chart
                $('#chart_btce').highcharts('StockChart', {
                        chart : {
                                events : {
                                        load : function() {
                                                $('#chart_btce').show("fast");
                                                // set up the updating of the chart each second
                                                var series = this.series[0];
                                                setInterval(function() {
                                                        
                                                        
                                                        
                                                        
                                                        
                                                        
                                                        var x = (new Date()).getTime(), // current time
                                                        y = Math.round(Math.random() * 100);
                                                        series.addPoint([x, y], true, true);
                                                        
                                                        
                                                        
                                                }, 4000);
                                        }
                                }
                        },
                        
                        rangeSelector: {
                                buttons: [{
                                        count: 1,
                                        type: 'minute',
                                        text: '1M'
                                }, {
                                        count: 5,
                                        type: 'minute',
                                        text: '5M'
                                }, {
                                        type: 'all',
                                        text: 'All'
                                }],
                                inputEnabled: false,
                                selected: 0
                        },
                        
                        title : {
                                text : 'BTC-e price BTC/USD'
                        },
                        
                        exporting: {
                                enabled: false
                        },
                        
                        series : [{
                                name : 'BTC-e ',
                                data : Data
                        }]
                });
            }  
                

        }
      
}