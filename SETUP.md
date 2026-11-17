# GitHub Actions setup — Bhavish-S profile

The workflows are already included and use the `Bhavish-S` account. They do not require a personal access token.

## 1. Repository and branch

Use the profile repository named **`Bhavish-S`** under the account **`Bhavish-S`** (the repository URL supplied was `https://github.com/Bhavish-S`; the profile README repository itself should be `https://github.com/Bhavish-S/Bhavish-S`). Commit the project files to the repository's default branch. The workflow push filters currently target `main`; change the branch name in the two workflow files if your default branch is different.

## 2. Enable workflow write permissions

In GitHub, open **Settings → Actions → General → Workflow permissions** and select **Read and write permissions**. This is required because the workflows commit generated SVGs. Keep the permissions repository-scoped; no PAT is needed.

Also ensure GitHub Actions are allowed for the repository. If branch protection or a ruleset blocks bot pushes to `main`, permit the Actions bot to update the generated SVG paths or adjust your ruleset.

## 3. Run the profile cards workflow

Open **Actions → Refresh Bhavish profile cards → Run workflow**. The workflow generates `assets/stats/overview.*.svg`, `contributions.*.svg` and `languages.*.svg` using GitHub account data and commits updates. It also runs daily at `00:13 UTC`.

Until the first successful run, the existing local cards are intentional non-numeric placeholders: they do not fabricate contribution, star, follower, or language counts.

## 4. Run the contribution snake workflow

Open **Actions → Generate contribution snake → Run workflow**. It uses `Platane/snk` to generate light and dark SVGs and commits them to `assets/contributions/`. It also runs daily at `00:17 UTC`.

The workflows use pinned action commit SHAs. The snake workflow only reacts to changes to its workflow file (besides manual and scheduled runs), so its own SVG commits do not create an infinite loop. The cards workflow uses `[skip ci]` in its commit message and filters pushes to README/workflow changes only.

## 5. Optional assets

The original README contains an optional metrics action setup and a 3D contribution map image reference. Their original instructions/markup are preserved. The local placeholder SVGs avoid broken image references until those optional generators are configured; the placeholders contain no invented statistics.

## External services

The new hero, ambient accent, radar SVG/GIF, project cards, social buttons, local badges, local stats placeholders, snake placeholders, and footer are self-hosted in this repository. The stats cards and snake become live local files after their workflows run. The README's pre-existing profile counter, activity graph, LeetCode card, trophy card, quote service, typing SVGs, skillicons images, GitHub summary cards, and other remote images remain external because the supplied content is retained verbatim. Their availability is controlled by the respective third-party services.

## Local badge regeneration

Run `python tools/generate_badges.py` from the repository root to regenerate the theme-aware SVG badge library. Python 3 is sufficient; no third-party packages are required by that script.
