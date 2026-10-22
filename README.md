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
20 of the 82 published submissions coded so far:
- **Institutional, not individual, accountability.** 11 of 20 place accountability on the firm as an institution. Only one asks for a named individual to be responsible, and even the FCA lists the Senior Managers and Certification Regime as one framework among several.
- **Existing rules are broadly accepted.** 7 say existing financial rules are enough, 7 say partly, 4 take no position and 2 say no. Both "no" positions come from academics; no industry body says no.
- **Accountability is rarely central.** 15 of 20 discuss it only briefly.

## Run it
```
pip install pandas matplotlib
python analyse.py
```
