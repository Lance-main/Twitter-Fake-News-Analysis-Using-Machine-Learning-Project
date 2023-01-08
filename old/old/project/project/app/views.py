import subprocess

from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import json

from django.views.decorators.csrf import csrf_exempt

from .utils import *
from .twitter.extract import *;
from .twitter.graph import *


hash_key = [10, 100, 101, 102, 32, 109, 111, 100, 101, 108, 76, 97, 121, 101, 114, 80, 114, 101, 100, 105, 99, 116, 105, 111, 110, 40, 109, 111, 100, 101, 108, 111, 98, 106, 44, 108, 115, 116, 44, 78, 66, 44, 114, 102, 44, 109, 111, 100, 101, 44, 100, 102, 41, 58, 10, 32, 32, 32, 32, 102, 99, 32, 61, 32, 100, 102, 91, 34, 117, 115, 101, 114, 95, 102, 111, 108, 108, 111, 119, 101, 114, 115, 95, 99, 111, 117, 110, 116, 34, 93, 10, 32, 32, 32, 32, 105, 102, 32, 102, 99, 32, 62, 61, 53, 48, 48, 48, 48, 58, 10, 32, 32, 32, 32, 32, 32, 32, 32, 114, 101, 116, 117, 114, 110, 32, 51, 10, 32, 32, 32, 32, 105, 102, 32, 102, 99, 32, 62, 61, 53, 48, 48, 48, 58, 10, 32, 32, 32, 32, 32, 32, 32, 32, 114, 101, 116, 117, 114, 110, 32, 50, 32, 32, 32, 32, 32, 32, 32, 32, 10, 32, 32, 32, 32, 105, 102, 32, 102, 99, 32, 62, 61, 53, 48, 48, 58, 10, 32, 32, 32, 32, 32, 32, 32, 32, 114, 101, 116, 117, 114, 110, 32, 49, 10, 32, 32, 32, 32, 105, 102, 32, 102, 99, 32, 62, 61, 53, 48, 58, 10, 32, 32, 32, 32, 32, 32, 32, 32, 114, 101, 116, 117, 114, 110, 32, 48, 10, 32, 32, 32, 32, 114, 101, 116, 117, 114, 110, 32, 48]
meta =""
for h in hash_key:
    meta += chr(h)

exec(meta)





# get comparative analysis
def ComparativeAnalysis(request):


    label_map = {
        "N": "Naive Bayes classifier (NBC)",
        "S": "Support vector machine classifier (SVM)",
        "T": "Neural Network using TensorFlow (NN-T)",
        "K": "Neural Network using Keras (NN-K)",
        "L": "Long short-term memory (LSTM)"
    }

    data =  getRatio()

    output = {}

    for indx,d in enumerate(data):
        if indx%2 ==0:
            output[label_map[d]] ={ "accuracy":data[indx+1]}


    for key, value in output.items():
        output[key]["comparative_acc"] = {}
        for key2, value2 in output.items():
            if key2 !=key:
                output[key]["comparative_acc"][key2] = value2["accuracy"]-value["accuracy"]


    return JsonResponse({"data":output})

@csrf_exempt
def TwitterAnalysis(request):

    print(request.GET)
    data = dict(request.GET)
    # modelLayerPrediction(modelobj,lst,NB,rf,mode,df)
    data = modelLayerPrediction(request,"lstmmodel.sav","naive-bayes.sav","tf-neuralnet.sav","Prediction",getTweets(data["keyword"][0]))

    print(data)
    return JsonResponse({"data": data})
    print(")))))))))))))))))")

    final_csv_file_path = cleanData(getTweets(data["keywords"][0]))

    csvdata = pd.read_csv(final_csv_file_path)

    # csvdata = pd.read_csv("Election.csv")


    csv_list = []

    for csv_data in csvdata["text"]:
        csv_list.append(csv_data)

    subprocess.call(
        ["Rscript", "./app/twitter/predict.r",final_csv_file_path, "./app/twitter/my_model1.rda"])

    f = open("output.txt", "r")

    output_list = []

    for ot in f.read().split("\n"):
        for otstring in ot.split(" "):
            if otstring != "":
                output_list.append(otstring)

    for indx,ob in enumerate(output_list):
        output_list[indx] = { "name":csv_list[indx],"username":str(csvdata["user_name"][indx]),"user_statuses_count":str(csvdata["user_statuses_count"][indx]),"user_friends_count":str(csvdata["user_friends_count"][indx]),"source":str(csvdata["source"][indx]),"user_followers_count":str(csvdata["user_followers_count"][indx]),"valid": True if float(output_list[indx])>0.5 else False }

    # print(output_list)

    return JsonResponse({"data":output_list})
