"""
Stock market prediction using Markov chains.

For each function, replace the return statement with your code.  Add
whatever helper functions you deem necessary.
"""

import comp140_module3 as stocks
import random
from collections import defaultdict
### Model
   
def markov_chain(data, order):
    """
    Create a Markov chain with the given order from the 
    given list of data.
    """
    model={}
#	history which consists of a list of continuos number based on given
#	list named data is the key of the dictionary named model 
#	In this way, the data will be cut into several fragments whose length
#	equal to order. Then this part will calculate the frequency of each number
#	that appears on the next state
    for index in range(0,len(data)-order):
        history=data[index:index+order]
        history=tuple(history)
        future=data[index+order]
        if history not in model:
            model[history]=defaultdict(float)
        model[history][future]+=1
#	The following part is used to calculate the probability of numbers that will appear on the next state
#	as the value of the dictionary
    for key_value in model:
        total_frequency=0
        for currency in model[key_value]:
            total_frequency+=model[key_value][currency]
        for new_currency in model[key_value]:
            model[key_value][new_currency]/=float(total_frequency)
             
    
    return model

def weight_number(dictionary):
    """
    This function is used to generate random choices with weight
    when given a dictionary
    """
    dict_item=dictionary.items()
    dict1={}
    middle=[0]
    weight=0
#	The following part is used to generate a new dictionary whose value euqals to keys
#	of the given dictionary and keys equal to the index of the list(the list is got by calling item()
#	function() to the given dictionary). At the same time it will push weight into an empty list named
#	as middle
    for new_index in range(0,len(dict_item)):
        weight+=dict_item[new_index][1]
        middle.append(weight)
        dict1[new_index+1]=dict_item[new_index][0]
    middle.append(1)
    radonumber=random.random()
#	The following part is used to generate random choices after the judgement that whether random numbers
#	are between the values that are represented by middle[new_index] and middle[new_index+1]
    for new_index in range(0, len(middle)):
        if radonumber>=middle[new_index] and radonumber<middle[new_index+1]:
            return dict1[new_index+1]
    
### Predict
def predict(model, last, num):
    """
    Predict the next num values given the model and the last values.
    """
    list1=list(last)
    result=[]
    while len(result)<num:
        tuple1=tuple(list1)
#	The following part is used to generate a number to predict the next day's change randomly
#	when the state is not in the Markov chain
        if tuple1 not in model:
            final=random.randrange(0,4)
        else:
            final=weight_number(model[tuple1])
        result.append(final)
        list1.pop(0)
        list1.append(final)
    return result


### Error

def mse(result, expected):
    """
    Calculate the mean squared error between the sequences 
    result and expected.
    """
    sum_square=0
    for number in range(0,len(result)):
        square_difference=(result[number]-expected[number])**2
        sum_square=sum_square+square_difference
    mean= sum_square/float(len(result))
    return mean



### Experiment

def run_experiment(train, order, test, future, actual, trials):
    """
    Run an experiment to predict the future of the test
    data given the training data.  Returns the average 
    mean squared error over the number of trials.
    
    train  - training data
    order  - order of the markov model to use
    test   - "order" days of testing data
    future - number of days to predict
    actual - actual results for next "future" days
    trials - number of trials to run
    """ 
    new_model=markov_chain(train,order)
    new_error=0
    final_index=0
#	The following part is used to calculate the averae mean squared error 
#	under the number of trials when given the prediction of the future of
#	the test data given the training data
    while final_index<trials:
        new_future=predict(new_model, test, future)
        new_error+=mse(new_future, actual)
        final_index+=1
    average_error=new_error/float(trials)
    return average_error


### Application

def run():
    """
    Run application.

    You do not need to modify any code in this function.  You should
    feel free to look it over and understand it, though.
    """
    # Get the supported stock symbols
    symbols = stocks.get_supported_symbols()
    
    # Get stock data and process it

    # Training data
    changes = {}
    bins = {}
    for symbol in symbols:
        prices = stocks.get_historical_prices(symbol)
        changes[symbol] = stocks.compute_daily_change(prices)
        bins[symbol] = stocks.bin_daily_changes(changes[symbol])

    # Test data
    testchanges = {}
    testbins = {}
    for symbol in symbols:        
        testprices = stocks.get_test_prices(symbol)
        testchanges[symbol] = stocks.compute_daily_change(testprices)
        testbins[symbol] = stocks.bin_daily_changes(testchanges[symbol])

    # Display data
    #   Comment these 2 lines out if you don't want to see the plots
    stocks.plot_daily_change(changes)
    stocks.plot_bin_histogram(bins)

    # Run experiments
    orders = [1, 3, 5, 7, 9]
    ntrials = 500
    days = 5

    for symbol in symbols:
        print symbol
        print "===="
        print "Actual:", testbins[symbol][-days:]
        for order in orders:
            error = run_experiment(bins[symbol], order,
                                   testbins[symbol][-order-days:-days], days, 
                                   testbins[symbol][-days:], ntrials)
            print "Order", order, ":", error
        print            
 
# You might want to comment this out while you are developing your code.           
# run()


