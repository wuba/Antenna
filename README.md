# Antenna

## 免责声明

1. 本工具仅面向 合法授权 的企业安全建设行为与个人学习行为，如您需要测试本工具的可用性，请自行搭建靶机环境。
2. 如您在使用本工具的过程中存在任何非法行为，您需自行承担相应后果，我们将不承担任何法律及连带责任。
   在安装并使用本工具前，请您 务必审慎阅读、充分理解各条款内容限制、免责条款或者其他涉及您重大权益的条款可能会以
   加粗、加下划线等形式提示您重点注意。
   除非您已充分阅读、完全理解并接受本协议所有条款，否则，请您不要安装并使用本工具。您的使用行为或者您以其他任何明示或者默示方式表示接受本协议的，即视为您已阅读并同意本协议的约束。

## Antenna简介

Antenna是58同城安全团队打造的一款辅助安全从业人员辅助验证网络中多种漏洞是否存在以及可利用性的工具。其基于带外应用安全测试(
OAST)通过任务的形式，将不同漏洞场景检测能力通过插件的形式进行集合，通过与目标进行Out-of-bind的数据通信方式进行辅助检测。

## Antenna的目标

我们绝不仅仅只是将Antenna做成一款只能监听DNS、HTTP等协议来简单判断无回显类型漏洞的工具，我们的目标是尝试在良好使用体验的基础上支持高度灵活的自定义组件能力，满足用户通过Antenna探索并实现各种应用安全漏洞场景的辅助检测。尽可能得实现通过Antenna这款产品降低各种安全漏洞场景的检测成本。

## 相关网站

博客(已开放)：[Antenna 博客](http://blog.antenna.cool/docs/intro)

演示平台(暂时关闭)：[演示平台](http://jiemuzu.cn)

漏洞靶场(已支持docker部署,docker-compose文件在项目docker目录中)：[lcttty/antenna-range:0.0.1](https://github.com/wuba/Antenna/blob/main/docker/docker-compose-range.yaml)

## Antenna_Inside计划

在我们开发Antenna时，就希望能够支持现有市场上流行的漏洞扫描工具漏洞结果回调与主动查询
,所以我们推出了CallBack与OpenAPI。为了让我们的这两个模块能够更加灵活与优雅。我们决定发起
Antenna_Inside计划，如果您是使用扫描工具的用户或者作者请联系我们，我们会无条件支持您的项目与
需求，帮助Antenna更方便的与漏洞扫描流程打通。如果您有推荐打通的项目，也可以在issue中提出来

已加入Antenna_Inside项目与进度

| 项目名称       | 项目地址                                                                       | 项目进度 |
|------------|----------------------------------------------------------------------------|------|
| EasyPen    | [https://github.com/lijiejie/EasyPen](https://github.com/lijiejie/EasyPen) | 正在对接 |


## 近期使用疑问解答

#### 1、关于docker部署发现平台配置保存后不能及时更新的问题

回答：更新完配置需在宿主机重新运行命令 **docker-compose restart** 后配置才能更新
不需要重启mysql容器

#### 2、关于各类组件的使用说明以及能否再详细的进行说明自定义组件开发教程

回答：文章将在Antenna博客不定时更新，基础文章已有，后续详细的也会有的，作者在加班加点的写，绝不会让各位师傅等太久

#### 3、运行docker-compose命令后镜像构建时间过长

回答：可能是您的服务器在境外，可将Dockerfile中替换镜像源的命令注释掉

#### 4、镜像部署总是遇到各种权限不允许的错误

回答：可将docker下列内容删除

```dockerfile
RUN addgroup --system antenna \
    && adduser --system --ingroup antenna antenna

USER antenna
```

#### 5、其他问题

如果您遇到了其他问题可查阅项目issue进行寻找相关解决方案，如果发现并没有其他人遇到和您相关的问题，请新建issue，
作者会及时回答您的疑问


## 相关教程链接
### 最新公告

v1.0版本发布公告及使用要点:[Antenna V1.0 发布公告](http://blog.antenna.cool/blog/v1.0)

### 关于部署
基础部署教程:[安装部署](http://blog.antenna.cool/docs/intro)

隐匿部署教程：[关于Antenna的隐匿性部署](http://blog.antenna.cool/blog/%20%20Secrecy)

前后端分离部署 [Antenna的前后端分离部署](http://blog.antenna.cool/blog/client_server)

### 关于配置

基础配置教程:[基础配置教程](http://blog.antenna.cool/docs/%E5%85%B3%E4%BA%8E%E9%85%8D%E7%BD%AE/config)

域名配置及DNS相关配置:[域名配置及阿里云dns服务修改教程](http://blog.antenna.cool/docs/%E5%85%B3%E4%BA%8E%E9%85%8D%E7%BD%AE/DNS)

开通邮箱通知以及邮箱授权码申请教程:[QQ邮箱授权码申请教程](https://service.mail.qq.com/cgi-bin/help?subtype=1&id=28&no=1001256)

### 关于任务

任务基础使用教程:[如何简单的使用任务](http://blog.antenna.cool/docs/%E5%85%B3%E4%BA%8E%E4%BB%BB%E5%8A%A1/task)

### 关于组件

组件基础使用教程:[Antenna的灵魂-组件Template](http://blog.antenna.cool/docs/%E5%85%B3%E4%BA%8E%E7%BB%84%E4%BB%B6/template)

xss 组件使用教程:[xss组件使用教程](http://blog.antenna.cool/docs/%E5%85%B3%E4%BA%8E%E7%BB%84%E4%BB%B6/xss)

组件开发教程:[如何编写Antenna组件](http://blog.antenna.cool/docs/%E5%85%B3%E4%BA%8E%E7%BB%84%E4%BB%B6/template_demo)

### 关于OPEN_API与CallBack


## 404星链计划

![](https://github.com/knownsec/404StarLink-Project/raw/master/logo.png)

ANTENNA 项目 现已加入 [404星链计划](https://github.com/knownsec/404StarLink)


## Stargazers over time

[![Stargazers over time](https://starchart.cc/wuba/Antenna.svg)](https://starchart.cc/wuba/Antenna)

##  联系我们

如果对Antenna有任何建设性意见或 BUG 反馈，欢迎大家提 issue,进交流群 作者也会线下约饭进行奖励🐶

如有问题想与技术同学沟通，请联系并添加微信号：bios_000

Antenna用户交流群：

![img_11.png](imgs/img_11.png)

