# Personal CI库

个人使用，说明书非常简略，有问题可以开issue问，**请勿选择Action标签**

目前已有2模块：BT下载、Pixiv

## BT下载功能说明

目前已有功能如下：

- [BT输入式下载](https://github.com/Rcrwrate/CI/blob/main/.github/workflows/BT.yml)
- [BT RSS订阅下载，常规用于下载新番](https://github.com/Rcrwrate/CI/blob/main/.github/workflows/BtRSS.yml)


## PIXIV相关功能说明

目前已有功能如下：

- [CI定时拉取个人收藏，上传](https://github.com/Rcrwrate/CI/blob/main/.github/workflows/Aria2.yml)
- [CI根据带有Action label的issue中的数据定时拉取对应用户作品](https://github.com/Rcrwrate/CI/blob/main/.github/workflows/issue.yml)
- [手动下载某收藏夹tag内容](https://github.com/Rcrwrate/CI/blob/main/.github/workflows/input.yml)

#### 模块设计说明：

1. 图片Url获取，仅获取未分类的图片，**获取后会自动加上saved的标签**，文件输出为`image\urllist.txt`

2. aria2下载图片，在下载完全部图片后，存储于`image`内

3. 上传图片

#### 上传服务

位于`Upload`中，目前仅提供上传Onedrive的途径(通过Graph API),可以通过rclone，需要自行上传rclone.conf和修改yml

### 使用说明

1. 在仓库设置中新建COOKIE的secret，其值为你Pixiv的账号凭证，打开[https://www.pixiv.net](https://www.pixiv.net)，按下F12在应用程序>Cookie找到名为PHPSESSID的值，就是它

2. 在仓库设置中新建UID的secret，其值为你Pixiv账号的UID

接下来进行加密的配置

3. 运行`python C_normal.py --mode create`，创建密钥对，(默认4096位)，请妥善保管

https://github.com/Rcrwrate/CI/blob/main/CRY/CRY_RSA.py#LL103C24-L103C24

如要修改，请在如上位置修改

4. 在仓库设置中新建PUBLIC和PRIVATE的secret，其值为public.pem和private.pem中的内容

接下来进行上传器Onedrive的配置，不提供APP的申请教程

在Upload中，会对oa.json和setting.py进行加密和解密，我们将要配置的也是这两个文件

5. oa.json，如下所示

`{"client_id": "*-*-*-*-*", "client_secret": "*-*~*.*.*"}`

6. setting.py可以使用`oa.py`中的`OA.default()`进行一键填写，注意修改L8的code

7. 加密全部机密`python C_normal.py --mode jiami`

温习提示`python C_normal.py --mode jiemi`解密全部机密

### 作为CLI使用

`python run.py -h`获取并下载(单线程)

`python aria.py -h`获取并生成urllist.txt文件
