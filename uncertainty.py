# -*- coding:utf-8 -*-
""" **datetime :2018.1.6** """
__version__ = 1.0
__author__ = 'huangqican'

import pandas as pd
import numpy as np
from flask import Flask, make_response, request
from flask_restful import Api, reqparse, Resource
import json
import uncertaintyFun as unFun

app = Flask(__name__)
api = Api(app)


@api.representation('application/json')
def output_json(data, code=200, headers=None):
    """Makes a Flask response with a JSON encoded body"""
    if isinstance(data, str):
        resp = make_response(data, code)
    else:
        resp = make_response(json.dumps(data, cls=NumpyEncoder).replace('NaN', 'null'), code)
    resp.headers.extend(headers or {})
    return resp


""" URL = /uncertainty/BasicInfor
    获取展示页面的基本信息"""


class BasicInfor(Resource):
    def post(self):
        resp_header = {'Access-Control-Allow-Origin': '*'}  # 允许跨域请求
        try:
            # if 1==1:
            temp = request.get_json()

            """修改wt_data和power_curve的格式"""
            dfc = DataFormatConversion()
            wt_data = dfc.wt_data_conv(temp['wt_data'])
            power_curve = dfc.power_curve_conv(temp['power_curve'])

            uncer = unFun.Basic_Info(wt_data)
            data = uncer.basic(power_curve)
            data = json.dumps(data, cls=NumpyEncoder).replace('NaN', 'null')
            return data, 200, resp_header
        except TypeError:
            msg = 'Json serislization error'
            resp_status = 500
            data = {'code': '3', 'data': {}, 'msg': msg}
            data = json.dumps(data, cls=NumpyEncoder)
            return data, resp_status
        except Exception as e:
            msg = e
            resp_status = 404
            data = {'code': '4', 'data': {}, 'msg': str(msg)}
            data = json.dumps(data, cls=NumpyEncoder)
            return data, resp_status


""" URL = /uncertainty/MastHorizont
    获取测风塔水平代表性"""


class MastHorizont(Resource):
    def post(self):
        resp_header = {'Access-Control-Allow-Origin': '*'}  # 允许跨域请求
        try:
        # if 1==1:
            temp = request.get_json()

            """修改wt_data的格式"""
            dfc = DataFormatConversion()
            wt_data = dfc.wt_data_conv(temp['wt_data'])
            horizont = temp['horizont']

            uncer = unFun.Basic_Info(wt_data)
            data = uncer.mast_horizont(horizont)
            data = json.dumps(data, cls=NumpyEncoder).replace('NaN', 'null')
            return data, 200, resp_header
        except TypeError:
            msg = 'Json serislization error'
            resp_status = 500
            data = {'code': '3', 'data': {}, 'msg': msg}
            data = json.dumps(data, cls=NumpyEncoder)
            return data, resp_status
        except Exception as e:
            msg = e
            resp_status = 404
            data = {'code': '4', 'data': {}, 'msg': str(msg)}
            data = json.dumps(data, cls=NumpyEncoder)
            return data, resp_status


""" URL = /uncertainty/MastVertical
    获取测风塔垂直代表性"""


class MastVertical(Resource):
    def post(self):
        resp_header = {'Access-Control-Allow-Origin': '*'}  # 允许跨域请求
        try:
        # if 1==1:
            temp = request.get_json()

            """修改wt_data的格式"""
            dfc = DataFormatConversion()
            wt_data = dfc.wt_data_conv(temp['wt_data'])
            vertical = temp['vertical']

            uncer = unFun.Basic_Info(wt_data)
            data = uncer.mast_vertical(vertical)
            data = json.dumps(data, cls=NumpyEncoder).replace('NaN', 'null')
            return data, 200, resp_header
        except TypeError:
            msg = 'Json serislization error'
            resp_status = 500
            data = {'code': '3', 'data': {}, 'msg': msg}
            data = json.dumps(data, cls=NumpyEncoder)
            return data, resp_status
        except Exception as e:
            msg = e
            resp_status = 404
            data = {'code': '4', 'data': {}, 'msg': str(msg)}
            data = json.dumps(data, cls=NumpyEncoder)
            return data, resp_status


""" URL = /uncertainty/StatInfo
    获取所需要的统计信息"""


class StatInfo(Resource):
    def post(self):
        resp_header = {'Access-Control-Allow-Origin': '*'}  # 允许跨域请求
        try:
        # if 1==1:
            temp = request.get_json()

            """修改wt_data和power_curve的格式"""
            dfc = DataFormatConversion()
            wt_data = dfc.wt_data_conv(temp['wt_data'])
            power_curve = dfc.power_curve_conv(temp['power_curve'])

            loss = temp['loss']
            uncertainty = temp['uncertainty']
            vertical = temp['vertical']
            horizont = temp['horizont']
            temp = unFun.Stat(wt_data, power_curve, loss, uncertainty, vertical, horizont)
            data = temp.result()
            data = json.dumps(data, cls=NumpyEncoder).replace('NaN', 'null')
            return data, 200, resp_header
        except TypeError:
            msg = 'Json serislization error'
            resp_status = 500
            data = {'code': '3', 'data': {}, 'msg': msg}
            data = json.dumps(data, cls=NumpyEncoder)
            return data, resp_status
        except Exception as e:
            msg = e
            resp_status = 404
            data = {'code': '4', 'data': {}, 'msg': str(msg)}
            data = json.dumps(data, cls=NumpyEncoder)
            return data, resp_status

# *******************


class DataFormatConversion():
    def wt_data_conv(self, wt_data):
        """
        将形式如data = [{'a':1,'b':2},{'a':2,'b':3},{'a':3,'b':4}]的数据转换为下面格式
        data = {'a':[1,2,3],'b':[2,3,4]}
        :param wt_data:
        :return:
        """
        temp = pd.DataFrame(wt_data)
        wt_data_new = {}
        for i in temp.columns:
            wt_data_new[str(i)] = temp[i].tolist()
        return wt_data_new

    def power_curve_conv(self, power_curve):
        """
        将形式如data = {'GW115/2000':[{'ws':1,'power':2},{'ws':2,'power':3},{'ws':3,'power':4}],
                        'GW121/2000':[{'ws':1,'power':2},{'ws':2,'power':3},{'ws':3,'power':4}]}的数据转换为下面格式
        data = {'GW115/2000':{'ws':[1,2,3],'power':[2,3,4]},
                'GW115/2000':{'ws':[1,2,3],'power':[2,3,4]}}
        :param power_curve:
        :return:
        """
        power_curve_new = {}
        for k in power_curve.keys():
            power_curve_new[k] = self.wt_data_conv(power_curve[k])
        return power_curve_new


# *******************
class NumpyEncoder(json.JSONEncoder):
    """
    Convert numpy type to python type for json.dumps

    Reference:
    1.http://stackoverflow.com/questions/27050108/convert-numpy-type-to-python
    2.https://docs.python.org/2/library/json.html#json.JSONEncoder
    """

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyEncoder, self).default(obj)
# *******************


api.add_resource(BasicInfor, '/uncertainty/BasicInfor')
api.add_resource(MastHorizont, '/uncertainty/MastHorizont')
api.add_resource(MastVertical, '/uncertainty/MastVertical')
api.add_resource(StatInfo, '/uncertainty/StatInfo')


#********************************************************************************
if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=8080)
    # app.run(host='localhost', port=8090)
