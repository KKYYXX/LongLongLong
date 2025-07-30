#放视图
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash

from app.models import TryModel, UserModel, ZCDocument, UploadModel
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

#用户注册接口（返回姓名、号码、微信、密码）
@blue.route('/user/register', methods=['POST'])
def register_user():
    # 获取请求中的注册信息
    name = request.form.get('name')
    phone = request.form.get('phone')
    password = request.form.get('password')
    wx_openid = request.form.get('wx_openid')

    # 查询手机号是否已经注册
    existing_user = UserModel.query.filter_by(phone=phone).first()

    if existing_user:
        # 如果用户已存在，匹配名字和微信号
        if existing_user.name == name and existing_user.wx_openid == wx_openid:
            # 如果匹配，允许注册（返回用户信息）
            user_info = {
                'name': existing_user.name,
                'phone': existing_user.phone,
                'wx_openid': existing_user.wx_openid,
                'password': existing_user.password  # Assuming password is already hashed
            }
            return jsonify(user_info), 200  # Registration successful (user exists and matches)
        else:
            # 如果名字和微信号不匹配，注册失败
            return jsonify({'message': 'User details do not match'}), 400
    else:
        # 如果用户不存在
        return jsonify({'message': 'User not found'}), 404

#转让页面接口（返回姓名、号码、密码）
@blue.route('/user/validate', methods=['POST'])
def validate_user():
    # 获取请求中的数据
    name = request.form.get('name')
    phone = request.form.get('phone')
    password = request.form.get('password')

    # 查询数据库中是否有该用户
    user = UserModel.query.filter_by(phone=phone).first()

    if user:
        # 如果用户存在，验证姓名和密码
        if user.name == name and check_password_hash(user.password, password):
            # 如果姓名和密码匹配，更新principal字段为True
            user.principal = True
            db.session.commit()  # 提交更改

            # 返回用户信息
            user_info = {
                'name': user.name,
                'phone': user.phone,
                'wx_openid': user.wx_openid,
                'principal': user.principal  # 返回更新后的principal值
            }
            return jsonify(user_info), 200  # 匹配成功，返回用户信息
        else:
            # 如果姓名或密码不匹配，返回失败信息
            return jsonify({'message': '姓名或密码错误'}), 400
    else:
        # 如果用户不存在，返回失败信息
        return jsonify({'message': '用户不存在'}), 404

#15项清单的查询权限人员（返回所有query_15为True的姓名和号码）
@blue.route('/user/query_15', methods=['GET'])
def get_users_query_15():
    # 查询所有query_15为True的用户
    users = UserModel.query.filter_by(query_15=True).all()

    # 格式化返回的结果
    result = []
    for user in users:
        result.append({
            'name': user.name,
            'phone': user.phone
        })

    return jsonify(result), 200  # 返回查询结果

#15项清单查询权限人员的添加（返回所有query_15为True的姓名和号码）
@blue.route('/user/add', methods=['POST'])
def add_user():
    # 获取请求中的数据
    name = request.form.get('name')
    phone = request.form.get('phone')

    # 查询数据库中是否已有该用户
    user = UserModel.query.filter_by(phone=phone).first()

    if user:
        # 如果用户已存在且query_15为True，返回"已存在"
        if user.query_15:
            return jsonify({"message": "已存在"}), 400  # 已存在并且query_15为True
        else:
            # 如果用户存在且query_15为False，更新query_15为True
            user.query_15 = True
            db.session.commit()  # 提交更改

            # 返回所有query_15为True的用户信息
            users = UserModel.query.filter_by(query_15=True).all()

            result = []
            for u in users:
                result.append({
                    'name': u.name,
                    'phone': u.phone
                })

            return jsonify(result), 200  # 更新成功，返回所有query_15为True的用户信息
    else:
        # 如果用户不存在，返回失败信息
        return jsonify({'message': '用户不存在'}), 404

#15项清单查询权限人员的删除（返回所有query_15为True的姓名和号码）
@blue.route('/user/delete', methods=['POST'])
def delete_user():
    # 获取请求中的数据（姓名和手机号）
    name = request.form.get('name')
    phone = request.form.get('phone')

    # 查询数据库中是否已有该用户
    user = UserModel.query.filter_by(phone=phone).first()

    if user:
        # 如果用户存在，检查query_15是否为True
        if user.query_15:
            # 如果query_15为True，删除该用户
            db.session.delete(user)
            db.session.commit()  # 提交删除操作

            # 返回所有query_15为True的用户信息
            users = UserModel.query.filter_by(query_15=True).all()

            result = []
            for u in users:
                result.append({
                    'name': u.name,
                    'phone': u.phone
                })

            return jsonify(result), 200  # 删除成功，返回所有query_15为True的用户信息
        else:
            # 如果query_15为False，无法删除
            return jsonify({'message': '该用户无法删除，query_15为False'}), 400
    else:
        # 如果用户不存在，返回失败信息
        return jsonify({'message': '用户不存在'}), 404

#15项清单修改权限人员（返回所有alter_15为true的姓名和号码）
@blue.route('/user/alter_15', methods=['GET'])
def get_users_alter_15():
    # 查询所有alter_15为True的用户
    users = UserModel.query.filter_by(alter_15=True).all()

    # 格式化返回的结果
    result = []
    for user in users:
        result.append({
            'name': user.name,
            'phone': user.phone
        })

    return jsonify(result), 200  # 返回查询结果

#15项清单修改权限人员的添加（返回所有alter_15为true的姓名和号码）
@blue.route('/user/add', methods=['POST'])
def add_user():
    # 获取请求中的数据（姓名和手机号）
    name = request.form.get('name')
    phone = request.form.get('phone')

    # 查询数据库中是否已有该用户
    user = UserModel.query.filter_by(phone=phone).first()

    if user:
        # 如果用户已存在且alter_15为True，返回"已存在"
        if user.alter_15:
            return jsonify({"message": "已存在"}), 400  # 已存在并且alter_15为True
        else:
            # 如果用户存在且alter_15为False，更新alter_15为True
            user.alter_15 = True
            db.session.commit()  # 提交更改

            # 返回所有alter_15为True的用户信息
            users = UserModel.query.filter_by(alter_15=True).all()

            result = []
            for u in users:
                result.append({
                    'name': u.name,
                    'phone': u.phone
                })

            return jsonify(result), 200  # 更新成功，返回所有alter_15为True的用户信息
    else:
        # 如果用户不存在，返回失败信息
        return jsonify({'message': '用户不存在'}), 404

#15项清单修改权限人员的删除（返回所有alter_15为true的姓名和号码）
@blue.route('/user/delete', methods=['POST'])
def delete_user():
    # 获取请求中的数据（姓名和手机号）
    name = request.form.get('name')
    phone = request.form.get('phone')

    # 查询数据库中是否已有该用户
    user = UserModel.query.filter_by(phone=phone).first()

    if user:
        # 如果用户存在，检查alter_15是否为True
        if user.alter_15:
            # 如果alter_15为True，删除该用户
            db.session.delete(user)
            db.session.commit()  # 提交删除操作

            # 返回所有alter_15为True的用户信息
            users = UserModel.query.filter_by(alter_15=True).all()

            result = []
            for u in users:
                result.append({
                    'name': u.name,
                    'phone': u.phone
                })

            return jsonify(result), 200  # 删除成功，返回所有alter_15为True的用户信息
        else:
            # 如果alter_15为False，无法删除
            return jsonify({'message': '该用户无法删除，alter_15为False'}), 400
    else:
        # 如果用户不存在，返回失败信息
        return jsonify({'message': '用户不存在'}), 404

#政策文件修改权限人员（返回所有alter_zc为true的姓名和电话）
@blue.route('/user/alter_zc', methods=['GET'])
def get_users_alter_zc():
    # 查询所有alter_zc为True的用户
    users = UserModel.query.filter_by(alter_zc=True).all()

    # 格式化返回的结果
    result = []
    for user in users:
        result.append({
            'name': user.name,
            'phone': user.phone
        })

    return jsonify(result), 200  # 返回查询结果

#政策文件修改权限人员的添加（返回所有alter_zc为true的姓名和电话）
@blue.route('/user/add', methods=['POST'])
def add_user():
    # 获取请求中的数据（姓名和手机号）
    name = request.form.get('name')
    phone = request.form.get('phone')

    # 查询数据库中是否已有该用户
    user = UserModel.query.filter_by(phone=phone).first()

    if user:
        # 如果用户已存在且alter_zc为True，返回"已存在"
        if user.alter_zc:
            return jsonify({"message": "已存在"}), 400  # 已存在并且alter_zc为True
        else:
            # 如果用户存在且alter_zc为False，更新alter_zc为True
            user.alter_zc = True
            db.session.commit()  # 提交更改

            # 返回所有alter_zc为True的用户信息
            users = UserModel.query.filter_by(alter_zc=True).all()

            result = []
            for u in users:
                result.append({
                    'name': u.name,
                    'phone': u.phone
                })

            return jsonify(result), 200  # 更新成功，返回所有alter_zc为True的用户信息
    else:
        # 如果用户不存在，返回失败信息
        return jsonify({'message': '用户不存在'}), 404

#政策文件修改权限人员的删除（返回所有alter_zc为true的姓名和电话）
@blue.route('/user/delete', methods=['POST'])
def delete_user():
    # 获取请求中的数据（姓名和手机号）
    name = request.form.get('name')
    phone = request.form.get('phone')

    # 查询数据库中是否已有该用户
    user = UserModel.query.filter_by(phone=phone).first()

    if user:
        # 如果用户存在，检查alter_zc是否为True
        if user.alter_zc:
            # 如果alter_zc为True，删除该用户
            db.session.delete(user)
            db.session.commit()  # 提交删除操作

            # 返回所有alter_zc为True的用户信息
            users = UserModel.query.filter_by(alter_zc=True).all()

            result = []
            for u in users:
                result.append({
                    'name': u.name,
                    'phone': u.phone
                })

            return jsonify(result), 200  # 删除成功，返回所有alter_zc为True的用户信息
        else:
            # 如果alter_zc为False，无法删除
            return jsonify({'message': '该用户无法删除，alter_zc为False'}), 400
    else:
        # 如果用户不存在，返回失败信息
        return jsonify({'message': '用户不存在'}), 404

#典型案例修改权限人员（返回所有alter_model为true的姓名和电话）
@blue.route('/user/alter_model', methods=['GET'])
def get_users_alter_model():
    # 查询所有alter_model为True的用户
    users = UserModel.query.filter_by(alter_model=True).all()

    # 格式化返回的结果
    result = []
    for user in users:
        result.append({
            'name': user.name,
            'phone': user.phone
        })

    return jsonify(result), 200  # 返回查询结果


#典型案例修改权限人员的添加（返回所有alter_model为true的姓名和电话）
@blue.route('/user/add', methods=['POST'])
def add_user():
    # 获取请求中的数据（姓名和手机号）
    name = request.form.get('name')
    phone = request.form.get('phone')

    # 查询数据库中是否已有该用户
    user = UserModel.query.filter_by(phone=phone).first()

    if user:
        # 如果用户已存在且alter_model为True，返回"已存在"
        if user.alter_model:
            return jsonify({"message": "已存在"}), 400  # 已存在并且alter_model为True
        else:
            # 如果用户存在且alter_model为False，更新alter_model为True
            user.alter_model = True
            db.session.commit()  # 提交更改

            # 返回所有alter_model为True的用户信息
            users = UserModel.query.filter_by(alter_model=True).all()

            result = []
            for u in users:
                result.append({
                    'name': u.name,
                    'phone': u.phone
                })

            return jsonify(result), 200  # 更新成功，返回所有alter_model为True的用户信息
    else:
        # 如果用户不存在，返回失败信息
        return jsonify({'message': '用户不存在'}), 404

#典型案例修改权限人员的删除（返回所有alter_model为true的姓名和电话）
@blue.route('/user/delete', methods=['POST'])
def delete_user():
    # 获取请求中的数据（姓名和手机号）
    name = request.form.get('name')
    phone = request.form.get('phone')

    # 查询数据库中是否已有该用户
    user = UserModel.query.filter_by(phone=phone).first()

    if user:
        # 如果用户存在，检查alter_model是否为True
        if user.alter_model:
            # 如果alter_model为True，删除该用户
            db.session.delete(user)
            db.session.commit()  # 提交删除操作

            # 返回所有alter_model为True的用户信息
            users = UserModel.query.filter_by(alter_model=True).all()

            result = []
            for u in users:
                result.append({
                    'name': u.name,
                    'phone': u.phone
                })

            return jsonify(result), 200  # 删除成功，返回所有alter_model为True的用户信息
        else:
            # 如果alter_model为False，无法删除
            return jsonify({'message': '该用户无法删除，alter_model为False'}), 400
    else:
        # 如果用户不存在，返回失败信息
        return jsonify({'message': '用户不存在'}), 404