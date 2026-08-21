# Native Transparent ImageGen Skill Guide

[English](native-transparent-imagegen.md) | [简体中文](native-transparent-imagegen.zh-CN.md)

[Back to Craft Skills](../README.en.md)

This experimental Codex skill generates new PNG or WebP assets with native alpha and validates
the untouched original before delivery. It does not remove backgrounds from existing opaque
images and never uses a checkerboard, chroma key, segmentation, or locally written alpha to
pretend native generation succeeded.

## Why this is not a prompt

"Transparent background" expresses intent; it is not acceptance evidence. A black-box image
tool can return genuine RGBA or an RGB image containing a drawn checkerboard. The reusable
workflow is serialized generation, original-file inspection, bounded retry, visual edge QA,
and fail-closed reporting.

## Use it for

Use the skill for newly generated transparent stickers, sprites, character art, product assets,
UI decorations, and fine-edged subjects such as fur, hair, glass, or smoke. Do not use it for
background removal, ordinary opaque generation, an explicitly accepted chroma-key pipeline,
or general image critique without a transparent deliverable.

## Install

```sh
git clone https://github.com/ZSeven-W/craft-skills.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R craft-skills/skills/native-transparent-imagegen \
  "${CODEX_HOME:-$HOME/.codex}/skills/"

python3 -m pip install -r \
  "${CODEX_HOME:-$HOME/.codex}/skills/native-transparent-imagegen/scripts/requirements.txt"
```

## Invoke

```text
Use $native-transparent-imagegen with my authorized character reference to create a transparent
PNG sticker. It must contain model-native alpha. Do not use background removal, chroma key,
segmentation, or a drawn checkerboard. Generate and validate one untouched original at a time;
if three attempts still lack alpha, report failure.
```

## Validate

```sh
python3 \
  "${CODEX_HOME:-$HOME/.codex}/skills/native-transparent-imagegen/scripts/validate_alpha.py" \
  --require-transparent-corners \
  /path/to/original-output.png
```

The read-only validator reports format, dimensions, SHA-256, encoded alpha, alpha extrema,
fully transparent pixel count, and corner values. Missing alpha, no fully transparent pixels,
an entirely transparent file, or non-transparent required corners fails the gate.

Metadata is not edge quality. Inspect the original over contrasting viewer backgrounds and
reject broad translucent haze, matte fringes, drawn checkerboards, clipped fur, or identity
errors even when alpha metadata passes.

## First-version Tuanzi and Hutao case

The [case record](../examples/native-transparent-imagegen-tuanzi-hutao.md) used a watermarked
first-version character action sheet supplied directly by Fini Yang as a local identity and
medium reference. The character sheet and generated originals are not part of the Apache code
license; the public package retains only auditable hashes, results, and acceptance boundaries.

Of three native generations, one returned RGBA and two returned RGB checkerboards. The RGBA
file passed the technical alpha gate but contained a broad low-alpha atmospheric haze, so its
technical result passed while its hero-case visual result failed. This is why the skill never
equates alpha metadata with clean fur edges.

## Maintenance boundary

Serialized calls and retries can be relaxed when the host exposes reliable native-alpha output
and verified concurrent behavior. Original-file validation, fine-edge QA, no-postprocessing
evidence, and separate acceptance states remain useful for production assets.
