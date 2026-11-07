# GitHub Pages publishing setup

## Current deployment — 2026-11-08

The user explicitly approved the Japanese HTML article for publication. PR #1 was merged as `3932b70cf193eaaef1bb84f3ae67943735eb9af8`.

- Repository: https://github.com/mameend/japanese-culture-journal
- Site: https://mameend.github.io/japanese-culture-journal/
- Pages source: **Deploy from a branch → main → / (root)**.
- The remote repository currently has the article HTML and editorial records at its root. The local workspace retains `outputs/` and `articles/tea-and-ceramics/`.
- Both Japanese and English HTML editions are available with reciprocal JP/EN links. Rebuild English after Japanese edits with `python3 scripts/build_english.py` locally, or `python3 build_english.py` in the flat GitHub checkout. Update `translations.en.json` when source copy changes.
- Changes to `main` automatically trigger publication. Keep unapproved work on a separate branch and merge only after explicit human approval.
- The manual Actions workflow described below is a planned local prototype, not installed or enforced on GitHub. `release.json` records authorization but is not currently checked by the branch deployment. There is no enforced review rule configured by this setup.

## Planned manual release workflow (not active)

This project is prepared for a deliberate, human-approved release. It does not connect to GitHub or publish by itself.

## Release model

```text
draft branch → review on phone → human approval record → main branch → manual Pages release
```

The Pages workflow is manual only. It runs only from `main`, only when the person starting it enters `PUBLISH`, and only when both approval records say the article has human approval. This is a guardrail, not a substitute for reviewing the article.

## One-time GitHub setup

1. Create an empty **public** GitHub repository, for example `japanese-culture-journal`. Everything in a public repository is visible to anyone, so include only material that is safe to disclose.
2. Add that repository as this folder's `origin` remote, then push the local `draft` branch. This keeps the work out of the public site.
3. On GitHub, open a pull request from `draft` to `main`. Review it on a computer or in GitHub Mobile. Do not merge it until the article's `approval.md`, fact register, and image-rights register are complete.
4. In repository **Settings → Pages**, set **Source** to **GitHub Actions**. This merely enables the release workflow; it does not publish a page.
5. After human approval, update `articles/tea-and-ceramics/approval.md` and `outputs/release.json` on the pull request, then merge into `main`.
6. On a phone or computer, open the repository in a browser, choose **Actions → Publish approved site → Run workflow**, and enter `PUBLISH`. GitHub Pages will then provide the live URL.

## Daily editorial rhythm

1. Codex prepares the next draft, source rows, asset rows, and a local HTML preview on `draft`.
2. Review the changed files from the phone. Leave unresolved facts, image rights, or wording as changes requested.
3. When ready, review the local or branch preview, fill the human approval record, and merge the reviewed pull request to `main`.
4. Use the manual Pages workflow to release. Record the live URL and date in `approval.md`.

## Important limits

- GitHub Pages is public. Do not release preliminary drafts, personal information, unlicensed images, or source material that must stay private.
- The current hero is original CSS artwork and has an image-rights record. The workflow is intentionally blocked until the human approval record is completed.
- For a later article, copy the first article's folder and give it its own draft, source, asset, and approval records. Update the release workflow to check each article's approval record before making it public.
