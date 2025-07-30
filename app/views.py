#放视图
from flask import Blueprint,request
from app.models import TryModel
from app.plugins import db
from sqlalchemy import func

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

    info_1 = TryModel.query.filter(TryModel.name == '王五').first()  #只显示第一个查询结果

    #多条件查询
    info_2 = TryModel.query.filter(TryModel.name == '王五',TryModel.id == 3 ).all()  #显示所有查询结果

    return '查询成功'

#模糊查询
@blue.route('/dept/like',methods=['GET'])
def likedeptdatail():

    #            张%                 %三                %三%     都可
    # 分别对应 startswith('张')   endswith('三')     contains('三')
    info_1 = TryModel.query.filter(TryModel.name.like('张%')).all()

    result = []
    for item in info_1:
        result.append(f'序号：{item.id}，名字：{item.name}')
    return '\n'.join(result)

#模糊查询2.0
@blue.route('/dept/like1',methods=['GET'])
def like1deptdatail():

    info_1 = TryModel.query.filter(TryModel.name.startswith('张')).all()

    result = []
    for item in info_1:
        result.append(f'序号：{item.id}，名字：{item.name}')
    return '\n'.join(result)

#查询结果按升序排列显示，默认按升序
@blue.route('/dept/order',methods=['GET'])
def orderdeptdatail():

    info_1 = TryModel.query.order_by(TryModel.id).all()

    result = []
    for item in info_1:
        result.append(f'序号：{item.id}，名字：{item.name}')
    return '\n'.join(result)

#查询结果按降序排列显示
@blue.route('/dept/order1',methods=['GET'])
def order1deptdatail():

    info_1 = TryModel.query.order_by(TryModel.id.desc()).all()

    result = []
    for item in info_1:
        result.append(f'序号：{item.id}，名字：{item.name}')
    return '\n'.join(result)

#查询结果只显示前几条
@blue.route('/dept/top',methods=['GET'])
def topdeptdatail():

    #只看前两条
    info_1 = TryModel.query.limit(2).all()

    result = []
    for item in info_1:
        result.append(f'序号：{item.id}，名字：{item.name}')
    return '\n'.join(result)

#分组查询
@blue.route('/dept/group',methods=['GET'])
def groupdeptdatail():
    #按性别分组
    info = db.session\
        .query(TryModel.gender,func.count(TryModel.gender).label('count_gender'))\
        .group_by(TryModel.gender).all()

    result = []
    for item in info:
        result.append(f'性别：{item.gender}，数量：{item.count_gender}')
    return '\n'.join(result)

