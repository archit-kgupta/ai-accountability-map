"""Builds charts and a filterable evidence map from submissions.csv."""
import json
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PUBLISHED = 82  # written evidence items published on the committee's inquiry page
OUT = Path("docs")
OUT.mkdir(exist_ok=True)
df = pd.read_csv("submissions.csv", dtype=str).fillna("")
df = df[df["primary_accountable"] != ""]  # only rows you have coded
if df.empty:
    raise SystemExit("No coded rows yet: fill primary_accountable for at least one submission.")


def barh(data, title, xlabel, path, **kw):
    ax = data.plot.barh(figsize=kw.pop("figsize", (8, 4.5)), **kw)
    ax.set_xlabel(xlabel); ax.set_ylabel(""); ax.set_title(title)
    if ax.get_legend():
        ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
    plt.tight_layout(); plt.savefig(OUT / path, dpi=150); plt.close()


# 1. Who submitted
barh(df["actor_type"].value_counts().sort_values(), "Submissions by type of actor",
     "Submissions", "by_actor.png", color="#4C6A92", figsize=(7, 4))

# 2. Where each actor type places accountability
table = pd.crosstab(df["actor_type"], df["primary_accountable"])
barh(table, "Who should be accountable, by actor type", "Submissions",
     "accountability_by_actor.png", stacked=True, colormap="tab10")

# 3. Are current rules enough?
order = [c for c in ["Yes", "Partly", "No", "Not stated"] if c in set(df["current_rules_enough"])]
rules = pd.crosstab(df["actor_type"], df["current_rules_enough"])[order]
barh(rules, "Are existing financial rules enough?", "Submissions", "rules_enough.png",
     stacked=True, color={"Yes": "#3B8E5A", "Partly": "#E0B040", "No": "#C0504D", "Not stated": "#B0B0B0"})

# 4. How seriously is accountability addressed?
barh(df["depth"].value_counts(), "How much each submission discusses accountability",
     "Submissions", "depth.png", color="#8A6D3B", figsize=(6, 2.5))

table.to_csv(OUT / "accountability_by_actor.csv")
print(f"{len(df)} of {PUBLISHED} published submissions coded\n")
print(df["primary_accountable"].value_counts(), "\n")
print(df["current_rules_enough"].value_counts(), "\n")

# 5. Filterable evidence map (GitHub Pages serves docs/index.html)
rows = df.to_dict(orient="records")
filters = {c: sorted(df[c].unique()) for c in
           ["actor_type", "primary_accountable", "current_rules_enough", "depth"]}
labels = {"actor_type": "Actor type", "primary_accountable": "Primary accountable",
          "current_rules_enough": "Rules enough?", "depth": "Depth"}
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI Accountability Evidence Map</title>
<style>
body{{font-family:system-ui,sans-serif;max-width:1100px;margin:auto;padding:16px;color:#1f2933;line-height:1.45}}
.filters{{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:12px}}
.filters label{{display:flex;flex-direction:column;font-size:13px;font-weight:600}}
select{{margin-top:4px;padding:4px;font-size:14px}}
.scroll{{overflow-x:auto}} table{{border-collapse:collapse;width:100%;min-width:760px;font-size:14px}}
th,td{{border-bottom:1px solid #ddd;padding:6px;text-align:left;vertical-align:top}} th{{background:#f3f4f6}}
.muted{{color:#5f6b7a;font-size:13px}} img{{max-width:100%;margin:8px 0}}
</style></head><body>
<h1>Who should be accountable for AI decisions in UK finance?</h1>
<p>An evidence map of written submissions to the House of Commons Treasury Committee's inquiry into
<a href="https://committees.parliament.uk/work/8901/ai-in-financial-services/publications/written-evidence/">AI in financial services</a>
(launched February 2025; report published January 2026). Coded by Archit Gupta (University of Bristol) as an independent project alongside his undergraduate dissertation.
<strong>{len(df)} of the {PUBLISHED} published submissions coded so far.</strong>
Codes follow codebook.md in this project's GitHub repository.</p>
<img src="accountability_by_actor.png" alt="Bar chart of who each actor type says should be accountable">
<img src="rules_enough.png" alt="Bar chart of whether each actor type says existing rules are enough">
<img src="depth.png" alt="Bar chart of how much each submission discusses accountability">
<h2>Browse the submissions</h2>
<div class="filters" id="f"></div>
<p class="muted" id="count"></p>
<div class="scroll"><table><thead><tr><th>Ref</th><th>Submitter</th><th>Actor</th><th>Primary / secondary accountable</th>
<th>Rules enough?</th><th>Depth / evidence</th><th>Argument, quote and notes</th></tr></thead><tbody id="t"></tbody></table></div>
<script>
const rows={json.dumps(rows)}, filters={json.dumps(filters)}, labels={json.dumps(labels)}, sel={{}};
const esc=s=>String(s).replace(/[&<>"]/g,c=>({{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}}[c]));
const f=document.getElementById('f');
for(const [k,vals] of Object.entries(filters)){{
  const l=document.createElement('label'); l.textContent=labels[k];
  const s=document.createElement('select');
  s.innerHTML='<option value="">All</option>'+vals.map(v=>`<option>${{esc(v)}}</option>`).join('');
  s.onchange=()=>{{sel[k]=s.value;draw()}}; l.append(s); f.append(l);
}}
function draw(){{
  const hit=rows.filter(r=>Object.entries(sel).every(([k,v])=>!v||r[k]===v));
  document.getElementById('count').textContent=`Showing ${{hit.length}} of ${{rows.length}} coded submissions`;
  document.getElementById('t').innerHTML=hit.length?hit.map(r=>
   `<tr><td>${{esc(r.id)}}</td><td><a href="${{esc(r.url)}}">${{esc(r.submitter)}}</a></td><td>${{esc(r.actor_type)}}</td>
    <td>${{esc(r.primary_accountable)}}${{r.secondary_accountable?'<br><span class="muted">then '+esc(r.secondary_accountable)+'</span>':''}}</td>
    <td>${{esc(r.current_rules_enough)}}</td><td>${{esc(r.depth)}}<br><span class="muted">${{esc(r.evidence)}} evidence</span></td>
    <td>${{esc(r.key_argument)}}<br><em>“${{esc(r.quote)}}”</em>${{r.notes?'<br><span class="muted">'+esc(r.notes)+'</span>':''}}</td></tr>`).join('')
   :'<tr><td colspan="7">No submissions match these filters.</td></tr>';
}}
draw();
</script></body></html>"""
(OUT / "index.html").write_text(page, encoding="utf-8")
print("Wrote docs/index.html and charts")
