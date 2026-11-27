# Brand assets

erdostack has one visual identity, shared with [erdostack.com](https://erdostack.com): chalk on a chalkboard, set in the typeface of a mathematics paper.

## Files

| File | Size | Use |
|---|---|---|
| `logo.svg`, `logo.png` | 256 viewBox, 512 x 512 | The mark on a rounded chalkboard square. The README, plugin manifests and marketplaces use it. It is the site's favicon at a larger size. |
| `avatar.svg`, `avatar.png` | 1024 x 1024 | The mark on a full square, for profile pictures. Readable down to 24 px. |
| `avatar-numbered.svg`, `avatar-numbered.png` | 1024 x 1024 | The same three vertices labeled with their distance from the source: 0, 1, 1. For large placements only; the numbers are lost below about 40 px. |
| `social-preview.svg`, `social-preview.png` | 1280 x 640 | The share card. Upload the PNG as the repository's social preview. |

Only `logo.svg` and `logo.png` ship to users, in the npm package and the GitHub release archive. The PyPI package carries no images.

## The mark

Three vertices, every pair joined. One vertex is yellow: it is the source, the vertex at distance 0. On the site's larger graph the source is Erdős, and every other vertex shows its Erdős number.

- Yellow marks the source vertex and nothing else in the mark.
- Keep the mark on the chalkboard green. Do not recolor it, outline it or place it on another background.
- Do not add the name inside the mark. Set the name beside it, in lowercase, as one word: erdostack.

## Palette

| Name | Hex | Use |
|---|---|---|
| Board | `#22302a` | Background |
| Board, deep | `#1b2621` | Shaded areas and code blocks |
| Chalk | `#edeae0` | Text, edges and vertices |
| Dust | `#aab6ad` | Secondary text |
| Yellow | `#f0d264` | The source vertex, buttons and emphasis |
| Pink | `#f29a94` | High-severity findings and the unreached vertex |
| Blue | `#93cbe8` | Links and fixes |

The plugin manifests use the yellow as `brandColor`. The README badges use the board as the label color.

## Typeface

Latin Modern Roman, with Latin Modern Mono for code. Both are free to use and embed under the GUST Font License. Where they are not installed, fall back to Cambria or Times New Roman.

## Changing an image

The SVG files are the sources. Each PNG is its SVG rendered in a browser with Latin Modern available, then reduced to 256 colors. When you change one:

- Render the PNG again from the SVG, so the two never differ.
- Keep every PNG under 1 MB. GitHub rejects larger social previews and profile pictures.
- Save without embedded metadata.
- If the mark itself changes, change the site's favicon in the same pull request series, so the two stay identical.
