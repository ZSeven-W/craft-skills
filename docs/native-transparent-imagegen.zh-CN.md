# Native Transparent ImageGen Skill 中文使用指南

[English](native-transparent-imagegen.md) | [简体中文](native-transparent-imagegen.zh-CN.md)

[返回 Craft Skills 集合](../README.md)

这是一个实验性的 Codex Skill，用于**直接生成**带原生 Alpha 的透明 PNG/WebP，并在
交付前检查未经修改的原文件。它不负责把已有不透明图片抠成透明，也不会用棋盘格、
色键或本地写入 Alpha 冒充模型直出。

## 为什么不是一条 Prompt

“透明背景”是生成意图，不是验收证据。当前黑盒生图入口可能返回真正 RGBA，也可能
返回画进 RGB 图片里的棋盘格。这个 Skill 把可复用价值放在工作流：逐张生成、读取
原始文件、有限重试、视觉边缘检查、失败即停。

## 什么时候使用

用于新生成的透明贴纸、Sprite、角色立绘、商品素材、UI 装饰，以及毛发、头发、玻璃、
烟雾等细边缘对象。不要用于：

- 给现有照片或插画去背景；
- 普通不透明生图；
- 用户明确接受色键或后处理的流水线；
- 仅审核一张图是否好看而不要求透明交付。

## 安装

```sh
git clone https://github.com/ZSeven-W/craft-skills.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R craft-skills/skills/native-transparent-imagegen \
  "${CODEX_HOME:-$HOME/.codex}/skills/"

python3 -m pip install -r \
  "${CODEX_HOME:-$HOME/.codex}/skills/native-transparent-imagegen/scripts/requirements.txt"
```

## 调用示例

```text
使用 $native-transparent-imagegen，参考附件中我有权使用的角色设定，生成一张透明
PNG 贴纸。必须是模型原生 Alpha，不允许抠图、色键、分割或绘制棋盘格。逐张生成并
验证未经修改的原文件；如果三次仍不是 RGBA，就报告失败。
```

## 验收

```sh
python3 \
  "${CODEX_HOME:-$HOME/.codex}/skills/native-transparent-imagegen/scripts/validate_alpha.py" \
  --require-transparent-corners \
  /path/to/original-output.png
```

脚本只读，不会修改图片。它检查格式、尺寸、SHA-256、Alpha 通道、Alpha 极值、完全
透明像素数量和四角像素。缺少 Alpha、整图完全透明、没有任何完全透明像素，或规定
四角透明却不透明，都会失败。

元数据通过后仍要在明暗对比背景下检查毛发、雾、玻璃和阴影。宽范围半透明色雾、
白边、黑边、假棋盘格、裁切毛尖或错误角色，都不能因为“有 Alpha”而通过。

## 团子与胡桃第一版案例

[案例记录](../examples/native-transparent-imagegen-tuanzi-hutao.md)使用 Fini Yang 直接提供、
有水印的第一版角色动作页作为本地身份与画材参考。原角色图与生成原图不进入 Apache
代码许可；公开包只保留可审计的测试记录、哈希和结果边界。

三次原生生成中，一次返回 RGBA，另外两次返回 RGB 棋盘格。RGBA 文件通过技术 Alpha
检查，但存在宽范围低 Alpha 氛围晕染，因此记录为“技术通过、英雄案例视觉未通过”。
这正是该 Skill 不把元数据通过等同于干净毛发边缘的原因。

## 维护边界

当宿主工具稳定暴露透明输出并修复批量行为时，逐张执行与重试规则可以简化。原文件
Alpha 验证、细边缘视觉 QA、无后处理证明和状态分离仍然适用于生产素材。
