# AI Accountability Evidence Map

Who do regulators, banks, tech providers, academics and consumer groups say should be accountable for AI-assisted decisions in UK financial services?

This repository codes the written evidence submitted to the House of Commons Treasury Committee's 2025–26 inquiry into AI in financial services and maps where each type of actor places responsibility. It is an independent project alongside my undergraduate dissertation at the University of Bristol, which studies the same inquiry.

**Live map:** https://archit-kgupta.github.io/ai-accountability-map/

## Method
- Source: published written evidence on the Treasury Committee website (secondary data).
- Each submission is coded against a fixed codebook ([codebook.md](codebook.md)): actor type, primary and secondary accountable party, and whether existing rules (e.g. SM&CR, Consumer Duty) are judged sufficient.
- Analysis: `analyse.py` (Python, pandas, matplotlib) cross-tabulates the codes and builds the charts and the filterable map in `docs/`.

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
