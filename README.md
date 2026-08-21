# Craft Skills

[简体中文](README.md) | [English](README.en.md)

面向 AI Agent 的研究驱动、评测驱动型 Skill 集合。

Craft Skills 把可迁移的专业方法提炼成聚焦的工作流，并为每个 Skill
明确触发边界、退出条件、原创案例与前向测试。它不是视频摘要库、提示词合集，
也不是模仿创作者风格的素材仓库。

由 [Fini Yang](https://github.com/finiking) 创建并策划，
[ZSeven](https://github.com/ZSeven-W) 维护。

## Skills

| Skill | 用途 | 状态 |
|---|---|---|
| [`logo-semantic-fusion`](skills/logo-semantic-fusion/README.md) | 设计和评审让多个含义真正共享几何结构的 Logo。 [阅读中文使用指南并查看案例](docs/logo-semantic-fusion.zh-CN.md) · [Agent 工作流](skills/logo-semantic-fusion/SKILL.md) | v0.1 实验版 |
| [`recurring-character-diary-comic`](skills/recurring-character-diary-comic/README.md) | 围绕已有且获授权的固定角色，创建、审核或局部修复 4–8 格日记漫画；锁定故事与视觉合同，按风险选择生成路线，可审计合成，并检查实际成品。 [阅读中文使用指南](docs/recurring-character-diary-comic.zh-CN.md) · [Agent 工作流](skills/recurring-character-diary-comic/SKILL.md) | v0.1 实验版 |
| [`native-transparent-imagegen`](skills/native-transparent-imagegen/README.md) | 原生生成透明 PNG/WebP，检查未经修改的 Alpha、细边缘和证据；RGB 棋盘格直接失败，禁止用抠图伪造成功。 [阅读中文使用指南与团子胡桃案例](docs/native-transparent-imagegen.zh-CN.md) · [Agent 工作流](skills/native-transparent-imagegen/SKILL.md) | v0.1 实验版 |

## 原生透明，不是把棋盘格画进图片

`native-transparent-imagegen` 解决的不是“怎样写一句透明背景 Prompt”，而是怎样证明
交付文件真的包含模型原生 Alpha：

- 新素材逐张生成，保留模型返回的原始字节；
- PNG/WebP 必须存在 Alpha、完全透明像素与符合要求的透明四角；
- RGB 棋盘格直接失败，最多有限重试；
- 禁止用抠图、色键、分割或本地写入 Alpha 冒充成功；
- 元数据通过后，仍要在明暗背景下检查毛发、玻璃、烟雾和半透明晕染。

[团子与胡桃第一版毛发案例](examples/native-transparent-imagegen-tuanzi-hutao.md)
使用权利人直接提供的角色动作页作为本地身份参考。三次原生生成中，一次返回 RGBA，
两次返回画着棋盘格的 RGB；唯一 RGBA 又因宽范围低 Alpha 晕染没有通过英雄案例视觉门。
因此公开结论不是“某句 Prompt 包成功”，而是：**能验，才算真的能用。**

```text
使用 $native-transparent-imagegen 生成透明 PNG。必须是模型原生 Alpha；
逐张验证未经修改的原文件，失败就报告，不允许抠图补救。
```

[![原创 Handoff 语义共形概念家族](assets/examples/handoff/handoff-concept-sheet.png)](docs/logo-semantic-fusion.zh-CN.md)

[![原创固定角色日记漫画不规则分镜案例](assets/examples/recurring-character-diary-comic/recurring-character-diary-comic-cover.png)](docs/recurring-character-diary-comic.zh-CN.md)

“实验版”表示这套工作流具备结构化测试和原创案例，不代表它已经达到生产就绪、
完成商标法律核查或获得专业人士批准。

## 安装

克隆仓库，然后只复制需要的 Skill：

```sh
git clone https://github.com/ZSeven-W/craft-skills.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R craft-skills/skills/logo-semantic-fusion \
  "${CODEX_HOME:-$HOME/.codex}/skills/"

# 或安装固定角色日记漫画 Skill：
cp -R craft-skills/skills/recurring-character-diary-comic \
  "${CODEX_HOME:-$HOME/.codex}/skills/"

# 或安装原生透明生图 Skill：
cp -R craft-skills/skills/native-transparent-imagegen \
  "${CODEX_HOME:-$HOME/.codex}/skills/"
```

如果安装后没有立即发现 Skill，请重启或重新加载 Agent 会话。

## 发布标准

每个公开 Skill 都必须：

- 解决一个范围明确、可复用的用户目标；
- 同时定义触发与不触发边界；
- 包含适用性判断、退出路径和证据规则；
- 只使用原创案例或许可明确的素材；
- 在评测中覆盖正常、信息不全、不应触发及边缘情况；
- 在未见过的任务上证明增益，而不只适配仓库内置案例；
- 区分已经检查的实际产物、提示词与预期输出；
- 通过仓库的确定性发布检查；
- 说明重要限制，不作缺乏依据的专业或法律承诺。

## 来源与媒体边界

公开教育内容可以为 Skill 的方法研究提供线索。对方法有重要影响的来源会在对应
Skill 的溯源说明或第三方声明中提供链接。署名只记录研究背景，不表示来源作者
认可或背书本项目。

本仓库不包含下载的视频、音频、封面、截图、字幕或转录文本、平台元数据或第三方
品牌素材。公开案例必须为原创内容或具有明确许可。研究档案和采集工具始终位于本
仓库及其发布历史之外。

## 参与贡献

欢迎提交缺陷修复、更清晰的说明、额外评测和原创测试案例。提出新 Skill 前请先
阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

请勿提交自动化来源转换、近似逐字摘要、创作者风格克隆、抓取媒体、通用提示词
合集，或把未经产物验证的结果描述成已经通过检查的内容。

## 验证

使用 Python 3.10 或更高版本。先安装验证依赖，再在仓库根目录运行确定性发布
检查：

```sh
python3 -m pip install -r \
  evals/recurring-character-diary-comic/requirements.txt
python3 scripts/check_release.py
```

根检查器除了验证包结构、链接、元数据、媒体和发布卫生，还会执行集合中各 Skill
自带的 eval validator。

## 许可证

仓库原创内容采用 [Apache License 2.0](LICENSE) 许可。链接内容和第三方内容
仍由各自权利方持有；详见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
