#!/usr/bin/env python3
"""Run deterministic hygiene checks for the public release package."""

from __future__ import annotations

import hashlib
import re
import struct
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
REQUIRED = (
    ROOT / "README.md",
    ROOT / "README.en.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "LICENSE",
    ROOT / "THIRD_PARTY_NOTICES.md",
    ROOT / ".github" / "CODEOWNERS",
    ROOT / "assets" / "examples" / "README.md",
    ROOT / "examples" / "handoff-hero.md",
)
MEDIA_SUFFIXES = {
    ".mp4",
    ".m4v",
    ".mov",
    ".webm",
    ".mkv",
    ".avi",
    ".m4a",
    ".mp3",
    ".aac",
    ".wav",
    ".flac",
    ".gif",
    ".jpg",
    ".jpeg",
    ".png",
    ".svg",
    ".webp",
}
ALLOWED_TEXT_SUFFIXES = {".json", ".md", ".py", ".txt", ".yaml"}
ALLOWED_TEXT_FILENAMES = {".gitignore", "CODEOWNERS", "LICENSE"}
BANNED_MEDIA_PATH_PARTS = {
    "contact-sheets",
    "raw-media",
    "source-media",
    "source-screenshots",
    "source-videos",
    "video-frames",
}
APPROVED_ASSETS = {
    Path("assets/examples/handoff/handoff-qa-board.png"): (
        "0741664632f5dcb8e39a540c3e48b13d0934e6fb7abed4f2ae408c8fc116823e",
        92196,
        (1200, 900),
    ),
    Path("assets/examples/handoff/handoff-qa-board.svg"): (
        "e6f56809e1fbb6ef17921e93b43c962e3d335e9d67187bffb3cdf53d78160d60",
        4361,
        None,
    ),
    Path("assets/examples/handoff/handoff-mark.svg"): (
        "f6ebeb8a021f79f6c48be5a1a498cdbd0842085a32195c506f629938faf56e65",
        547,
        None,
    ),
    Path("assets/examples/handoff/handoff-concept-sheet.png"): (
        "bff47ca23cdfa1297131a06a7ffa61138739972cccc12472d5d983feee692207",
        152995,
        (1440, 960),
    ),
    Path("assets/examples/handoff/handoff-micro-mark.svg"): (
        "4d31a61aba2f5e0f380ced0847451cb99f2d288bae7234749b0e4c8398a18a5f",
        505,
        None,
    ),
    Path("assets/examples/handoff/handoff-concept-sheet.svg"): (
        "1c3f04d66a0fe4fd311480d1c7c5b63cbc02141f0c5259239f2ac07572be4c38",
        5850,
        None,
    ),
    Path("assets/examples/xiuyue/xiuyue-symbol.svg"): (
        "ebab75aa83c6bc1191286723b903b51fda2bd909c84f1973338aff01d734b66b",
        520,
        None,
    ),
    Path("assets/examples/xiuyue/xiuyue-case-board.svg"): (
        "7559f8173326da2a7d92a090d4d351b6a916047237e3d712ec95a0d300eae9b7",
        5337,
        None,
    ),
    Path("assets/examples/xiuyue/xiuyue-case-board.png"): (
        "c21d943dab3fe8382fde939a5974435e44de9373e025f5a83519d7c195cb6341",
        127830,
        (1200, 900),
    ),
    Path("assets/examples/xiuyue/xiuyue-micro-symbol.svg"): (
        "54dfef21436e7ca446909a0bc2887597684a0c23063a99e40d7828690af44bd9",
        453,
        None,
    ),
    Path("assets/examples/d-tool/d-tool-qa-board.svg"): (
        "4128ea50e636cdc94a18660a7de488913a8dd08cb2170e629109c48f806d750e",
        3520,
        None,
    ),
    Path("assets/examples/d-tool/d-tool-qa-board.png"): (
        "66f3950183c39edba8d362cd7794d39599ccc50757b0f5a99c4f4994e4559a40",
        73341,
        (1200, 900),
    ),
    Path("assets/examples/d-tool/d-tool-mark-mono.svg"): (
        "99b5ee85ea4569709b7c1e09618df4e61aead049fbc415b32c1b4721f3a14ccc",
        589,
        None,
    ),
    Path("assets/examples/d-tool/icons/d-tool-16.png"): (
        "bc5a52e013bcec05f194a646c9909c2709dbd86e4745c9be619cda61459b5539",
        293,
        (16, 16),
    ),
    Path("assets/examples/d-tool/icons/d-tool-24.png"): (
        "f78e505983c38276b4f8dd218aa2cf0048343c90b6073d666a64672481a388d9",
        419,
        (24, 24),
    ),
    Path("assets/examples/d-tool/icons/d-tool-32.png"): (
        "e9fc0e7cb94d210ba9b8ac633432aa9810486cd77ff638dc5dbdbf77aa7a9823",
        457,
        (32, 32),
    ),
    Path("assets/examples/d-tool/icons/d-tool-64.png"): (
        "fa89c628c128781de3e421daefc9f0e47558df7db974ca1935bba520076cd8c5",
        841,
        (64, 64),
    ),
    Path("assets/examples/d-tool/icons/d-tool-128.png"): (
        "16755ae669e0d0d7807030136bca77fa08eae05a5d2d285eaafa9b44a9e870df",
        1703,
        (128, 128),
    ),
    Path("assets/examples/d-tool/d-tool-mark.svg"): (
        "09b090f4ab60410948aa16a6811e77df60e0fa68c19f55a3acf858307b1bc41a",
        578,
        None,
    ),
    Path(
        "assets/examples/recurring-character-diary-comic/"
        "recurring-character-diary-comic-cover.png"
    ): (
        "aef95d57385e4888351cc91172d144f13488596215ebe47d9a76fa7bf3619954",
        643725,
        (1000, 400),
    ),
}
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"\bghp_[A-Za-z0-9]{20,}"),
    re.compile(r"\b(?:sessionid|sid_guard|__ac_signature)\s*[:=]", re.I),
)
ABSOLUTE_PATH_PATTERNS = (
    re.compile("/" + r"Users/[^\s)`]+"),
    re.compile("/" + r"home/[^\s)`]+"),
    re.compile(r"[A-Za-z]:\\Users\\[^\s]+"),
)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_required_files() -> None:
    for path in REQUIRED:
        if not path.is_file():
            fail(f"missing required file: {path.relative_to(ROOT)}")


def discover_skills() -> tuple[Path, ...]:
    if not SKILLS_ROOT.is_dir():
        fail("missing skills directory")
    skills = tuple(
        sorted(path.parent for path in SKILLS_ROOT.glob("*/SKILL.md"))
    )
    if not skills:
        fail("no skills found")
    for child in SKILLS_ROOT.iterdir():
        if child.is_dir() and not (child / "SKILL.md").is_file():
            fail(f"skill directory is missing SKILL.md: {child.name}")
    return skills


def check_skill_frontmatter(skill: Path) -> None:
    path = skill / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if not match:
        fail("SKILL.md frontmatter is missing or malformed")
    frontmatter = match.group(1)
    name_match = re.search(r"^name:\s*([^\n]+)$", frontmatter, re.M)
    description_match = re.search(r"^description:\s*([^\n]+)$", frontmatter, re.M)
    if not name_match or not description_match:
        fail("SKILL.md requires name and description")
    name = name_match.group(1).strip().strip('"\'')
    if name != skill.name or not re.fullmatch(r"[a-z0-9-]{1,63}", name):
        fail(f"invalid skill name: {name}")
    if len(description_match.group(1).strip()) < 40:
        fail("skill description is too short to define a useful trigger")

    openai_yaml = skill / "agents" / "openai.yaml"
    if not openai_yaml.is_file():
        fail(f"missing agents/openai.yaml for {skill.name}")
    for readme_name in ("README.md", "README.en.md"):
        if not (skill / readme_name).is_file():
            fail(f"missing {readme_name} for {skill.name}")
    evals = ROOT / "evals" / skill.name / "cases.yaml"
    if not evals.is_file():
        fail(f"missing evals for {skill.name}: {evals.relative_to(ROOT)}")


def check_markdown_links() -> None:
    root = ROOT.resolve()
    for source in ROOT.rglob("*.md"):
        text = source.read_text(encoding="utf-8")
        targets = re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", text)
        targets.extend(re.findall(r"\bsrc=[\"']([^\"']+)[\"']", text, re.I))
        for raw_target in targets:
            target = raw_target.strip().strip("<>").split("#", 1)[0]
            if not target or target.startswith(
                ("http://", "https://", "mailto:", "#")
            ):
                continue
            target = target.split(maxsplit=1)[0]
            resolved = (source.parent / target).resolve()
            try:
                resolved.relative_to(root)
            except ValueError:
                fail(f"local Markdown link escapes release root: {source}: {target}")
            if not resolved.is_file():
                fail(
                    "broken local Markdown link: "
                    f"{source.relative_to(ROOT)} -> {target}"
                )


def verify_approved_asset(path: Path, relative: Path) -> None:
    expected_hash, expected_size, expected_dimensions = APPROVED_ASSETS[relative]
    data = path.read_bytes()
    if len(data) != expected_size:
        fail(f"approved asset size changed: {relative}")
    actual_hash = hashlib.sha256(data).hexdigest()
    if actual_hash != expected_hash:
        fail(f"approved asset hash changed: {relative}")

    if path.suffix.lower() == ".png":
        if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
            fail(f"invalid PNG signature: {relative}")
        width, height = struct.unpack(">II", data[16:24])
        if (width, height) != expected_dimensions:
            fail(
                f"approved PNG dimensions changed: {relative} "
                f"({width}x{height})"
            )
        lowered = data.lower()
        for marker in (b"c2pa", b"gpt-image", b"trainedalgorithmicmedia"):
            if marker in lowered:
                fail(f"generated-media provenance marker in {relative}")


def check_svg_safety(text: str, relative: Path) -> None:
    lowered = text.lower()
    for token in ("<script", "<foreignobject", "<image", "javascript:", "data:"):
        if token in lowered:
            fail(f"unsafe or embedded SVG content in {relative}: {token}")
    if re.search(r"\son[a-z]+\s*=", text, re.I):
        fail(f"SVG event handler is not allowed: {relative}")
    if re.search(r"(?:href|xlink:href)\s*=\s*[\"'](?!#)", text, re.I):
        fail(f"external SVG reference is not allowed: {relative}")
    if "<title" not in lowered or "<desc" not in lowered:
        fail(f"approved SVG requires title and desc: {relative}")


def check_asset_references() -> None:
    markdown = "\n".join(
        path.read_text(encoding="utf-8") for path in ROOT.rglob("*.md")
    )
    for relative in APPROVED_ASSETS:
        if relative.as_posix() not in markdown:
            fail(f"approved asset is not referenced by documentation: {relative}")


def check_tree_hygiene() -> None:
    seen_assets = set()
    for path in ROOT.rglob("*"):
        if ".git" in path.parts:
            continue
        relative = path.relative_to(ROOT)
        if path.is_symlink():
            fail(f"symbolic links are not allowed in release: {relative}")
        if path.is_dir():
            continue
        if not path.is_file():
            fail(f"unexpected non-regular filesystem entry: {relative}")
        if any(part.lower() in BANNED_MEDIA_PATH_PARTS for part in relative.parts):
            fail(f"banned source-media path in release: {relative}")
        if path.stat().st_size > 1_048_576:
            fail(f"file exceeds 1 MiB: {relative}")

        if relative in APPROVED_ASSETS:
            verify_approved_asset(path, relative)
            seen_assets.add(relative)
            if path.suffix.lower() == ".png":
                continue
        elif path.suffix.lower() in MEDIA_SUFFIXES:
            fail(f"unapproved media asset in release: {relative}")
        elif (
            path.suffix.lower() not in ALLOWED_TEXT_SUFFIXES
            and path.name not in ALLOWED_TEXT_FILENAMES
        ):
            fail(f"unapproved release file type: {relative}")

        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            fail(f"unexpected binary file: {relative}")
        if path.suffix.lower() == ".svg":
            check_svg_safety(text, relative)
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                fail(f"possible secret in {relative}: {pattern.pattern}")
        for pattern in ABSOLUTE_PATH_PATTERNS:
            if pattern.search(text):
                fail(f"machine-specific absolute path in {relative}")

    missing_assets = set(APPROVED_ASSETS) - seen_assets
    if missing_assets:
        fail(
            "missing approved assets: "
            + ", ".join(str(path) for path in sorted(missing_assets))
        )


def check_openai_yaml(skill: Path) -> None:
    text = (skill / "agents" / "openai.yaml").read_text(encoding="utf-8")
    if f"${skill.name}" not in text:
        fail(
            "agents/openai.yaml default_prompt must name "
            f"${skill.name}"
        )


def check_eval_schemas(skills: tuple[Path, ...]) -> None:
    for skill in skills:
        eval_dir = ROOT / "evals" / skill.name
        cases = eval_dir / "cases.yaml"
        validator = eval_dir / "validate_cases.py"
        requirements = eval_dir / "requirements.txt"
        self_test = eval_dir / "self_test_validate_cases.py"
        if not validator.is_file():
            fail(f"missing eval validator for {skill.name}: {validator.relative_to(ROOT)}")
        if not requirements.is_file():
            fail(
                f"missing eval requirements for {skill.name}: "
                f"{requirements.relative_to(ROOT)}"
            )
        result = subprocess.run(
            [sys.executable, "-B", str(validator), str(cases)],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            detail = (result.stderr or result.stdout).strip()
            fail(
                f"eval validator failed for {skill.name}; install "
                f"{requirements.relative_to(ROOT)}"
                + (f": {detail}" if detail else "")
            )
        if self_test.is_file():
            result = subprocess.run(
                [sys.executable, "-B", str(self_test)],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                detail = (result.stderr or result.stdout).strip()
                fail(
                    f"eval self-test failed for {skill.name}"
                    + (f": {detail}" if detail else "")
                )


def check_collection_index(skills: tuple[Path, ...]) -> None:
    readmes = {
        "README.md": (ROOT / "README.md").read_text(encoding="utf-8"),
        "README.en.md": (ROOT / "README.en.md").read_text(encoding="utf-8"),
    }
    for skill in skills:
        expected_skill = f"skills/{skill.name}/"
        for readme_name, readme in readmes.items():
            if expected_skill not in readme:
                fail(f"{readme_name} does not index {skill.name}")

        expected_guides = {
            "README.md": ROOT / "docs" / f"{skill.name}.zh-CN.md",
            "README.en.md": ROOT / "docs" / f"{skill.name}.md",
        }
        for readme_name, guide in expected_guides.items():
            if not guide.is_file():
                fail(
                    f"missing public guide for {skill.name}: "
                    f"{guide.relative_to(ROOT)}"
                )
            expected_guide = guide.relative_to(ROOT).as_posix()
            if expected_guide not in readmes[readme_name]:
                fail(f"{readme_name} does not link {expected_guide}")


def main() -> int:
    check_required_files()
    skills = discover_skills()
    for skill in skills:
        check_skill_frontmatter(skill)
    check_markdown_links()
    check_tree_hygiene()
    check_asset_references()
    for skill in skills:
        check_openai_yaml(skill)
    check_eval_schemas(skills)
    check_collection_index(skills)
    print(f"release_check=ok skills={len(skills)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
