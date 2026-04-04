# Research: Adding Isometric Commit Calendar to README

To add an Isometric Commit Calendar to your GitHub profile README, the most recommended tool is [lowlighter/metrics](https://github.com/lowlighter/metrics).

## 1. What is Isometric Commit Calendar?
It is a plugin for the `metrics` library that renders your GitHub contribution history in a 3D isometric view, similar to a city where the height of each block represents the number of commits.

## 2. How to implement it
The easiest way is to use a GitHub Action that runs on a schedule and generates an SVG image, which you then link in your README.

### Prerequisites
- **GitHub Personal Access Token (PAT):** Some plugins in `metrics` require a PAT with `read:user` and `repo` scopes to fetch detailed data. However, the `isocalendar` plugin can sometimes work with the default `${{ secrets.GITHUB_TOKEN }}` depending on the visibility of your contributions.
- **Workflow file:** You need a `.github/workflows/metrics.yml` file.

### Proposed Workflow (`.github/workflows/metrics.yml`)
```yaml
name: Metrics
on:
  # Schedule updates (each hour)
  schedule: [{cron: "0 * * * *"}]
  # Lines below allow to run workflow manually and on each commit
  workflow_dispatch:
  push: {branches: ["master", "main"]}
jobs:
  github-metrics:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: lowlighter/metrics@latest
        with:
          # Your GitHub token
          token: ${{ secrets.METRICS_TOKEN }}

          # Options
          user: Umerjamshaid
          template: classic
          base: ""
          config_timezone: Asia/Karachi # Adjust to your timezone
          plugin_isocalendar: yes
          plugin_isocalendar_duration: half-year
```

## 3. README Integration
Once the workflow runs, it will generate a file (usually `github-metrics.svg` by default, or you can specify the filename). You can then add it to your `README.md` like this:

```markdown
![Isometric Calendar](https://github.com/Umerjamshaid/Umerjamshaid/blob/master/github-metrics.svg)
```
*(Note: The path depends on where the Action saves the file. Usually, it's pushed to the main branch or a specific output branch.)*

## 4. Alternative: Simple Readme Stats
If you don't want to set up a GitHub Action, there are other community-driven tools, but `lowlighter/metrics` is the most powerful and customizable one for this specific 3D look.

---
**Recommendation:** 
I can set up the `.github/workflows/metrics.yml` for you. You will just need to add a `METRICS_TOKEN` to your repository secrets if the default token doesn't provide enough data.
