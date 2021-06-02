import sqlite3
from flask_restful import Resource, reqparse
from models.evaluation import EvalModel
from resources.eval_functions import EvaluationFunctions
from flask import Flask,request,render_template,redirect,url_for, jsonify
import json

class Evaluate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('model_path',
        type=str,
        required=True,
        help="Please provide a model path"
    )
    parser.add_argument('dataset_path',
        type=str,
        required=True,
        help="Please provide a datset path"
    )
    parser.add_argument('model_type',
        type=str,
        required=True,
        help="Please define the type of model"
    )
    parser.add_argument('name',
        type=str,
        required=True,
        help="Please define the name of model"
    )

    def get(self,eval_id):
        evaluation_entity = EvalModel.find_by_id(eval_id)
        print(evaluation_entity, type(evaluation_entity))
        if evaluation_entity:
            eval_dict = evaluation_entity.json()
            # print("here_1")
            # eval_dict = jsonify(evaluation_entity)
            # print("here_2")
            print(eval_dict, type(eval_dict))
            evaluation_object = EvaluationFunctions(eval_dict['model_type'], eval_dict['model_path'], eval_dict['dataset_path'])
            print(evaluation_object, type(evaluation_entity))
            if eval_dict['model_type'] == 'regression':
                metrics = evaluation_object.evaluate_regression()
            else:
                metrics = evaluation_object.evaluate_classification()
            print(metrics, type(metrics))
            print(evaluation_entity.meta)
            evaluation_entity.meta = json.dumps(metrics)
            evaluation_entity.save_to_db()
            return evaluation_entity.json()
            # return metrics

        return {"message":"Requested evaluation entity doesn't exist"}, 404


class EvaluateList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('model_path',
        type=str,
        required=True,
        help="Please provide a model path"
    )
    parser.add_argument('dataset_path',
        type=str,
        required=True,
        help="Please provide a datset path"
    )
    parser.add_argument('model_type',
        type=str,
        required=True,
        help="Please define the type of model"
    )
    parser.add_argument('name',
        type=str,
        required=True,
        help="Please define the name of model"
    )
    def get(self):
        return {"evaluation_entities":[x.json() for x in EvalModel.query.all()]}

    def post(self):
        data = EvaluateList.parser.parse_args()

        item = EvalModel(**data)

        try:
            item.save_to_db()
        except:
            return {"message":"An error occured inserting the evaluation"}, 500

        return item.json(), 201
