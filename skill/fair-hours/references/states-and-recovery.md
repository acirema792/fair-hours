# States and recovery

Every delegation ends in one of five public states. Use a step's business result only after `completed`.

| Step | `completed` | `failed` or `cancelled` | `waiting_user` | `waiting_approval` |
|---|---|---|---|---|
| 1 Camera check | Match the named entry cameras; ask if none match | Stop: the comparison needs the camera list. Say what failed. | Relay the question, wait, resume step 1 | Not expected for a read step; report the state and wait |
| 2 Find the bill | One file: use it. Several: ask. No results: offer typed hours or Draft mode | Offer typed hours or Draft mode; never search other folders | Relay, wait, resume | Not expected; report and wait |
| 3 Read the bill | Use only values printed on the bill | Offer typed hours or Draft mode; no visits are invented | Relay, wait, resume | Not expected; report and wait |
| 4 Helper events | Continue, including with an empty list | Stop the comparison: without helper events every result would be a guess | Relay, wait, resume | Not expected; report and wait |
| 5 Recording proof | Apply rules 5 and 6 | Rows that need it become `Inconclusive` with "recording not confirmed"; the rest stands | Relay, wait, resume | Not expected; report and wait |
| 7 Evidence | Show the snapshot references for review on the NAS | Say the snapshots could not be loaded; the report is unchanged | Relay, wait, resume | Not expected; report and wait |
| 8 Save | Report the saved file only when verified is true and an output file is returned | Say the report was not saved; it is still in the chat | Relay, wait, resume | Tell the user the save is waiting in the NAS approval prompt; report nothing as saved yet |

## Partial work

If the run stops partway, say which steps completed, which did not, and what the user can do next. Never present a partial comparison as a full report: label it "partial" and list the missing steps.

## Retrying

Retry a failed read step once only if the user asks. Never retry step 8 on your own: a second save could create a duplicate file.
