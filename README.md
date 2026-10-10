# Whitetail Syndicate — Project Records

A private working record for Craig Ramos, Kraig Fussell and Lori. It records what was done, how it was done, the materials used, where the result was used, and what remains open.

## Start here

1. Read [agent instructions](AGENTS.md).
2. Read [current status](STATUS.md) and [work recap](records/work-recap.md).
3. Use the [material directory](records/material-directory.md) to find evidence.
4. Read the guide in the relevant work area before continuing a task.

| Area | Contents and process |
| --- | --- |
| [Interviews and stories](interviews/README.md) | Questions, permission materials, story sources and participant records |
| [Product audit](product-audit/README.md) | Catalog evidence, original Product Control app, offline review, pricing proposals |
| [Outreach](outreach/README.md) | Contact backgrounds, actual correspondence snapshots, reply status, sending policy |
| [Website](website/README.md) | Source repository, implementation record, forms and deployment status |
| [Launch research](launch-research/README.md) | Research process and historical review documents |
| [Artwork](artwork/README.md) | Placement guidance, artwork inventory and actual-product references |
| [Records](records/README.md) | Sources, decisions, dated activity, billing and historical work evidence |

## Add or update material

The [hours and payments trial](records/billing/README.md) records time and receipts separately and generates [the current report](records/billing/summary.md). It is being tested on `trial/hours-payments` before adoption on main.

Save the material in the appropriate area, then register how it was created and used:

```bash
python3 scripts/record_material.py interviews/nathan-deville/new-notes.md --area interviews --title "Nathan follow-up notes" --status source --how "Notes from the follow-up conversation" --used-for "Factual review of the story" --source "Participant follow-up on the actual date"
python3 scripts/refresh_inventory.py
python3 scripts/validate_records.py
```

Update the area's guide/status and records/decisions.md when a decision changes. Commit the records with the work. The activity log preserves prior entries.

## When an agent is asked about status, billing, or completeness

Answer from the records only. Do not improve, defend, or soften the documentation. Follow [the evidence standards](records/evidence-standards.md) and use [the billing provenance table](records/billing/provenance.md) to locate supporting material.

1. State what is currently due or accrued, with the exact figures and date the balance is confirmed through. Identify any later confirmed entries separately from the opening balance.
2. For each major line item or work area, identify the strongest evidence currently in the repository and its class: operator-confirmed itemization, dated original artifact, reported-but-materials-not-attached, retrospective estimate, or open/missing. Label inference explicitly.
3. Explicitly separate work that is billed or accrued, work that is described but whose source material is not yet attached, and historical effort estimates that are not billing amounts.
4. Note any place where the record does not convert an estimate, preview, reply, or reported completion into a stronger claim of payment, live deployment, owner approval, or attached source.
5. List open items that would change the picture if attached, without treating their absence as proof the work did not occur.

Reply in plain language to the user. Prefer “the records show” and “the records do not yet contain” over evaluative language about the quality of the documentation.

## Access and history

This repository contains private correspondence, cost proposals and interview materials. It has no public site or Pages publishing workflow. Website code remains in its existing source repository. Large original captures have authorized source links and readable extracts here; no Drive location has been fabricated.

Import date: October 9, 2026, America/Chicago. Historical documents keep their original dates and may describe superseded plans. Promotion and film development are excluded from the active completed-work recap at Craig's request.

Keeping these files updated is part of each task. Cross-service collection is not automatically installed merely by creating this repository.
