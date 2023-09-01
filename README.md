# AuthService

## 目录
- [基本介绍](#基本介绍)
- [安装](#安装)
- [启动](#启动)
- [执行测试用例](#执行测试用例)
- [API](#api)
- [第三方包](#第三方包)

## 基本介绍
AuthService是一个基于Django搭建的简单后台API服务，其提供了基本的用户创建以及鉴权功能，同时提供了角色创建和绑定用户的功能

## 安装

### 将仓库代码clone到本地
```shell
git clone https://github.com/sindwerra/authService.git
```

### 执行pip命令安装依赖包
```shell
pip install -r requirements.txt
```

## 执行测试用例
在真正启动服务前，可以先通过Django提供的test方法执行测试用例
```shell
python manage.py test --pattern="*_test.py" 
```

## API
请注意，API接口的所有路径前缀都带有api/
### 创建新用户  
创建新用户，如果指定的username已经存在，则创建失败，返回400状态码并给出创建失败提示

POST user/add/

示例请求  
username: 新增用户的用户名，必须与现有的用户用户名不同  
password: 新增用户的密码
```json
{
  "username": "sindwerra",
  "password": "102102102a"
}
```

示例响应（创建成功）
```json
"User Creation Success!"
```

### 删除用户
删除用户，如果指定的用户username不存在，则删除失败，返回400状态码并给出删除失败提示

DELETE user/delete/  

示例请求  
username: 需要删除的用户的用户名
```json
{
  "username": "sindwerra"
}
```

示例响应（删除成功）
```json
"User Already Deleted."
```

### 用户登录
用户登录，登录成功会返回一个过期时间为2h（默认配置，可以通过修改settings.py中的TOKEN_EXPIRATION_DURATION_HOUR来修改过期时间）令牌，
该令牌用于访问[获取当前用户绑定角色](#使用token获取当前用户绑定的所有角色)和[检查角色是否与当前用户绑定](#使用token获取当前用户是否和指定角色绑定)两个需要鉴权的API接口

POST authenticate/

示例请求  
username: 用户名  
password: 密码
```json
{
  "username": "sindwerra",
  "password": "102102102a"
}
```

示例响应（登录成功）
```json
"This is an example token."
```

### 用户Token失效
用户Token失效，会将当前生效的Token直接失效，如果Token不存在，则返回400状态码并给出提示

POST invalidate/  

示例请求  
token: 用户身份识别令牌
```json
{
  "token": "example-token"
}
```

示例响应（失效成功）
```json
"Token invalidated"
```


### 新增角色
新增角色，如果角色已存在，则返回400状态码并给出提示

POST role/add/  
  
示例请求  
role: 需要增加的角色的角色名称，必须与现有角色名不同
```json
{
  "role": "demon hunter"
}
```

示例响应（创建成功）
```json
"Role Creation Success!"
```
### 删除角色
删除指定的角色，如果该角色不存在，则返回400状态码并给出提示

DELETE role/delete  

示例请求  
role: 需要删除的角色的角色名
```json
{
  "role": "demon hunter"
}
```

示例响应（删除成功）
```json
"Role Already Deleted."
```

### 绑定用户与角色
绑定指定用户和角色，如果用户或者角色不存在，则返回400状态码并给出提示

POST role/assign/  
  
示例请求  
role: 需要绑定的角色名称   
user: 需要绑定的用户的用户名
```json
{
  "role": "witch",
  "user": "sindwerra"
}
```

示例响应（绑定成功）
```json
"Binding Success"
```

### 使用Token获取当前用户绑定的所有角色
使用Token获取对应用户绑定角色的列表，如果Token不存在或者失效，则返回400状态码并给出提示

GET role/list/  
  
示例请求  
token: 用户身份识别令牌
```json
{
  "token": "example-token"
}
```

示例响应（获取成功）
```json
[
  "role_a", 
  "role_b",
  "role_c"
]
```

### 使用Token获取当前用户是否和指定角色绑定
使用Token获取当前用户是否和指定角色绑定，如果Token不存在或失效，或者角色不存在，则返回400状态码并给出提示

POST role/check/  
  
示例请求  
token: 用户身份识别令牌  
role: 需要检查是否绑定用户的角色
```json
{
  "token": "example-token",
  "role": "witch"
}
```

示例响应（用户与角色已绑定）
```json
"True"
```


## 启动
有两种方式启动AuthService服务
### PyCharm启动
### 控制台命令行启动
```shell
python manage.py runserver
```

## 第三方包
1. Django （服务端框架）
2. PyJWT（成熟的Python Token使用方案）
3. django-rest-framework（基于Django的成熟的API框架工具）