#!/usr/bin/env python3
"""Rebuild the static publication list, its figure credits, and both citation downloads."""
import json
import re
from html import escape
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
EMAIL = "Emmanuel.ogunniyi@sjsu.edu"
KINDS = {
    "journal": ("Journal", "Journals"),
    "preprint": ("Preprint", "Preprints"),
    "conference": ("Conference", "Conferences"),
    "presentation": ("Presentation", "Presentations"),
    "thesis": ("Thesis", "Theses"),
}


def e(value):
    return escape(str(value), quote=True)


def link(url, label):
    return f'<a href="{e(url)}">{e(label)}</a>'


def figure_markup(record):
    path = record.get("figure")
    if not path:
        return ""
    caption = record["figure_caption"]
    credit = record["figure_credit"]
    source = record["figure_source"]
    return f"""<figure class="publication-figure">
          <a class="figure-open" href="{e(path)}" data-figure="{e(path)}" data-caption="{e(caption)}" data-source="{e(source)}" aria-label="Enlarge figure for {e(record['title'])}">
            <img src="{e(path)}" width="{int(credit['width'])}" height="{int(credit['height'])}" loading="lazy" decoding="async" alt="{e(caption)}">
          </a>
          <p class="figure-load-error" hidden>{link(source, "View figure at source")}</p>
          <figcaption><a href="credits.html#credit-{e(record['id'])}">Figure credit</a></figcaption>
        </figure>"""


def render_record(record):
    title = record["title"]
    pdf = record.get("pdf_url")
    doi = record.get("doi")
    if pdf:
        actions = [link(pdf, record.get("pdf_label") or "Paper PDF")]
    else:
        request = "mailto:" + EMAIL + "?subject=" + quote("PDF request: " + title)
        actions = [link(request, "Request PDF")]
    if doi:
        doi_url = doi if doi.startswith("https://") else "https://doi.org/" + doi
        actions.append(link(doi_url, record.get("doi_label") or "DOI"))
    figure = figure_markup(record)
    if not figure and pdf:
        figure_page = record.get("figure_page")
        source = record.get("figures_url") or (pdf + f"#page={figure_page}" if figure_page else "")
        if source and source != pdf:
            actions.append(link(source, record.get("figures_label") or "View figures"))
    actions.append(f'<button class="copy-citation enhanced" type="button" data-citation="{e(record["citation"])}" aria-label="Copy citation for {e(title)}">Copy citation</button>')
    kind = record["kind"]
    year = str(record["year"])
    return f"""        <article class="publication{'' if figure else ' publication--text'}" id="{e(record['id'])}" data-type="{e(kind)}" data-year="{e(year)}">
          <div class="publication-meta"><span class="year">{e(year) if year.isdigit() else 'Undated'}</span><span class="kind">{e(KINDS[kind][0])}</span></div>
          <div class="publication-details"><h2 class="publication-title">{e(title)}</h2>
            <p class="publication-authors">{e(record['authors'])}</p>
            <p class="publication-venue">{e(record['venue'])}</p>
            <div class="publication-links">{' '.join(actions)}</div>
          </div>{figure}
        </article>"""


def credit_markup(record):
    c = record["figure_credit"]
    copyright_text = e(c.get("copyright", ""))
    reference = c.get("reference", "").split(" https://")[0]
    return f"""        <article class="credit-row" id="credit-{e(record['id'])}">
          <img src="{e(record['figure'])}" width="{int(c['width'])}" height="{int(c['height'])}" loading="lazy" alt="">
          <div><h3>{e(c['title'])}</h3><p>{e(c['author'])}. {copyright_text}</p><p>{e(reference)}</p>
            <p>{e(c['changes'])} {link(record['figure_source'], "Source")} · {link(c['license_url'], c['license'])}</p></div>
        </article>"""


def replace_block(content, marker, markup):
    start = f"<!-- {marker}:START -->"
    end = f"<!-- {marker}:END -->"
    first, divider, rest = content.partition(start)
    if not divider or rest.count(end) != 1 or start in rest:
        raise ValueError(f"Expected one {marker} marker pair")
    return first + start + "\n" + markup + "\n" + end + rest.split(end, 1)[1]


def bib_escape(value):
    return str(value).replace("&", r"\&").replace("%", r"\%").replace("_", r"\_").replace("#", r"\#")


def bibtex(record):
    kind = record["kind"]
    entry_type = {"journal": "article", "conference": "inproceedings", "thesis": "phdthesis" if record["id"] == "t2" else "mastersthesis"}.get(kind, "misc")
    names = record["authors"].replace(", and ", ", ").replace(" and ", ", ").split(",")
    fields = {
        "title": "{" + bib_escape(record["title"]) + "}",
        "author": bib_escape(" and ".join(name.strip() for name in names if name.strip())),
        "note": bib_escape(record["venue"]),
    }
    if str(record["year"]).isdigit():
        fields["year"] = record["year"]
    if kind in ("journal", "conference"):
        fields["journal" if kind == "journal" else "booktitle"] = bib_escape(record["venue"].split(",")[0])
    if kind == "thesis":
        fields["school"] = "University of South Carolina"
    if record.get("doi"):
        fields["doi"] = record["doi"].removeprefix("https://doi.org/")
    if record.get("pdf_url"):
        fields["url"] = record["pdf_url"]
    lines = ",\n".join(f"  {key} = {{{value}}}" for key, value in fields.items())
    return f"@{entry_type}{{imas_{record['id']},\n{lines}\n}}"


def build():
    records = json.loads((ROOT / "data/publications.json").read_text(encoding="utf-8"))
    ids = [r["id"] for r in records]
    if len(set(ids)) != len(ids) or not all(re.fullmatch(r"[a-zA-Z][\w-]*", ident) for ident in ids):
        raise ValueError("Supply a unique HTML anchor ID for every publication")
    for r in records:
        if r.get("figure") and not (r.get("figure_credit") and r.get("figure_source") and r.get("figure_caption")):
            raise ValueError(f"Missing figure attribution for {r['id']}")
    path = ROOT / "publications.html"
    page = replace_block(path.read_text(encoding="utf-8"), "PUBLICATIONS", "\n".join(map(render_record, records)))
    years = sorted({str(r["year"]) for r in records if str(r["year"]).isdigit()}, reverse=True)
    years += sorted({str(r["year"]) for r in records if not str(r["year"]).isdigit()})
    options = '<option value="all">All years</option>' + "".join(f'<option value="{e(y)}">{e(y) if y.isdigit() else "Undated"}</option>' for y in years)
    page, count = re.subn(r'(<select id="publication-year">).*?(</select>)', lambda m: m[1] + options + m[2], page, flags=re.S)
    if count != 1:
        raise ValueError("Year selector is missing")
    filters = [("all", "All records")] + [(key, labels[1]) for key, labels in KINDS.items() if any(r["kind"] == key for r in records)]
    buttons = "".join(f'<button type="button" data-filter="{key}" aria-pressed="{str(key == "all").lower()}">{label}</button>' for key,label in filters)
    page, count = re.subn(r'(<div class="filter-buttons"[^>]*>).*?(</div>)', lambda m: m[1] + buttons + m[2], page, flags=re.S)
    if count != 1:
        raise ValueError("Type filter is missing")
    credits_path = ROOT / "credits.html"
    credits = replace_block(credits_path.read_text(encoding="utf-8"), "PUBLICATION-CREDITS", "\n".join(credit_markup(r) for r in records if r.get("figure")))
    files = ROOT / "assets/files"
    files.mkdir(parents=True, exist_ok=True)
    path.write_text(page, encoding="utf-8")
    credits_path.write_text(credits, encoding="utf-8")
    (files / "imas-publications.bib").write_text("\n\n".join(map(bibtex, records)) + "\n", encoding="utf-8")
    (files / "imas-citations.txt").write_text("iMAS Lab — Publication references\n\n" + "\n\n".join(r["citation"] for r in records) + "\n", encoding="utf-8")
    print(f"Rebuilt {len(records)} publication records, figure credits, and citation downloads.")


if __name__ == "__main__":
    build()
