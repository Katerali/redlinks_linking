import pandas as pd





# takes a cell value as an input
def babel_net_model(predictions):
    if predictions == 1:
        return True
    else:
        return False  



def evaluate_BabelNet_model(ground_truth, model_results):
    if ground_truth == model_results == False:
        return 'TN'
    if ground_truth == False and model_results == True:
        return 'FP'
    if ground_truth == model_results == True:
        return 'TP'
    if ground_truth == True and model_results == False:
        return 'FN'
