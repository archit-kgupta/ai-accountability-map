"""Builds charts and a filterable evidence map from submissions.csv and oral_evidence.csv.

Research question: How do organisations giving evidence to the UK Treasury Committee's
2025-26 inquiry into AI in financial services construct accountability for regulated
firms' AI-assisted decisions?
"""
import json
from html import escape
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PUBLISHED = 82  # written evidence items published on the committee's inquiry page
OUT = Path(".")  # GitHub Pages serves index.html and the charts from the repository root

INDUSTRY = "Industry"
PUBLIC = "Public authorities"
INDEPENDENT = "Public-interest and independent"
OUTSIDE = "Tech, AI provider or consultancy (outside core groups)"
GROUPS = [INDUSTRY, PUBLIC, INDEPENDENT]

# actor_type -> actor_group (see codebook.md, "actor_group")
GROUP_OF_TYPE = {
    "Bank": INDUSTRY, "Insurer": INDUSTRY, "Asset manager": INDUSTRY, "Industry body": INDUSTRY,
    "Regulator": PUBLIC, "Government": PUBLIC,
    "Academic": INDEPENDENT, "Consumer body": INDEPENDENT, "Civil society": INDEPENDENT,
    "Think tank": INDEPENDENT, "Trade union": INDEPENDENT,
    "Tech provider": OUTSIDE, "Professional services": OUTSIDE, "Law firm": OUTSIDE,
    "Other": OUTSIDE,
}
# Boundary cases decided by submitter rather than by actor_type (documented in codebook.md)
GROUP_OVERRIDE = {"AIFS0048": INDUSTRY}  # Mastercard: payment network, grouped with FS firms


def actor_group(row):
    return GROUP_OVERRIDE.get(row["id"], GROUP_OF_TYPE.get(row["actor_type"], OUTSIDE))


all_rows = pd.read_csv("submissions.csv", dtype=str).fillna("")
all_rows["actor_group"] = all_rows.apply(actor_group, axis=1)
cols = [c for c in all_rows.columns if c not in ("actor_group", "url")] + ["actor_group", "url"]
all_rows[cols].to_csv("submissions.csv", index=False)  # keep the derived field in the data file

df = all_rows[all_rows["primary_accountable"] != ""]  # only rows you have coded
if df.empty:
    raise SystemExit("No coded rows yet: fill primary_accountable for at least one submission.")
core = df[df["actor_group"].isin(GROUPS)]
n_outside = len(df) - len(core)
oral = pd.read_csv("oral_evidence.csv", dtype=str).fillna("")


def barh(data, title, xlabel, path, **kw):
    ax = data.plot.barh(figsize=kw.pop("figsize", (8, 4)), **kw)
    ax.set_xlabel(xlabel); ax.set_ylabel(""); ax.set_title(title)
    if ax.get_legend():
        ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
    plt.tight_layout(); plt.savefig(OUT / path, dpi=150); plt.close()


def by_group(col):
    t = pd.crosstab(core["actor_group"], core[col])
    return t.reindex([g for g in GROUPS if g in t.index][::-1])


# 1. Who submitted (all coded rows, by group; tech/consultancy shown separately)
barh(df["actor_group"].value_counts().reindex(GROUPS + [OUTSIDE]).dropna()[::-1],
     "Coded submissions by actor group", "Submissions", "by_actor.png", color="#4C6A92", figsize=(8, 3))

# 2. Where each group places accountability
table = by_group("primary_accountable")
barh(table, "Who should be accountable, by actor group", "Submissions",
     "accountability_by_actor.png", stacked=True, colormap="tab10")

# 3. Are current rules enough?
order = [c for c in ["Yes", "Partly", "No", "Not stated"] if c in set(core["current_rules_enough"])]
rules = by_group("current_rules_enough")[order]
barh(rules, "Are existing financial rules enough? (by actor group)", "Submissions", "rules_enough.png",
     stacked=True, color={"Yes": "#3B8E5A", "Partly": "#E0B040", "No": "#C0504D", "Not stated": "#B0B0B0"})

# 4. How seriously is accountability addressed?
barh(by_group("depth"), "How much each submission discusses accountability", "Submissions",
     "depth.png", stacked=True, color={"Brief": "#C9B48A", "Substantive": "#8A6D3B"}, figsize=(8, 3))

table.to_csv(OUT / "accountability_by_actor.csv")
print(f"{len(df)} of {PUBLISHED} published submissions coded ({n_outside} outside the three core groups)\n")
print(df.groupby("actor_group")["primary_accountable"].value_counts(), "\n")
print(df["current_rules_enough"].value_counts(), "\n")

# 5. Filterable evidence map. Rows are rendered into the HTML so the table is never empty;
# the script only hides rows that do not match the filters.
filter_cols = ["actor_group", "actor_type", "primary_accountable", "current_rules_enough", "depth"]
labels = {"actor_group": "Actor group", "actor_type": "Actor type", "primary_accountable": "Primary accountable",
          "current_rules_enough": "Rules enough?", "depth": "Depth"}
filters = {c: sorted(df[c].unique()) for c in filter_cols}
e = lambda s: escape(str(s), quote=True)


def tr(r):
    data = " ".join(f'data-{c.replace("_", "-")}="{e(r[c])}"' for c in filter_cols)
    sec = f'<br><span class="muted">then {e(r["secondary_accountable"])}</span>' if r["secondary_accountable"] else ""
    notes = f'<br><span class="muted">{e(r["notes"])}</span>' if r["notes"] else ""
    return (f'<tr {data}><td>{e(r["id"])}</td><td><a href="{e(r["url"])}">{e(r["submitter"])}</a></td>'
            f'<td>{e(r["actor_group"])}<br><span class="muted">{e(r["actor_type"])}</span></td>'
            f'<td>{e(r["primary_accountable"])}{sec}</td><td>{e(r["current_rules_enough"])}</td>'
            f'<td>{e(r["depth"])}<br><span class="muted">{e(r["evidence"])} evidence</span></td>'
            f'<td>{e(r["key_argument"])}<br><em>“{e(r["quote"])}”</em>{notes}</td></tr>')


def select(c):
    opts = "".join(f'<option value="{e(v)}">{e(v)}</option>' for v in filters[c])
    return f'<label>{e(labels[c])}<select data-col="{c.replace("_", "-")}"><option value="">All</option>{opts}</select></label>'


oral_rows = "".join(
    f'<tr><td>{e(pd.Timestamp(o["session_date"]).strftime("%-d %B %Y"))}</td><td>{e(o["witness_organisations"])}'
    f'<br><span class="muted">{e(o["witnesses"])}</span></td><td>{e(o["actor_group"])}</td><td>{e(o["questions"])}</td>'
    f'<td><a href="{e(o["transcript_url"])}">Transcript</a></td><td>{e(o["coding_status"])}</td></tr>'
    for o in oral.to_dict(orient="records"))

page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI Accountability Evidence Map</title>
<style>
body{{font-family:system-ui,sans-serif;max-width:1100px;margin:auto;padding:16px;color:#1f2933;background:#fff;line-height:1.45}}
.rq{{font-size:1.1em;border-left:4px solid #4C6A92;padding:4px 12px;margin:12px 0}}
.filters{{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:12px}}
.filters label{{display:flex;flex-direction:column;font-size:13px;font-weight:600;max-width:100%}}
select{{margin-top:4px;padding:4px;font-size:14px;max-width:100%}}
.scroll{{overflow-x:auto}} table{{border-collapse:collapse;width:100%;min-width:760px;font-size:14px}}
th,td{{border-bottom:1px solid #ddd;padding:6px;text-align:left;vertical-align:top}} th{{background:#f3f4f6}}
.muted{{color:#5f6b7a;font-size:13px}} img{{max-width:100%;margin:8px 0}}
</style></head><body>
<h1>How do organisations construct accountability for AI-assisted decisions in UK finance?</h1>
<p class="rq"><strong>Research question:</strong> How do organisations giving evidence to the UK Treasury Committee's
2025–26 inquiry into AI in financial services construct accountability for regulated firms' AI-assisted decisions?</p>
<p>An evidence map of written and oral evidence to the House of Commons Treasury Committee's inquiry into
<a href="https://committees.parliament.uk/work/8901/ai-in-financial-services/">AI in financial services</a>
(launched February 2025; report HC 684 published January 2026). Coded by Archit Gupta (University of Bristol) as an independent project alongside his undergraduate dissertation.
<strong>{len(df)} of the {PUBLISHED} published written submissions coded so far; the {len(oral)} oral evidence sessions are not yet coded.</strong>
Codes follow codebook.md in this project's GitHub repository.</p>

<h2>Definitions and method</h2>
<ul>
<li><strong>Accountability</strong> follows Bovens (2007, <em>European Law Journal</em> 13(4)): a relationship in which an
<em>actor</em> is answerable to a <em>forum</em>, must explain and justify its conduct, and can face consequences.
The map records to whom each organisation assigns accountability for a regulated firm's AI-assisted decision, and whether it judges existing rules sufficient.</li>
<li><strong>Constructing accountability</strong> means the positions organisations put forward about who is, or should be,
answerable. They are positions in a policy debate, not evidence of practice inside firms.</li>
<li><strong>Coding</strong> uses a framework (deductive) coding scheme: every contribution is coded against fixed, predefined
categories in the codebook, rather than codes emerging from the text.</li>
<li><strong>Actor groups.</strong> Each submitter keeps its original actor type and is also placed in one of three groups:
<em>industry</em> (financial-services firms and trade bodies), <em>public authorities</em> (FCA, Bank of England, HM Treasury) and
<em>public-interest and independent</em> contributors (consumer, civil-society, academic and think tank).
Tech and AI providers and consultancies are outside the SM&amp;CR perimeter, so they form a separate category: they stay in the
table but are left out of the group charts ({n_outside} coded so far). This is a stated limitation.</li>
</ul>

<h2>Written evidence by actor group</h2>
<img src="accountability_by_actor.png" alt="Bar chart of who each actor group says should be accountable">
<img src="rules_enough.png" alt="Bar chart of whether each actor group says existing rules are enough">
<img src="depth.png" alt="Bar chart of how much submissions in each actor group discuss accountability">

<h2>Oral evidence</h2>
<p>The Committee held four oral evidence sessions. They are listed here with links to the official transcripts and have <strong>not yet been coded</strong>.</p>
<div class="scroll"><table><thead><tr><th>Session</th><th>Witnesses</th><th>Actor group</th><th>Questions</th><th>Transcript</th><th>Status</th></tr></thead>
<tbody>{oral_rows}</tbody></table></div>

<h2>Browse the written submissions</h2>
<div class="filters" id="f">{"".join(select(c) for c in filter_cols)}</div>
<p class="muted" id="count">Showing {len(df)} of {len(df)} coded submissions</p>
<div class="scroll"><table><thead><tr><th>Ref</th><th>Submitter</th><th>Actor group / type</th><th>Primary / secondary accountable</th>
<th>Rules enough?</th><th>Depth / evidence</th><th>Argument, quote and notes</th></tr></thead><tbody id="t">
{"".join(tr(r) for r in df.to_dict(orient="records"))}
<tr id="none" hidden><td colspan="7">No submissions match these filters.</td></tr></tbody></table></div>
<script>
const sels=[...document.querySelectorAll('#f select')], rows=[...document.querySelectorAll('#t tr[data-actor-group]')];
function draw(){{
  let n=0;
  for(const r of rows){{const ok=sels.every(s=>!s.value||r.dataset[s.dataset.col.replace(/-(.)/g,(m,c)=>c.toUpperCase())]===s.value); r.hidden=!ok; n+=ok;}}
  document.getElementById('none').hidden=n>0;
  document.getElementById('count').textContent=`Showing ${{n}} of ${{rows.length}} coded submissions`;
}}
sels.forEach(s=>s.addEventListener('change',draw));
</script></body></html>"""
(OUT / "index.html").write_text(page, encoding="utf-8")
print("Wrote index.html and charts")
