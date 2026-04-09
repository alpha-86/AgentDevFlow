# Codex 接入

## 建议接入方式

- 使用 `plugins/agentdevpipeline/` 作为 Codex 本地插件
- 插件内只放入口与说明，核心内容仍引用仓库中的共享文档

## 最小安装

1. 将 `plugins/agentdevpipeline/` 放入 Codex 可见插件目录
2. 按平台要求注册插件
3. 让角色初始化时优先阅读 `prompts/zh-cn/` 和 `skills/shared/`

## 说明

- Codex 适配层不复制全部 prompt，而是把仓库作为内容根
- 如后续需要，可再补 hooks、scripts、marketplace 元数据

