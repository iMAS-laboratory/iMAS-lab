# iMAS Lab website

Intelligent Manufacturing and Autonomous Systems Laboratory, Department of Mechanical Engineering, San José State University.

## Preview and publish

Extract the ZIP and open `index.html` in a browser. The six main pages, research images, fonts, and publication filters work locally. Paper PDFs, DOI records, email links, and external profiles open through their respective services.

To update the existing GitHub Pages site, copy the extracted contents into the publishing root of `iMAS-laboratory/iMAS-lab`, with `index.html` at the root. Commit those changes to the branch your repository uses for Pages. The site consists of static files and requires no deployment build.

## Edit content

| File | Content |
| --- | --- |
| `index.html` | Landing page and homepage photograph |
| `research.html` | Six research thrusts, image descriptions, and related-publication links |
| `people.html` | PI profile and graduate and undergraduate research assistant sections |
| `resources.html` | Equipment, facilities, and code repositories |
| `contact.html` | Contact address, student research, and collaborations |
| `data/publications.json` | Citation metadata, paper and figure links, and figure attribution |
| `credits.html` | Photograph and research-figure attributions |
| `assets/images/IMAGE-SOURCES.txt` | Reuse details for the homepage and research images |
| `css/styles.css` and `js/main.js` | Shared design and interactions |

All primary pages contain ordinary HTML. If you change a shared navigation link, update it across the pages. Relative URLs preserve the existing `/iMAS-lab/` address and publication anchors.

### Research assistants and equipment

In `people.html`, insert confirmed profiles inside `graduate-assistants` or `undergraduate-assistants`. In `resources.html`, add confirmed equipment inside the `equipment` section. Both areas accept this short entry format:

```html
<article>
  <h3>Name</h3>
  <p>Degree program and research topic, or equipment model and capability.</p>
</article>
```

### Publications and images

Edit `data/publications.json`, then run `python tools/build-publications.py` (Python 3.9+). The script regenerates the publication list, filters, both citation downloads, and publication-figure credits. Keep each existing record ID so links such as `publications.html#j8` continue to work.

An embedded figure uses a local `figure` path, a descriptive `figure_caption`, a `figure_source` URL, and a `figure_credit` object. For a source-only image, leave `figure` empty and set `figures_url` or `figure_page` to the original figure location. Research images and publication figures each have their own license in Image credits. The institutional marks and supplied portrait retain their respective owners’ rights.
