# 15projects表接口说明

本文件说明后端针对`15projects`表开放的API接口，包括：查询所有project_name、根据project_name查objectives、增加记录、修改记录。

---

## 1. 查询所有project_name
- **请求方式**：GET
- **请求路径**：/api/15projects/names
- **请求参数**：无
- **返回示例**：
```json
{
  "success": true,
  "data": ["项目A", "项目B", "项目C"]
}
```

---

## 2. 根据project_name查objectives
- **请求方式**：GET
- **请求路径**：/api/15projects/objectives
- **请求参数**：query参数 project_name（要查询的项目名）
- **返回示例**：
```json
{
  "success": true,
  "data": {"objectives": "主要任务目标内容"}
}
```
- **失败示例**：
```json
{
  "success": false,
  "message": "未找到该项目"
}
```

---

## 3. 增加记录
- **请求方式**：POST
- **请求路径**：/api/15projects
- **请求参数**（JSON格式，*为必填）：
  - serial_number*：项目序号
  - city*：项目所在地级市
  - county*：结对县(市、区)
  - universities*：组团结对高校院所
  - project_name*：项目名称
  - implementing_institutions*：项目实施单位
  - is_key_project*：是否重点项目（是/否）
  - project_type*：项目类型
  - start_date*：项目开始时间
  - end_date*：项目结束时间
  - 其他字段可选：background, content_and_measures, objectives, contacts, remarks, involved_areas
- **返回示例**：
```json
{
  "success": true,
  "message": "添加成功",
  "id": 1
}
```
- **失败示例**：
```json
{
  "success": false,
  "message": "缺少必要参数: project_name"
}
```

---

## 4. 修改记录
- **请求方式**：PUT
- **请求路径**：/api/15projects/<project_id>
- **请求参数**：路径参数 project_id，body为要修改的字段及新值（JSON）
- **返回示例**：
```json
{
  "success": true,
  "message": "修改成功"
}
```
- **失败示例**：
```json
{
  "success": false,
  "message": "未找到该项目"
}
```

---

## 说明与注意事项
- 所有接口返回JSON格式。
- 新增和修改接口均有参数校验，缺失参数或类型错误会返回失败信息。
- 仅支持修改前端传递的字段。