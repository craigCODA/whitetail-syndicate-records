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

## Access and history

This repository contains private correspondence, cost proposals and interview materials. It has no public site or Pages publishing workflow. Website code remains in its existing source repository. Large original captures have authorized source links and readable extracts here; no Drive location has been fabricated.

Import date: October 9, 2026, America/Chicago. Historical documents keep their original dates and may describe superseded plans. Promotion and film development are excluded from the active completed-work recap at Craig's request.

Keeping these files updated is part of each task. Cross-service collection is not automatically installed merely by creating this repository.
