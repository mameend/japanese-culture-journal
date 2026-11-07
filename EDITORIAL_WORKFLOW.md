# Editorial workflow

## One article, one record

Each article lives in `articles/<slug>/`. Keep Japanese and English drafts separate so edits and approvals can be tracked independently. English may be adapted for readers rather than translated sentence-for-sentence, but factual claims must retain the same meaning and evidence.

## Working stages

1. **Idea / research** — capture the angle, reader, outline, and questions. Do not state uncertain details as facts.
2. **Drafting** — work in both language files. Mark unsupported particulars `[要確認]` / `[VERIFY]` in the draft and enter them in `sources.csv`.
3. **Fact check** — each material claim must point to a source. Record source type, access date, claim supported, and status (`unchecked`, `checked`, `needs_revision`). Prefer primary sources for historical or institutional claims; record disagreements and uncertainty.
4. **Image rights** — every used image needs an asset record with creator, source/original URL, license or permission scope, commercial-use status, attribution wording, evidence location, and reviewer. `unknown` means do not use. Keep original, edited, and AI-generated images identifiable.
5. **Editorial review** — check structure, tone, Japanese/English consistency, accessibility, links, and captions. Record unresolved issues in the article record.
6. **Human approval gate** — the human editor reviews the final versions of both drafts, all material fact-check rows, and every image-rights row. Only that person may enter their name, date, and approved version in `approval.md` and change status to `approved`. Any subsequent substantive edit resets approval to `approval_requested`.
7. **Publication** — the human publisher separately publishes through the chosen CMS and records the live URL/date. Approval does not itself publish. Codex must not publish, schedule, or send external communications.

## Minimum conditions to request approval

- Both language drafts are complete and internally consistent.
- No unresolved `[要確認]` / `[VERIFY]` markers remain.
- All material claims have a checked source entry, or are explicitly framed as interpretation/opinion.
- Every image intended for use has documented rights for the intended commercial and geographic use, plus the required attribution.
- The reviewer has checked headings, captions, links, and any disclosures.
- `approval.md` identifies the exact versions reviewed (record a commit ID or date/version label).

## Using Codex

Ask Codex to edit only the specified draft or records, then inspect the resulting diff. Useful requests include: “list unsupported factual claims,” “compare the JP and EN drafts for meaning,” and “check that every used image has a complete rights record.” These are preparation aids, not approval. Never treat an AI-generated source, citation, license statement, or fact-check as verified without opening the evidence.
