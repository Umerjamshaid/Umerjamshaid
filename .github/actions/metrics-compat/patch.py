"""Small, checked patches for the pinned original Metrics source and image."""

from pathlib import Path
import sys

IMAGE = "ghcr.io/lowlighter/metrics@sha256:b8013996b12be3ea049fad2e18db6b31083575a197e43ed63a690a094b9164fb"
PATCHES = {
    "source/plugins/achievements/queries/achievements.graphql": [
        ("    projects(first:", "    projects: projectsV2(first:"),
    ],
    "source/plugins/habits/index.mjs": [
        (".flatMap(({payload}) => payload.commits)",
         ".flatMap(({payload}) => payload?.commits ?? [])\n          .filter(commit => commit?.author)"),
    ],
    "source/plugins/lines/index.mjs": [
        ('if (data.account)', 'if (account === "organization")'),
        ("${contributor.author.login}", '${contributor.author?.login ?? "unknown"}'),
    ],
}


def replace_checked(source, before, after):
    if source.count(before) != 1:
        raise ValueError(f"Pinned upstream source changed: expected one occurrence of {before!r}")
    return source.replace(before, after)


def patch(root):
    for relative, replacements in PATCHES.items():
        target = root / relative
        source = target.read_text(encoding="utf-8")
        for before, after in replacements:
            source = replace_checked(source, before, after)
        target.write_text(source, encoding="utf-8")

    target = root / "action.yml"
    source = target.read_text(encoding="utf-8")
    source = replace_checked(source, "METRICS_ACTION: ${{ github.action }}", "METRICS_ACTION: lowlighter_metrics")
    source = replace_checked(source, "METRICS_IMAGE=ghcr.io/lowlighter/metrics:$METRICS_TAG", f"METRICS_IMAGE={IMAGE}")
    # Mount only patched files; keep the original image's dependencies and built templates.
    mounts = " ".join(f'--volume "$METRICS_ACTION_PATH/{p}:/metrics/{p}:ro"' for p in PATCHES)
    source = replace_checked(source, "docker run --init --rm ", f"docker run --init --rm {mounts} ")
    target.write_text(source, encoding="utf-8")


if __name__ == "__main__":
    patch(Path(sys.argv[1]))
    print("Applied three local compatibility fixes using the pinned original Metrics image.")
