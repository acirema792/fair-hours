# Privacy and fairness

Read this before step 1. These limits are part of the Skill, not options.

## Whose data is touched

- **The named helper only.** Step 4 asks for one known identity by name. Fair Hours never searches strangers, other household members or other visitors.
- **Recording proof without identities.** Step 5 returns event counts and times per camera, with no names, faces, plates or snapshots. It answers "was the camera recording?" and nothing else.
- **Entry cameras only.** The user chooses the cameras that cover the doors. Fair Hours does not use indoor rooms to follow a helper around the home.
- **Snapshots on request.** Step 7 runs only for rows that are not `Confirmed`, only when the user asks, with purpose `user_review`. Snapshots stay on the NAS.
- **No identification from appearance.** A face counts only if the household registered it as a known identity in the surveillance app. Fair Hours cannot register faces and never infers who someone is.

## Notice to the helper

Fair Hours runs only after the user confirms the helper knows the entry cameras exist. If the user says the helper does not know, Fair Hours explains why it stops and makes no camera query. Recording rules for household employees differ by country and state; the household is responsible for its own cameras.

## Fair use of the result

- Differences are counted in both directions and shown side by side. Time the helper worked without billing is listed first in the advice.
- `Inconclusive` is never treated as a missed visit: cameras go offline, people use side doors, and faces are sometimes not recognised.
- The report is a starting point for a conversation with the helper. Fair Hours never sends messages, never contacts an agency and never decides what is owed.

## Where data goes

Everything runs through the NAS's registered experts on the household's own UGREEN AI NAS. Fair Hours calls no external service and sends no data off the device. The report is shown in the chat and saved to a NAS folder only after the user approves the save in the platform approval prompt.
