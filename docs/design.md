# 简介
此系统为运维管理平台，以flask+mysql为基础框架开发的。


# 设计思路
以CMDB为基础，运用流行的管理工具Ansible支撑整个运维平台。


# 导航图

```
|-- 主页    ----完成
|
|-- CMDB    ---- 完成
|   |
|   |-- 服务器管理
|   |
|   |-- IDC管理
|   |
|   |-- 软件管理
|   |
|   |-- 服务器导入
|
|-- 项目管理    ---- 完成
|   |
|   |-- 项目管理
|   |
|   |-- 模块管理
|   |
|   |-- 环境管理
|
|-- 配置管理    ---- 未开始
|   |
|   |-- 配置列表
|   |
|   |-- 配置创建
|
|-- 发布管理    ---- 转移到deploy仓库
|   |
|   |-- 模块打包
|   |
|   |-- 模块发布
|   |
|   |-- 发布历史
|
|-- ansible管理    ---- 转移到deploy仓库
|   |
|   |-- anslbie执行
|   |
|   |-- playbook执行
|
|-- wiki    ---- 完成
|   |
|   |-- index
|   |
|   |-- server-info
|   |
|   |-- nginx-proxy
|
|-- 脚本库    ---- 未开始
|
|-- 日志管理    ---- 未开始
```