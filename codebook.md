# Codebook (v3, 22 Oct 2026)

**Research question:** How do organisations giving evidence to the UK Treasury Committee's 2025–26 inquiry into AI in financial services construct accountability for regulated firms' AI-assisted decisions?

## Definitions and method
- **Accountability** follows Bovens (2007, *European Law Journal* 13(4)): a relationship in which an actor is answerable to a forum, must explain and justify its conduct, and can face consequences. The codes record to whom an organisation assigns accountability for a regulated firm's AI-assisted decision (the actor and forum) and whether it judges existing rules sufficient.
- **Coding approach:** this is a framework (deductive) coding scheme. Every contribution is coded against the fixed, predefined categories below; categories are not derived inductively from the texts. Anything outside the categories goes in notes.
- **Unit of analysis:** one organisation's contribution in one form: a written submission (AIFS code), or its share of an oral evidence session.

Use these exact values so the script can count them. Each rule says when a code applies. If two codes could apply, use the more specific one.

## actor_type
Regulator · Bank · Insurer · Asset manager · Tech provider · Industry body · Professional services · Law firm · Academic · Consumer body · Civil society · Trade union · Other

- Consumer body: organisations whose main purpose is representing consumers.
- Civil society: charities and research units working on finance in the public interest.
- Tech provider: tech firms and tech-sector trade bodies.

## actor_group (derived)
Derived from actor_type by `analyse.py`; do not code it by hand. actor_type is kept as the sub-field.

| actor_group | actor_type values |
|---|---|
| Industry | Bank · Insurer · Asset manager · Industry body (financial-services firms and trade bodies) |
| Public authorities | Regulator · Government (FCA, Bank of England, HM Treasury) |
| Public-interest and independent | Consumer body · Civil society · Academic · Think tank · Trade union |
| Tech, AI provider or consultancy (outside core groups) | Tech provider · Professional services · Law firm · Other |

- Boundary case: Mastercard (AIFS0048) keeps actor_type Tech provider but is grouped as Industry (a payment network inside the financial-services perimeter).
- Tech and AI providers and consultancies are outside the SM&CR perimeter, so they are a separate category and are left out of the group comparison. Their absence is a stated limitation.

## Oral evidence
The four oral evidence sessions are listed in `oral_evidence.csv` with links to the official transcripts. They are coded with the same categories, one row per organisation per session, once coding starts. Until then, coding_status is "Not yet coded".

## primary_accountable / secondary_accountable
| Code | Use when the submission places accountability for AI-assisted decisions on… |
|---|---|
| Senior manager (named individual) | a named individual, e.g. a senior manager under SM&CR or a nominated board member or senior person |
| Board | the board or senior management as a collective |
| Firm | the deploying firm as an institution (its governance, risk management, human oversight) |
| Shared: firm + vendor | firms and AI, data or cloud providers, split along the supply chain |
| Shared: firm + regulator | firms and regulators jointly |
| Vendor | AI, data or cloud providers |
| Regulator | the FCA, PRA, Bank of England or other regulators |
| Government | HM Treasury or government (legislation, clarifying liability) |
| Not stated | no position on who is accountable |

**Secondary** is the next party the submission names, usually the one it asks to act (for example, to clarify liability). Leave it blank if there is none.

## current_rules_enough
This covers **financial services regulation** only (SM&CR, Consumer Duty, prudential rules, etc.).

| Code | Rule |
|---|---|
| Yes | Existing rules are adequate; at most, it asks for guidance or clarification on how they apply |
| Partly | Keeps the existing framework, but asks for specific amendments or new requirements within it |
| No | Says the existing framework is inadequate, or calls for AI-specific legislation or a new regime |
| Not stated | No position on financial regulation. A position on other law (e.g. employment law) still counts as Not stated; record it in notes |

## depth
Substantive (accountability is discussed as a topic in its own right) · Brief (mentioned in passing or only implied)

## evidence
Strong (the quote directly states the coded position) · Weak (the quote only implies it, so the code rests on the wider text; explain in notes)

## Quotes
Copy quotes exactly. Mark omissions with "…", put clarifying words in [square brackets], and add [sic] after errors in the original.

## Free-text columns
- key_argument: one sentence, in your own words
- notes: anything a reader needs to judge the code
