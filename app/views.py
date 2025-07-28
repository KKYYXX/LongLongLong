#放视图
from flask import Blueprint,request
from app.models import TryModel
from app.plugins import db

blue = Blueprint('blue',__name__)

#视图
@blue.route('/dept/info/<id>',methods=['GET'])
#数据查询模型
def getDepInfo(id):

    dept= TryModel.query.get(id)

    return f'序号：{ dept.id }，名字：{ dept.name }'

#记录添加
@blue.route('/dept/add',methods=['POST'])
def addDepinfo():
    try1 = (TryModel(
    name = request.args.get('name'),
    id =request.args.get('id')
    ))
    db.session.add(try1)
    db.session.commit()

    return "添加信息成功"

#记录修改
@blue.route('/dept/add',methods=['POST'])
def addDepinfo():

    try1 = (TryModel(
    name = request.args.get('name'),
    id =request.args.get('id')
    ))
    db.session.add(try1)
    db.session.commit()

    return "添加信息成功"
