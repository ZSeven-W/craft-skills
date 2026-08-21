# Native transparency case: first-version Tuanzi and Hutao

This case exercises native alpha on fur that would be costly to extract cleanly after generation.

## Rights and release boundary

The held-out reference is Fini Yang's watermarked first-version Tuanzi and Hutao character action
sheet. It was supplied directly by the rights holder for this test. The sheet and generated
raster originals are not redistributed in this repository and are not licensed under Apache-2.0.
Their hashes are included only to identify the inspected evidence.

## Fixed method

- Built-in image generation; no API key.
- One request at a time.
- The reference was labeled as identity and colored-pencil medium guidance, not an edit target.
- Each prompt requested native PNG alpha.
- No background removal, chroma key, segmentation, mask, local alpha writing, resizing, or other
  raster postprocessing was used.
- The original returned files were inspected with Pillow and the skill validator contract.

## Reference evidence

```text
role: held-out identity and medium reference
dimensions: 1086x1448
mode: RGB
sha256: fa6d089525ee28f628d7fb787575fd6964f0f620bfa24a1bb6aaeb703c94fc5c
```

## Attempts

| Attempt | Requested asset | Original result | Technical alpha gate | Visual edge gate |
|---|---|---|---|---|
| 1 | Tuanzi and Hutao sitting together | PNG 1536x1024 RGBA; alpha 0-254; 854,016 fully transparent pixels; four corners 0 | pass | fail: broad low-alpha atmospheric haze around the fur |
| 2 | Tuanzi leaning against Hutao | PNG 1254x1254 RGB with a drawn checkerboard | fail: missing alpha | not run |
| 3 | Hutao lying on its back | PNG 1402x1122 RGB with a drawn checkerboard | fail: missing alpha | not run |

## Prompt set

The local file path was supplied to the built-in tool separately and is intentionally omitted
from the public prompts.

### Attempt 1

```text
Use the attached image only as the authorized identity and medium reference for the first-version
Tuanzi and Hutao characters. Create the same two cats sitting shoulder to shoulder and looking up
curiously: Tuanzi is the compact round golden short-haired cat with the small cream muzzle and
chest; Hutao is the larger very fluffy white long-haired cat with fine flyaway fur and a full plume
tail. Preserve the original first-version colored-pencil linework, restrained cream/gold/white
palette, small facial features, and natural cat proportions. Return a PNG whose entire area outside
the two cats is genuine pixel transparency with a real alpha channel. Keep both cats complete and
uncropped with generous transparent padding. No room, floor, blue pencil backdrop, speech bubble,
text, watermark, border, glow, or shadow.
```

### Attempt 2

```text
Use the attached sheet only as the authorized identity and medium reference for the first-version
Tuanzi and Hutao characters. Draw Tuanzi, the compact round golden short-haired cat, gently leaning
against Hutao, the larger fluffy white long-haired cat with fine flyaway fur and a full plume tail.
Match the first-version colored-pencil outlines, small facial features, quiet expressions,
restrained cream/gold/white palette, and natural cat proportions. Generate this as a native
transparent PNG: every pixel outside the cats must have alpha 0, except only a narrow anti-aliased
fringe needed for individual fur strands. The cats themselves should be opaque. No colored haze,
ambient glow, vignette, backdrop, floor, cast shadow, blue pencil patch, speech bubble, text,
watermark, or border. Keep the complete duo centered and uncropped with generous empty transparent
padding.
```

### Attempt 3

```text
Use the attached sheet only as the authorized identity and colored-pencil medium reference for
first-version Hutao. Draw Hutao, the same very fluffy white long-haired cat with green eyes, pink
ears, fine flyaway fur, and a full plume tail, lying comfortably on its back with paws relaxed.
Return a native transparent PNG with a real alpha channel; everything outside the cat must be
transparent. Keep the complete cat centered with transparent padding. No floor, shadow, glow,
backdrop, blue pencil patch, text, speech bubble, watermark, or border.
```

Attempt 1 original SHA-256:

```text
066d5b134cbc267a52bbca681afc742b7c64cc2313e1cd77ff3fce5180a8fbb8
```

## Verdict

The case proves that the host can return native alpha for first-version Tuanzi and Hutao fur, but
does not establish reliable delivery or a clean public hero asset. The accepted public claim is:

> Native alpha succeeded in one inspected attempt; two opaque checkerboard outputs and one visual
> haze failure show why prompts alone are insufficient.

The case remains an experimental regression record, not a published character asset, user
acceptance, or permission to release the held-out images.
