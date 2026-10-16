# Codebook (v2, 16 Oct 2026)

Use these exact values so the script can count them. Each rule says when a code applies. If two codes could apply, use the more specific one.

## actor_type
Regulator · Bank · Insurer · Asset manager · Tech provider · Industry body · Professional services · Law firm · Academic · Consumer body · Civil society · Trade union · Other

- Consumer body: organisations whose main purpose is representing consumers.
- Civil society: charities and research units working on finance in the public interest.
- Tech provider: tech firms and tech-sector trade bodies.

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
