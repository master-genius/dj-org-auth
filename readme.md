## 组织用户验证
这仅仅是一个探索方案，实现思路是独立于Django的用户认证，实现一个独立的认证过程用于组织用户，然后和Django自带的用户认证进行关联。

代码在orgauth目录，使用中间件检测是否存在session文件，存在则读取并设置orguser，orguser采用字典类型存储，并转换成json格式存储到对应文件，session文件存储路径是/tmp/，存储格式是sess_字符串加上生成的[CookieID]。

组织用户登录后可以通过输入平台账户的用户名和密码进行绑定，一个平台账户只能绑定一个组织内的账户，但是可以绑定多个组织。从安全角度考虑，需要更合理的绑定方式，比如先要平台账户发起一个验证申请，目前还没有想到既操作方便实现也比较简单的方式。

平台账户登录后会把已经关联的组织信息放到session中，通过request.session[‘orgbind’]获取。

组织账户使用一个配置表用于管理权限，角色对应一个列表表示具备的权限，这属于默认的权限，有一个数据表用于动态设置，暂时没有实现，组织账户访问接口会通过登录与权限的检测，如果是平台账户则会查看是否具备绑定关系并且是否具备权限。



**问题**

session文件没有加入过期检测，如果方案可行，需要规划并重新组织代码结构。