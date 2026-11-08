# Photo rights evidence — 2026-11-08

The owner requested a design inspired by https://menomeonline.com/ and photographs that can be published. That site was inspected for visual direction only. No photographs, logo, text, or code were copied from it.

## Policy verified

- Provider: The Metropolitan Museum of Art, New York.
- Policy: https://www.metmuseum.org/hubs/open-access
- Opened on 2026-11-08. Public-domain artwork images are available under Creative Commons Zero (CC0), for unrestricted use.
- Both selected collection pages displayed **Public Domain**; official API responses returned `isPublicDomain: true`.
- The collection pages explicitly allow unrestricted commercial and noncommercial use of Open Access data and public-domain images without permission or fee.
- Attribution is not required by CC0; this project voluntarily credits the museum, object records, and collection credit lines. No museum endorsement is implied and no museum logos are used.

## asset-002 — Red Raku Tea Bowl (Chawan)

- File: `outputs/red-raku-tea-bowl.jpg` (repository root on GitHub).
- Object: 36.120.525; Japan; 18th century.
- Attribution: **Style of Hon'ami Kōetsu, by an unknown potter**. Do not state that Kōetsu made this work.
- Japanese collection title: 赤楽茶碗　本阿弥光悦様式.
- Record: https://www.metmuseum.org/art/collection/search/63180
- API: https://collectionapi.metmuseum.org/public/collection/v1/objects/63180
- Image: https://images.metmuseum.org/CRDImages/as/original/DP260410.jpg
- Credit: The Howard Mansfield Collection, Gift of Howard Mansfield, 1936.
- Rights: Public Domain / CC0; commercial use permitted.
- Processing: original JPEG, no color change or generated alteration; responsive CSS only.
- Use: main article photograph and social-sharing image.

## asset-003 — Tea Bowl with Cross Design

- File: `outputs/tea-bowl-mishima.jpg` (repository root on GitHub).
- Object: 29.100.633; Japan; early 19th century.
- Japanese collection title: 十字文三島茶碗.
- Record: https://www.metmuseum.org/art/collection/search/63114
- API: https://collectionapi.metmuseum.org/public/collection/v1/objects/63114
- Image: https://images.metmuseum.org/CRDImages/as/original/DP239535.jpg
- Credit: H. O. Havemeyer Collection, Bequest of Mrs. H. O. Havemeyer, 1929.
- Rights: Public Domain / CC0; commercial use permitted.
- Processing: original JPEG, no color change or generated alteration; responsive CSS only.
- Use: in-article photograph.

## Verification scope

Source inspection and captions checked by Codex on 2026-11-08 against official records. This is an automated editorial check, not separate human fact-check review. The existing essay body is unchanged; new factual text is limited to the photographed objects' titles, dates, attribution, collection, and rights.

The monochrome candidate `outputs/tea-bowl-raku.jpg` (object 62884) was considered but is not used or uploaded. The former CSS hero is retired. Original API snapshots are retained locally in `evidence/`.


## 2026-11-08 remediation — current publication

The owner explicitly requested updates to GitHub and the public site after the image audit.
This review does not conclude that the previous use was unauthorized.

- All active photographs are recorded in assets.csv with file path, SHA-256, source, terms and actual uses, including list thumbnails.
- Kutani and Hasami now use the historical Met CC0 examples already used in the regional guide (48822 and 63699). Both files were compared byte-for-byte with the official API primaryImageSmall. Official API snapshots are committed alongside the other 10 regional Met records.
- The four contemporary Commons photographs (Kasama, Kutani teacup, Hasami display, Mino table setting) and the LACMA photograph were removed from all current pages and from the current repository tree. Their audit rows remain as retired_pending_verification. This is a conservative publication decision, not a finding that CC BY/CC BY-SA prohibits commercial use.
- Kasama and Tsuboya remain available as complete articles with official maker links and text covers. No unrelated regional image was substituted.
- Tobe: Commons identifies Gryffindor, CC0 1.0, and a 2018-01-15 background cleanup by PawełMM. Captions retain both names and identify the cleanup rather than claiming that the source was never modified. Source-file binary comparison remains pending; CC0 publication is based on the individual author declaration at https://commons.wikimedia.org/wiki/File:Aichi_Prefectural_Ceramic_Museum_(56).jpg .
- Mashiko: the individual record states Public Domain. The museum's official dataset https://github.com/artsmia/collection/blob/main/objects/116/116947.json states rights_type=Public Domain, restricted=0, image_copyright=null. https://new.artsmia.org/copyright-and-image-access specifically permits commercial use and modification of PD images. It is not recorded as CC0. Source-file binary comparison remains pending. Captions do not assert verified absence of processing.
- Met policy: https://www.metmuseum.org/policies/image-resources . CC0 permits commercial use and modification, without mandatory attribution or ShareAlike; credit is retained voluntarily.
- Reader-facing bilingual image-credits pages provide source links and distinguish editorial copyright from image rights.
- Retired material remains in Git history and in the audit ledger for provenance. Do not reuse it until the open source/binary/underlying-work questions recorded in its notes have been resolved.

### Remaining scope limitations

Source institutions' PD determinations and the Commons author's CC0 declaration are the basis of publication. This is not a guarantee of every third-party right in every jurisdiction. Do not replace unknown authors with an invented attribution. Future image additions must pass scripts/check_image_rights.py; the check verifies registration and file integrity, not legal ownership or licensing authority.


## 2026-11-08 — flower article photograph

- Article: `flowers-one-stem.html` and its English edition. The owner requested a suitable free-to-use photograph after reviewing the article.
- Photographer: Marianne Krohn, as identified by the [individual Unsplash photo page](https://unsplash.com/photos/a-single-pink-flower-in-a-clear-vase-z4NUcUZO-58).
- License: [Unsplash License](https://unsplash.com/license), opened on 2026-11-08. It permits free commercial use and modification worldwide without mandatory attribution. It is not CC0 or a public-domain dedication.
- Restrictions: no sale without significant modification; no compilation to replicate a similar or competing image service. The use here is an editorial illustration, not a standalone image sale or image-library service.
- Voluntary credit and links are displayed in Japanese/English captions and image-credit pages. No photographer or school endorsement is claimed.
- File: `flowers-one-stem-marianne-krohn.jpg`, SHA-256 `bc16c4fb19ccbfcd1fa49b25232bad90183897d11c244b9b12d2d9e18b64e06e`. The repository copy is byte-identical to the downloaded 3000-pixel JPEG rendition. The browser crops its display to fit the article and card layouts. No other local processing was performed and no statement is made about processing before download.
- The inspected photograph shows a pale pink flower in a plain clear glass bottle, with no identifiable person, readable brand, or separately reproduced artwork observed. We do not assert the flower species, arrangement author, location, or affiliation with any ikebana school.
- Structured evidence and all six use locations: `articles/flowers-one-stem/photo-evidence.json` and `assets.csv`.
