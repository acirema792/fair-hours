# Privacy and fairness

Read this before step 1. These limits are part of the Skill, not options.

## Whose data is touched

- **The named helper only.** Step 1 confirms the helper's registered name; if the name does not match exactly, only the closest registered names are shown so the user can pick the right one, with no images or details. Step 4 asks for that one known identity. Fair Hours never searches strangers, household members or visitors by name.
- **Passages without identities.** Step 5 returns, for a few dates only, each passage's time, camera and whether the person was recognised (yes or no), with no names, faces, plates or snapshots. Passages answer two questions only: was the camera recording, and could an unrecognised person have been the helper.
- **Entry cameras only.** The user chooses the cameras that cover the doors; a camera that is not at an entrance needs the user's confirmation that it only covers a door. Fair Hours does not use indoor cameras to follow a helper around the home.
- **Snapshots on request.** Step 7 runs only for rows that are not `Confirmed` and have helper events, only when the user asks, with purpose `user_review`. Snapshots stay on the NAS.
- **No identification from appearance.** A face counts only if the household registered it as a known identity. Fair Hours cannot register faces and never infers who someone is. An unrecognised person is never counted for or against the helper.

## Notice to the helper

Fair Hours runs only after the user confirms the helper knows that the entry cameras recognise faces and may be used to check hours. If the user says no, Fair Hours explains why it stops, notes that some places require written consent for this kind of processing, and makes no camera query. The household is responsible for following its local rules on cameras and household employees.

## Fair use of the result

- Differences are counted in both directions and shown side by side. Time the helper worked without billing is mentioned first in the advice.
- Every doubt goes the helper's way: a camera gap, a cut-off list, an unrecognised passage near an arrival or departure, or a name never recognised in the period gives `Inconclusive`, never a missed visit.
- Agreed rounding and minimum-visit terms are applied before any difference is reported.
- The report is a starting point for a conversation with the helper. Fair Hours never sends messages, never contacts an agency and never decides what is owed.

## Where data goes

Fair Hours works only through the experts registered on the household's own UGREEN AI NAS, and the experts use the AI models that run on the NAS. Fair Hours itself calls no external service and sends no data off the device. Which chat model Uliya uses to orchestrate the Skill is a Uliya setting outside the Skill; households that want everything on the device should keep Uliya on its local model. The report is shown in the chat and saved to a NAS folder only after the user approves the save in the platform approval prompt.
