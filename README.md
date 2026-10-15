# iMAS Lab

**Intelligent Manufacturing and Autonomous Systems Laboratory**  
Department of Mechanical Engineering  
San José State University

Advancing manufacturing through sensing, intelligence, and autonomy.

A responsive website for GitHub Pages, written in HTML, CSS, and JavaScript. No package installation, build step, API key, or backend is required to host it.

## Publish with GitHub Pages

1. Extract `iMAS-Lab-GitHub-Pages.zip`.
2. Create a GitHub repository, or open your existing website repository.
3. Upload the **contents inside the extracted `imas-lab` folder**. Place `index.html` at the repository root, alongside `research.html`, `css`, `js`, and `assets`. Upload the extracted files, not the ZIP.
4. If replacing the previous design, delete the old `projects.html` from your repository. Uploading this package alone will not delete old files.
5. Open **Settings → Pages**. Under **Build and deployment**, choose **Deploy from a branch**, select **main** and **/ (root)**, then save.
6. Once deployment finishes, GitHub displays the website address in Pages settings.

Relative page and asset links support both project URLs such as `https://USERNAME.github.io/imas-lab/` and sites at the domain root. The example address is not a published deployment.

Official guide: [Configuring a publishing source for GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

## Preview

Open the accompanying `iMAS-Lab-preview.html` in a browser to navigate the complete design. You can also open `index.html` from the extracted folder. The preview embeds the local artwork, portrait, scripts, styles, and citation downloads. Author-hosted publication images, paper PDFs, DOI links, and external profiles need an internet connection.

Publication search, category/year filters, citations, the Sense–Model–Adapt controls, and figure enlargement use JavaScript. Page content and ordinary links remain usable without it. Clipboard access varies for local files; a selectable citation dialog is available as a fallback.

## Where to edit

| File | Content |
| --- | --- |
| `index.html` | Manufacturing illustration, research pillars, interactive research approach, and PI introduction |
| `research.html` | Research areas and methods |
| `publications.html` | Publication page introduction and controls; records are generated from the data file |
| `data/publications.json` | Publication metadata, PDF links, DOIs, and figure paths |
| `people.html` | PI portrait, biography, and profile links |
| `resources.html` | Public profiles and bibliography downloads |
| `contact.html` | `Emmanuel.ogunniyi@sjsu.edu` and inquiry guidance |
| `css/styles.css` | Colors, spacing, typography, and responsive layouts |
| `js/main.js` | Navigation, filters, citations, workflow controls, and image viewer |
| `assets/images/` | Local image assets |
| `assets/files/` | Generated BibTeX and plain-text citations |
| `tools/build-publications.py` | Optional publication updater; standard Python 3.9+ only |
| `PAPER-ASSETS.md` | Per-record inventory of PDF, DOI, and figure availability |
| `404.html` and `site-marker.json` | Error page and project-path recovery |

Navigation and footers are present in every HTML file. Update each page when changing shared links. The error page embeds the stylesheet so it works at missing nested URLs; keep its `<style>` block in sync when changing the theme.

## Add a PDF, DOI, or paper figure

1. Put paper PDFs in `assets/papers/` and figure images in `assets/images/papers/`, creating the folders as needed. Use filename-safe names, for example `capacitive-sensor-paper.pdf` and `capacitive-sensor-figure.webp`.
2. Find the matching record in `data/publications.json` and edit its asset fields:

   ```json
   {
     "pdf_url": "assets/papers/capacitive-sensor-paper.pdf",
     "pdf_label": "Paper PDF",
     "doi": "10.xxxx/your-verified-doi",
     "figure": "assets/images/papers/capacitive-sensor-figure.webp",
     "figure_caption": "Figure 3. Experimental sensor arrangement. Briefly describe the actual image.",
     "figure_source": "assets/papers/capacitive-sensor-paper.pdf#page=4"
   }
   ```

   This is an illustrative field fragment, not a complete publication record. Use the paper's actual DOI; leave an unavailable field as an empty string. URLs may be HTTPS addresses or relative local paths. Keep the original record ID because Research links use it.

3. From the website folder, run:

   ```sh
   python tools/build-publications.py
   ```

   On Windows, `py tools/build-publications.py` may be appropriate. This updates the static publication records, year options, and both citation downloads. It is an editing utility; GitHub Pages does not need to run Python.

4. Commit the changed HTML, JSON, downloads, and assets to your repository. The separate companion preview does not automatically update when source files change.

To add a publication, duplicate a complete JSON record, use a unique `id`, and edit its metadata. Supported `kind` values are `journal`, `preprint`, `conference`, `presentation`, and `thesis`. Keep `citation` consistent with the authors, title, year, venue, and DOI. Numeric years are strings such as `"2026"`; an undated preprint can use `"Preprint"`.

The displayed links are **Paper PDF** (or **Slides PDF**), **DOI**, and **Copy citation**. A presentation's associated article DOI is labeled **Paper DOI**. Missing PDFs use **Request PDF**, addressed to the PI; unavailable DOI information is labeled **DOI not listed**. This static site has no upload form or administrative backend.

## Content and image notes

- The exact brand is **iMAS Lab**: lowercase **i**, uppercase **MAS**.
- Projects and their navigation links have been removed. The homepage no longer includes a funded-project feature or selected-publication list.
- People no longer includes graduate-research or degree-year/thesis-title sections. Thesis records remain on Publications.
- Contact uses **Emmanuel.ogunniyi@sjsu.edu**.
- The manufacturing hero is original AI-generated concept artwork showing robotic additive manufacturing, embedded sensing, and a digital twin. It is not a photograph of lab equipment or an experimental result.
- The supplied PI portrait is unchanged.
- The publication collection retains the supplied record IDs. Public author/publisher sources were checked for PDF links, DOIs, and bibliographic corrections, including the published 2026 status of the local eigenvalue modification paper.
- There are seven inline publication visuals: six images hosted on the coauthor's university website and one locally included experimental image from the accompanying thin-wall printing presentation. Source links appear beneath each image. A failed remote thumbnail falls back to a source link.
- Other records link to figures within the source PDF where available. Two records still need an exact PDF: the data-fusion review preprint (`j9`) and the 2025 invited talk (`i1`). `PAPER-ASSETS.md` lists the remaining inline-figure gaps.
- Figure captions distinguish a paper preview from a presentation extract. The original scientific figures and portrait retain their existing ownership and rights. Full third-party papers are linked, not bundled.

Image sources and the hero prompt are documented in `assets/images/IMAGE-SOURCES.txt`.

## Accessibility and verification

The site includes semantic page structure, a skip link, keyboard focus indicators, labeled controls, mobile navigation, image alternatives, native figure/citation dialogs, and reduced-motion support. Contact links open the visitor's email application; the site does not send messages or collect form submissions.

The update was checked for local page/asset links, publication data consistency, JavaScript syntax, filtering, citation handling, figure controls, and preview routing. Automated checks do not substitute for visual browser review; browser rendering was not available in the editing environment.
