import json
import pandas as pd
import numpy as np
from datetime import *

class PredictionSerializer(json.JSONEncoder):
    pk = 0

    def default(self, prediction):
        model = 'figures.Prediction'
        self.pk += 1
        fields = prediction.__dict__

        django_dict= {
            'model': model,
            'pk': self.pk,
            'fields': fields
        }

        return django_dict

class Prediction:
    def __init__(self, district, dem_vote, std, dem_win, dt):
        self.district = district
        self.dem_perc = dem_vote
        self.rep_perc = 1 - self.dem_perc
        self.prediction_std = std
        self.dem_win_percent = dem_win
        self.rep_win_percent = 1 - self.dem_win_percent
        self.date = str(dt)

class NationalPrediction:
    def __init__(self, histogram_data):
        self.dem_win_perc = round(sum(histogram_data[218:])/sum(histogram_data)*100,2)
        #self.rep_perc = 1 - self.dem_perc
        temp_histogram = []
        for i, val in enumerate(histogram_data):
            if i < 218:
                c = "#FF3000"
            else:
                c = "#0084FF"
            temp_histogram.append({ "x": i, "y": val*100, "color": c})
        self.histogram_data = str(temp_histogram[180:281])
            
class NationalPredictionSerializer(json.JSONEncoder):
    pk = 0

    def default(self, prediction):
        model = 'figures.NationalPrediction'
        self.pk += 1
        fields = prediction.__dict__

        django_dict= {
            'model': model,
            'pk': self.pk,
            'fields': fields
        }

        return django_dict


prediction_list = []
for row in open('district_results.csv','r').read().split("\n")[1:-1]:
    row = row.split(',')
    dt = datetime(int(row[0]),int(row[1]),int(row[2]),12)
    prediction_list.append(Prediction(row[3],float(row[4]),float(row[5]),float(row[6]),dt))
    
with open('predictions.json', 'w') as file:
    json.dump(prediction_list, cls=PredictionSerializer, fp=file)

nats = NationalPrediction([float(i) for i in open("histogram.csv","r").read().split("\n")[:436]])

with open('national_predictions.json', 'w') as file:
    json.dump([nats], cls=NationalPredictionSerializer, fp=file)
