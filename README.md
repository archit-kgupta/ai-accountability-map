# AI Accountability Evidence Map

**Research question:** How do organisations giving evidence to the UK Treasury Committee's 2025–26 inquiry into AI in financial services construct accountability for regulated firms' AI-assisted decisions?

This repository codes the written and oral evidence submitted to the House of Commons Treasury Committee's 2025–26 inquiry into AI in financial services and maps where three actor groups (industry; public authorities; public-interest and independent contributors) place accountability. It is an independent project alongside my undergraduate dissertation at the University of Bristol, which studies the same inquiry.

**Live map:** https://archit-kgupta.github.io/ai-accountability-map/

## Method
- Source: published written evidence and the four oral evidence transcripts on the Treasury Committee website (secondary data). Oral evidence is listed in `oral_evidence.csv` and is not yet coded.
- Accountability follows Bovens (2007, *European Law Journal*): answerability of an actor to a forum.
- Each submission is coded with a framework (deductive) coding scheme ([codebook.md](codebook.md)): actor type and derived actor group, primary and secondary accountable party, and whether existing rules (e.g. SM&CR, Consumer Duty) are judged sufficient.
- Analysis: `analyse.py` (Python, pandas, matplotlib) cross-tabulates the codes and builds the charts and the filterable map in `index.html` (served by GitHub Pages from the repository root). Tech providers and consultancies are a separate category outside the three groups.

## Early findings
All 82 published written submissions are coded (61 in the three core groups, 21 outside them):
- **Institutional, not individual, accountability.** 33 of 82 place primary accountability on the firm as an institution and 27 do not say who is accountable. Only 5 point first to a named senior manager, and two of those (City of London Corporation, Innovate Finance) do so to criticise how the SM&CR concentrates AI risk on one person.
- **Many hands is the recurring worry.** 15 submissions code the AI vendor as primary or secondary, or call accountability shared between firm and vendor. Several say firms carry obligations they cannot enforce on much larger AI providers.
- **Existing rules are broadly accepted by industry.** 12 of 28 industry submissions say existing financial rules are enough and only 1 says no. Among public-interest and independent contributors, 1 says yes and 6 say no.
- **Accountability is rarely central.** 66 of 82 discuss it only briefly.

## Run it
```
pip install pandas matplotlib
python analyse.py
```
