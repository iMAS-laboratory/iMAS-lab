#!/usr/bin/env python3
"""Update the static publication page and downloads from data/publications.json.

No packages required. Run from any directory: python tools/build-publications.py
"""
from pathlib import Path
from html import escape
from urllib.parse import quote
import json,re

ROOT=Path(__file__).resolve().parents[1]
EMAIL='Emmanuel.ogunniyi@sjsu.edu'
def e(value): return escape(str(value),quote=True)
def anchor(url,label,classes='paper-action'):
    return f'<a class="{classes}" href="{e(url)}" target="_blank" rel="noopener">{label}</a>'

def render_record(p):
    ident=p['id'];title=p['title'];figure=p.get('figure','');pdf=p.get('pdf_url','');doi=p.get('doi','')
    source=p.get('figure_source') or pdf or p.get('source_url','')
    caption=p.get('figure_caption') or 'Research figure from the source publication.'
    visual=''
    if figure:
        visual=f'''<figure class="publication-figure"><a class="figure-open" href="{e(figure)}" data-figure="{e(figure)}" data-caption="{e(caption)}" data-source="{e(source)}" aria-label="Enlarge research figure for {e(title)}" target="_blank" rel="noopener"><img src="{e(figure)}" width="640" height="420" alt="{e(caption)}" loading="lazy" decoding="async"><span class="figure-open-label">Enlarge figure</span></a><p class="figure-load-error" hidden>Figure preview is unavailable. {anchor(source or figure,'View at source','')}</p><figcaption>{e(caption)} {anchor(source or figure,'Source','')}</figcaption></figure>'''
    if pdf:
        pdf_link=anchor(pdf,e(p.get('pdf_label') or 'Paper PDF'),'paper-action primary')
    else:
        request='mailto:'+EMAIL+'?subject='+quote('PDF request: '+title)
        pdf_link=f'<a class="paper-action primary" href="{e(request)}">Request PDF</a>'
    if doi:
        doi_link=anchor(doi if doi.startswith('https://') else 'https://doi.org/'+doi,e(p.get('doi_label') or 'DOI'))
    else:doi_link='<span class="paper-action-disabled">DOI not listed</span>'
    note=''
    if not figure:
        if pdf:
            figures_url=pdf+(f'#page={p["figure_page"]}' if p.get('figure_page') else '')
            note='<p class="figure-note">'+anchor(figures_url,'View figures in the PDF','')+'</p>'
        else:note='<p class="figure-note">Paper and figure available by request.</p>'
    return f'''<!-- Publication {e(ident)}: edit PDF, DOI, and figure in data/publications.json. -->
<article class="publication{' publication--text' if not figure else ''}" id="{e(ident)}" data-type="{e(p['kind'])}" data-year="{e(p['year'])}">{visual}<div class="publication-details"><div class="publication-meta"><span class="year">{e(p['year']) if str(p['year']).isdigit() else 'Undated'}</span><span class="kind">{e(p['kind'].capitalize())}</span></div><h2 class="publication-title">{e(title)}</h2><p class="publication-authors">{e(p['authors'])}</p><p class="publication-venue">{e(p['venue'])}</p><div class="publication-links">{pdf_link}{doi_link}<button class="copy-citation enhanced" type="button" data-citation="{e(p['citation'])}" aria-label="Copy citation for {e(title)}">Copy citation</button></div>{note}</div></article>'''

def bib_escape(value):
    return str(value).replace('\\',r'\textbackslash{}').replace('&',r'\&').replace('%',r'\%').replace('_',r'\_').replace('#',r'\#')

def build():
    records=json.loads((ROOT/'data/publications.json').read_text())
    if len({p['id'] for p in records}) != len(records):raise ValueError('Publication IDs must be unique.')
    path=ROOT/'publications.html';content=path.read_text()
    rendered='<!-- PUBLICATIONS:START -->\n'+'\n'.join(render_record(p) for p in records)+'\n<!-- PUBLICATIONS:END -->'
    content,n=re.subn(r'<!-- PUBLICATIONS:START -->.*?<!-- PUBLICATIONS:END -->',lambda _:rendered,content,flags=re.S)
    if n!=1:raise ValueError('Expected one publication-list marker pair.')
    years=sorted({str(p['year']) for p in records if str(p['year']).isdigit()},reverse=True)
    options='<option value="all">All years</option>'+''.join(f'<option value="{y}">{y}</option>' for y in years)
    if any(p['year']=='Preprint' for p in records):options+='<option value="Preprint">Undated preprints</option>'
    content=re.sub(r'(<select id="publication-year">).*?(</select>)',lambda m:m[1]+options+m[2],content,flags=re.S)
    path.write_text(content)
    bibliography=['% iMAS Lab publication references. Source links are recorded in data/publications.json.']
    for p in records:
        kind={'journal':'article','conference':'inproceedings','thesis':'phdthesis' if p['id']=='t2' else 'mastersthesis'}.get(p['kind'],'misc')
        authors=' and '.join(x.strip() for x in p['authors'].replace(', and ',', ').replace(' and ',', ').split(',') if x.strip())
        fields={'title':'{'+p['title']+'}','author':authors,'note':p['venue']}
        if str(p['year']).isdigit():fields['year']=p['year']
        if p['kind']=='journal':fields['journal']=p['venue'].split(',')[0]
        if p['kind']=='conference':fields['booktitle']=p['venue'].split(',')[0]
        if p['kind']=='thesis':fields['school']='University of South Carolina'
        if p.get('doi'):fields['doi']=p['doi'].removeprefix('https://doi.org/')
        if p.get('pdf_url'):fields['url']=p['pdf_url']
        bibliography.append('@'+kind+'{imas_'+p['id']+',\n'+',\n'.join('  '+k+' = {'+bib_escape(v)+'}' for k,v in fields.items())+'\n}')
    (ROOT/'assets/files/imas-publications.bib').write_text('\n\n'.join(bibliography)+'\n')
    (ROOT/'assets/files/imas-citations.txt').write_text('iMAS Lab — Publication references\n\n'+'\n\n'.join(p['citation'] for p in records)+'\n')
    print('Publication page and citation downloads updated.')

if __name__=='__main__':build()
