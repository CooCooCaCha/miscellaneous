import urllib.request;
import time;
import json;

s_one         = 0;
alpha         = 0.7;
keep_looping  = 1;
price_array   = [];

buy_limit  = 10;
sell_limit = 10;

bitcoins     = [];
current_cash = 50;
savings      = current_cash * 0.4;

def get_ticker_price():
    ticker_data_json = urllib.request.urlopen( 'https://www.bitstamp.net/api/ticker/' ).read().decode( 'utf-8' );
    return float( json.loads( ticker_data_json )['last'] );

while data_index < len( data ):
    ticker_price = get_ticker_price();

    if( ticker_price > 10000 or ticker_price < 1 ):
        continue;

    price_array.append( ticker_price );

    if( len( price_array ) < 1000 ):
        print( 'Initializing price array' );
        time.sleep( 5 );
        continue;

    if( len( price_array ) > 5000 ):
        price_array.pop( 0 );

    s_one  = price_array[0];
    s_one += price_array[1];
    s_one += price_array[2];
    s_one += price_array[3];
    s_one += price_array[4];

    s_one = s_one / 5.0;

    ema = s_one;
    sma = 0;
    for x in range( 0, len( price_array ) ):
        ema  = (price_array[x] * alpha) + (ema * (1 - alpha));
        sma += price_array[x] * (1/len(price_array));

    bitcoin_average  = 0;
    bitcoin_quantity = 0;

    for x in range( 0, len( bitcoins ) ):
        bitcoin_average  += bitcoins[x]['price'] * bitcoins[x]['quantity'];
        bitcoin_quantity += bitcoins[x]['quantity'];

    if( bitcoin_quantity > 0 ):
        bitcoin_average = bitcoin_average / bitcoin_quantity;

    if( (ema - bitcoin_average > 2) and (bitcoin_average > 0)  ):
        sell_amount = bitcoin_average * len( bitcoins );
        current_cash += sell_amount;
        savings      += sell_amount * 0.4;
        print( 'SELL: ' + str( ticker_price ) + ' AVG: ' + str( bitcoin_average ) );
        bitcoins = [];

    could_buy = (current_cash - savings) / ticker_price;

    if( (current_cash > 0) and (could_buy > 0.01) and (sma - ema > 2) ):
        bitcoins.append( { 'price': ticker_price, 'quantity': could_buy } );
        current_cash -= ticker_price * could_buy;
        print( 'BUY: ' + str( ticker_price ) + ' AVG: ' + str( bitcoin_average ) );

    print( 'EMA: ' + str( ema ) + ' SMA: ' + str( sma ) + ' BTC AVG: ' + str( bitcoin_average ) + ' BTC QTY: ' + str( bitcoin_quantity ) + ' Last: ' + str( ticker_price ) + ' Cash: ' + str( current_cash ) + ' Bitcoins: ' + str( len( bitcoins ) ) );

    time.sleep( 5 );
