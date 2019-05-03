# MxOnline

**仿mooc网在线教育平台**：xadmin第三方后台管理系统搭建在线教育平台，基于<code>Python3.x</code>，<code>Django2.x</code>和<code>xadmin</code>


- 系统具有完整的用户登录注册以及找回密码功能，拥有完整个人中心。
- 个人中心: 修改头像，修改密码，修改邮箱，可以看到我的课程以及我的收藏。可以删除收藏，我的消息。
- 导航栏: 公开课，授课讲师，授课机构，全局搜索。
- 点击公开课–> 课程列表，排序-搜索。热门课程推荐，课程的分页。
- 点击课程–> 课程详情页中对课程进行收藏，取消收藏。富文本展示课程内容。
- 点击开始学习–> 课程的章节信息，课程的评论信息。课程资源的下载链接。
- 点击授课讲师–>授课讲师列表页，对讲师进行人气排序以及分页，右边有讲师排行榜。
- 点击讲师的详情页面–> 对讲师进行收藏和分享，以及讲师的全部课程。
- 导航栏: 授课机构有分页，排序筛选功能。
- 机构列表页右侧有快速提交我要学习的表单。
- 点击机构–> 左侧：机构首页,机构课程，机构介绍，机构讲师。
- 后台管理系统可以切换主题。左侧每一个功能都有列表显示, 增删改查，筛选功能。
- 课程列表页可以对不同字段进行排序。选择多条记录进行删除操作。
- 课程列表页：过滤器->选择字段范围等,搜索,导出csv，xml，json。
- 课程新增页面上传图片，富文本的编辑。时间选择，添加章节，添加课程资源。
- 日志记录：记录后台人员的操作


**首页**
![index](https://github.com/weilanhanf/Photos/blob/master/MxOnline/index.png?raw=true)


**课程详情页**
![course_info](https://github.com/weilanhanf/Photos/blob/master/MxOnline/course_info.png?raw=true)


**课程列表页**
![course_list](https://github.com/weilanhanf/Photos/blob/master/MxOnline/course_list.png?raw=true)


**登录页**
![login](https://github.com/weilanhanf/Photos/blob/master/MxOnline/login.png?raw=true)


**后台管理首页**
![manage](https://github.com/weilanhanf/Photos/blob/master/MxOnline/manage.png?raw=true)


**后台管理详情**
![manage_info](https://github.com/weilanhanf/Photos/blob/master/MxOnline/manage_info.png?raw=true)


**机构列表页**
![organ_list](https://github.com/weilanhanf/Photos/blob/master/MxOnline/organ_list.png?raw=true)


**教师首页**
![teacher_index](https://github.com/weilanhanf/Photos/blob/master/MxOnline/teacher_index.png?raw=true)


**用户中心**
![user_center](https://github.com/weilanhanf/Photos/blob/master/MxOnline/user_center.png?raw=true)



## 安装

### 依赖包安装

下载文件进入项目目录之后，使用pip安装依赖包

<code>pip install -Ur requirements.txt</code>

### 数据库配置

修改wxcrm/setting.py 修改数据库配置，如下所示：

```
 DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mxonline',
        'USER': 'root', 
        'PASSWORD': 'password',
        'HOST': 'host',
        'PORT': 3306,
    }
}
```

### 创建数据库

mysql数据库中执行:

<code>CREATE DATABASE 'mxonline'</code>

迁移数据库，终端下执行:

```
./python manage.py makemigrations
./python manage.py migrate
```

### 创建超级用户

终端下执行:

<code>./python manage.py createsuperuser</code>

然后输入相应的超级用户名以及密码，邮箱即可。

### 开始运行

终端下执行:

<code>./python manage.py runserver</code>
 
浏览器打开: <code>http://127.0.0.1</code> 即可进入普通用户入口

浏览器打开: <code>http://127.0.0.1/xadmin</code> 即可进入超级用户入口
  
## 感谢

感谢您的star和fork
