# Documentation map

This is the index of every document under `docs/`. Each file has exactly one
role; find the row that matches your question instead of searching everything.

| Question | Where |
|---|---|
| Where are we, what is next | [project/HANDOFF.md](project/HANDOFF.md) — read whole |
| What is still to do, known debt | [project/ROADMAP.md](project/ROADMAP.md) |
| What changed in each version, and why | [project/CHANGELOG.md](project/CHANGELOG.md) |
| How the system is designed, what not to break | [project/ARCHITECTURE.md](project/ARCHITECTURE.md) |

<!--
The four rows below point at directories (decisions/, guides/, features/,
archive/) that a small project may not have yet — see "Scaling to project
size" in the docs-and-versioning skill. Delete a row if you haven't created
its directory; a link to a directory that doesn't exist is a broken link
like any other. Add it back the first time that directory earns its keep.

| Why a specific decision went the way it did | [decisions/](decisions/) |
| How to do a recurring task in this repo | [guides/](guides/) |
| How an external consumer uses this project | [features/](features/) |
| What happened in a finished initiative | [archive/](archive/) |
-->

<!--
Add one row per file/directory below the table as the project grows past the
starter set above. Keep each hook to one line — the point of this file is
that someone can scan it in ten seconds and know where to go, not read a
description here instead of the doc itself.

Example additions:
| How to add a new module | [guides/NEW_MODULE.md](guides/NEW_MODULE.md) |
| Why we chose X over Y for auth | [decisions/AUTH_APPROACH.md](decisions/AUTH_APPROACH.md) |
-->

## Writing a new doc here

Every file (except this one) opens with a role banner:

```
> **Role:** <what question this file answers> · **Audience:** <who reads it>
```

Pick the directory whose description above matches the question your new
content answers — not the file that happens to be open. Then add a row to
this table. A file that isn't listed here is a file nobody will find, which
means nobody will keep it accurate.
