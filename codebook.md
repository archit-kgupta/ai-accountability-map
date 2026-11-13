# Codebook (v3, 22 Oct 2026)

**Research question:** How do organisations giving evidence to the UK Treasury Committee's 2025–26 inquiry into AI in financial services construct accountability for regulated firms' AI-assisted decisions?

## Definitions and method
- **Accountability** follows Bovens (2007, *European Law Journal* 13(4)): a relationship in which an actor is answerable to a forum, must explain and justify its conduct, and can face consequences. The codes record to whom an organisation assigns accountability for a regulated firm's AI-assisted decision (the actor and forum) and whether it judges existing rules sufficient.
- **Coding approach:** this is a framework (deductive) coding scheme. Every contribution is coded against the fixed, predefined categories below; categories are not derived inductively from the texts. Anything outside the categories goes in notes.
- **Unit of analysis:** one organisation's contribution in one form: a written submission (AIFS code), or its share of an oral evidence session.

Use these exact values so the script can count them. Each rule says when a code applies. If two codes could apply, use the more specific one.

## actor_type
Regulator · Government · Bank · Insurer · Asset manager · Tech provider · Industry body · Professional services · Law firm · Academic · Consumer body · Civil society · Think tank · Trade union · Other

- Consumer body: organisations whose main purpose is representing consumers.
- Civil society: charities and research units working on finance in the public interest.
- Tech provider: tech firms and tech-sector trade bodies.
- Industry body: also covers professional bodies for financial-services practitioners (e.g. Chartered Insurance Institute, Institute and Faculty of Actuaries).
- Other: submitters that fit no other type, e.g. the City of London Corporation and the APPG on Insurance and Financial Services (neither regulates firms), training providers and individuals without an academic affiliation.

## actor_group (derived)
Derived from actor_type by `analyse.py`; do not code it by hand. actor_type is kept as the sub-field.

| actor_group | actor_type values |
|---|---|
| Industry | Bank · Insurer · Asset manager · Industry body (financial-services firms and trade bodies) |
| Public authorities | Regulator · Government (FCA, Bank of England, HM Treasury) |
| Public-interest and independent | Consumer body · Civil society · Academic · Think tank · Trade union |
| Tech, AI provider or consultancy (outside core groups) | Tech provider · Professional services · Law firm · Other |

- Actor type decides the group: every Tech provider, Professional services firm or consultancy goes in the Tech, AI provider or consultancy category, whatever sector it serves.
- Tech and AI providers and consultancies are outside the SM&CR perimeter, so they are a separate category and are left out of the group comparison. Their absence is a stated limitation.

## Oral evidence
The four oral evidence sessions are listed in `oral_evidence.csv` with links to the official transcripts. They are coded with the same categories, one row per organisation per session, once coding starts. Until then, coding_status is "Not yet coded".

## primary_accountable / secondary_accountable
| Code | Use when the submission places accountability for AI-assisted decisions on… |
|---|---|
| Senior manager (named individual) | a specific individual role: a named senior manager or SMF holder, or a single nominated board member or senior person. If the submission offers a choice between an individual and a committee, code Board |
| Board | the board or senior management as a collective |
| Firm | the deploying firm as an institution (its governance, risk management, human oversight) |
| Shared: firm + vendor | firms and AI, data or cloud providers, split along the supply chain |
| Shared: firm + regulator | firms and regulators jointly |
| Vendor | AI, data or cloud providers |
| Regulator | the FCA, PRA, Bank of England or other regulators |
| Government | HM Treasury or government (legislation, clarifying liability) |
| Not stated | no position on who is accountable |

**Decision rules for primary_accountable**
- Code a party only when the submission takes a position (says who is, or should be, responsible, or prescribes what they must do). A description of current practice, such as "firms use AI under human oversight", or an accountability that is only implied, is Not stated.
- Human oversight counts as Firm only when the submission says the deploying firm should keep it. Oversight demanded without naming anyone is Not stated.
- When nearly every recommendation is addressed to regulators, code Regulator, with Firm as secondary if firms carry the duties.
- A critique of SM&CR's focus on one individual is still coded Senior manager (named individual), because that is the locus being argued about; record the critique in notes.
- Pension trustees and trustee boards are coded Board.

**Secondary** is the next party on whom the submission takes a position, using the same test as primary: it says that party is or should be responsible, or prescribes what it must do. Listing a framework among existing rules (for example, citing SM&CR) is not a position. Leave it blank if no second party meets the test.

## current_rules_enough
This covers **financial services regulation** only (SM&CR, Consumer Duty, prudential rules, etc.).

| Code | Rule |
|---|---|
| Yes | Existing rules are adequate; at most, it asks for guidance or clarification on how they apply. A hedged remark that rules may need expanding in future does not change an explicit statement that no new rules are needed |
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

## Change log

13 November 2026: Secondary codes now need a position, not a mention (FCA and FIA recoded blank; CII to Board). Senior manager limited to a specific individual role; individual-or-committee choices coded Board (UKSIF recoded to Board). Actor group follows actor type (Mastercard moved to the Tech category). All 82 rows re-checked against the revised secondary rule, which also changed three further rows: Martins Pereira (AIFS0079) and Sutton & Williams (AIFS0076) secondary to blank, and the Electronic Money Association (AIFS0062) secondary from Vendor to Regulator.
