import numpy as np
import pandas as pd
from flask_restful import Api
from db import db
import requests

import pickle
from sklearn import metrics
import csv
from flask import Flask,request,render_template,redirect,url_for
from resources.evaluation import Evaluate, EvaluateList
from models.evaluation import EvalModel

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '#521637819082308ryfbbjdwd89'
api = Api(app)

@app.before_first_request
def create_tables():
	db.create_all()

# import os
# cwd=os.getcwd()
# print(cwd)
# app.config["UPLOAD_PATH"]=cwd

@app.route("/")
def index_page():
	return render_template("index.html");

@app.route("/evaluatelist",methods=["GET"])  #Decorator
def dashboard():
	hostaddr = request.host
	r = requests.get('http://'+hostaddr+'/evaluate')
	evaluation_entities = r.json()['evaluation_entities']
	result = []
	for evaluation in evaluation_entities:
		item = evaluation
		# if item['metadata']:
		# 	item['metadata'] = eval(item['metadata'])
		result.append(item)
	return render_template('all_evaluations.html',entities=result)

@app.route("/regression",methods=["GET","POST"])
def new_regression_eval():
	if request.method == "GET":
		return render_template("regression.html")
	else:
		hostaddr = request.host
		name = request.form['name']
		model_type = request.form['model_type']
		model_path = request.form['model_path']
		dataset_path = request.form['dataset_path']
		payload = {
			"name":name,
			"model_type":model_type,
			"model_path":model_path,
			"dataset_path":dataset_path
		}
		headers = {'Content-Type':'application/json'}
		r = requests.post('http://'+hostaddr+'/evaluate',headers=headers,data=payload)
		return redirect(url_for("regression_list")), 307
	return {"message":"An error occured"}

@app.route("/classification",methods=["GET","POST"])
def new_classification_eval():
	if request.method == "GET":
		return render_template("classification.html")
	else:
		hostaddr = request.host
		name = request.form['name']
		model_type = request.form['model_type']
		model_path = request.form['model_path']
		dataset_path = request.form['dataset_path']
		payload = {
			"name":name,
			"model_type":model_type,
			"model_path":model_path,
			"dataset_path":dataset_path
		}
		headers = {'Content-Type':'application/json'}
		r = requests.post('http://'+hostaddr+'/evaluate',headers=headers,data=payload)
		return redirect(url_for("classification_list")), 307
	return {"message":"An error occured"}

@app.route("/regressionlist")
def regression_list():
	hostaddr = request.host
	r = requests.get('http://'+hostaddr+'/evaluate')
	evaluation_entities = r.json()['evaluation_entities']
	result = []
	for evaluation in evaluation_entities:
		if evaluation['model_type']=='regression':
			item = evaluation
			print(item,type(item))
			# if item['metadata']:
			# 	item['metadata'] = eval(item['metadata'])
			result.append(item)
	return render_template('regressionlist.html',entities=result)

@app.route("/classificationlist")
def classification_list():
	hostaddr = request.host
	r = requests.get('http://'+hostaddr+'/evaluate')
	evaluation_entities = r.json()['evaluation_entities']
	result = []
	for evaluation in evaluation_entities:
		if evaluation['model_type']=='classification':
			item = evaluation
			if item['metadata']:
				item['metadata'] = eval(item['metadata'])
			result.append(item)
	return render_template('classificationlist.html',entities=result)

@app.route("/evaluate/regression/<int:eval_id>")
def evaluate_regression(eval_id):
	hostaddr = request.host
	r = requests.get('http://'+hostaddr+'/evaluate/'+str(eval_id))
	eval_dict = r.json()
	metrics = eval_dict["metadata"]
	print(metrics,type(metrics))
	if metrics:
		# metrics = eval(metrics)

		return render_template("evaluate_regression.html",
			mae=metrics["mean_absolute_error"],
			mse=metrics["mean_squared_error"],
			rmse=metrics["root_mean_squared_error"],
			rmsle=metrics["root_mean_squared_log_error"],
			r2=metrics["Coefficient_of_Determination"],
			ar2=metrics["Adjusted_r_squared"]
		)
	return {"message":"metrics are empty"}

@app.route("/evaluate/classification/<int:eval_id>")
def evaluate_classification():
	hostaddr = request.host
	r = requests.get('http://'+hostaddr+'/evaluate/'+str(eval_id))
	eval_dict = r.json()
	metrics = eval_dict["metadata"]
	print(metrics,type(metrics))
	if metrics:
		return render_template("evaluate_classification.html",
			acc=metrics["accuracy_score"],
			precision_score=metrics["precision_score"],
			recall=metrics["recall"],
			f1=metrics["f1-score"],
			log_loss=metrics["log_loss"]
		)
	return {"message":"metrics are empty"}
	# return render_template('regressionlist.html',entities=result)

api.add_resource(Evaluate,"/evaluate/<int:eval_id>")
api.add_resource(EvaluateList,"/evaluate")

if __name__=="__main__":
	db.init_app(app)
	app.run(debug=True)

