
# 📘 UserModel 接口文档

该文档整理了所有以 `/user/` 开头的接口，涵盖用户注册、权限管理、验证、查询等功能。

---

## 📌 1. 用户注册接口

- **接口路径**：`POST /user/register`
- **请求参数**（`application/x-www-form-urlencoded`）：

| 参数名      | 类型   | 是否必填 | 说明           |
|-------------|--------|----------|----------------|
| name        | string | 是       | 姓名           |
| phone       | string | 是       | 手机号         |
| password    | string | 是       | 密码（明文）   |
| wx_openid   | string | 是       | 微信 openid    |

- **成功返回**（用户已存在且匹配）：
```json
{
  "name": "张三",
  "phone": "12345678901",
  "wx_openid": "xxx",
  "password": "123456"
}
```

- **失败返回**：

| 状态码 | 返回内容 |
|--------|----------|
| 400    | 用户信息不匹配 |
| 404    | 用户不存在     |

---

## 📌 2. 用户验证（用于身份转让）

- **接口路径**：`POST /user/validate`
- **请求参数**：

| 参数名   | 类型   | 是否必填 | 说明         |
|----------|--------|----------|--------------|
| name     | string | 是       | 姓名         |
| phone    | string | 是       | 手机号       |
| password | string | 是       | 明文密码     |

- **逻辑说明**：
  - 用户存在、信息匹配、并且 `principal=True` 才视为验证通过。

- **成功返回**：
```json
{
  "name": "张三",
  "phone": "12345678901",
  "wx_openid": "xxx",
  "principal": true
}
```

- **失败情况**：

| 状态码 | message                        |
|--------|--------------------------------|
| 400    | 姓名或密码错误                 |
| 403    | 该用户不是负责人，无法转让     |
| 404    | 用户不存在                     |

---

## 📌 3. 查询拥有 15项清单【查询权限】的用户

- **接口路径**：`GET /user/query_15`
- **返回**：
```json
[
  {"name": "张三", "phone": "12345678901"},
  ...
]
```

---

## 📌 4. 添加 15项清单【查询权限】

- **接口路径**：`POST /user/query_15_add`
- **参数**：`name`, `phone`
- **成功返回**：所有 `query_15=True` 的用户信息

---

## 📌 5. 删除 15项清单【查询权限】

- **接口路径**：`POST /user/query_15_delete`
- **参数**：`name`, `phone`
- **成功返回**：所有 `query_15=True` 的用户信息
- **失败情况**：
  - 用户无权限（`query_15=False`）
  - 用户不存在

---

## 📌 6~9. 权限控制接口列表

| 权限名称       | 查询路径            | 添加路径               | 删除路径                 |
|----------------|---------------------|--------------------------|--------------------------|
| 15项清单修改权限 | `/user/alter_15`     | `/user/alter_15_add`     | `/user/alter_15_delete`  |
| 政策文件修改权限 | `/user/alter_zc`     | `/user/alter_zc_add`     | `/user/alter_zc_delete`  |
| 典型案例修改权限 | `/user/alter_model`  | `/user/alter_model_add`  | `/user/alter_model_delete` |
| 进度信息修改权限 | `/user/alter_progress` | `/user/alter_progress_add` | `/user/alter_progress_delete` |

---

## 📝 参数说明统一（适用于所有添加/删除权限接口）

- 请求参数格式：`application/x-www-form-urlencoded`
- 请求参数：

| 参数名 | 类型   | 是否必填 | 说明     |
|--------|--------|----------|----------|
| name   | string | 是       | 姓名     |
| phone  | string | 是       | 手机号   |

---

## ✅ 字段说明（UserModel）

| 字段名           | 类型     | 说明                         |
|------------------|----------|------------------------------|
| name             | string   | 姓名                         |
| phone            | string   | 手机号                       |
| password         | string   | 密码（明文，建议加密）       |
| wx_openid        | string   | 微信openid                   |
| principal        | boolean  | 是否负责人（用于转让验证）   |
| query_15         | boolean  | 是否有 15项清单查询权限      |
| alter_15         | boolean  | 是否有 15项清单修改权限      |
| alter_zc         | boolean  | 是否有政策文件修改权限       |
| alter_model      | boolean  | 是否有典型案例修改权限       |
| alter_progress   | boolean  | 是否有进度信息修改权限       |
