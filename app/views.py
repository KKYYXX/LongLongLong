#放视图
from flask import Blueprint,request,jsonify
from app.models import TryModel, Projects15, UserModel
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
    name = request.form.get('name'),
    id =request.form.get('id',type=int)
    ))
    db.session.add(try1)
    db.session.commit()

    return "添加信息成功"

#记录更新
@blue.route('/dept/upd',methods=['POST'])
def updDepinfo():

    try2 = TryModel.query.get(request.form.get('id'))
    try2.name = request.form.get('name')

    db.session.commit()

    return "修改信息成功"

#记录删除
@blue.route('/dept/del',methods=['POST'])
def delDepinfo():

    try3 = TryModel.query.get(request.form.get('id'))

    db.session.delete(try3)

    db.session.commit()

    return "删除信息成功"


#信息查询（条件查询）显示的是列表的形式
@blue.route('/dept/find',methods=['GET'])
def finddepts():

    info_1 = TryModel.query.filter(TryModel.name == '陈留').all()

    return '查询成功'

