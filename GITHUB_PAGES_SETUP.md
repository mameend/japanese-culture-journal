# GitHub Pages publishing setup

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
