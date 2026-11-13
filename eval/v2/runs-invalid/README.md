# Invalid runs (kept for the record)

`skill-mockbug/`: first v2 Skill run set (31 cases). Invalid because of a bench bug, not a Skill bug: the v2 mock
routed by keyword and matched the word "faces" in the camera-list instruction ("Do not return faces, plates or
snapshots"), so the camera list came back as a face-match answer. The Skill then correctly refused to guess camera
names, which ended many runs early. Fixed in mock_delegate.py (route on the exact `ug-surveillance <action>`), and
test_mocks.py now sends every SKILL.md delegate template through the mock before any run. All 31 cases were re-run.
Score of this invalid set, for transparency: 16/25 main + 3/6 blind cases; 0 false Not seen, 0 false Confirmed.
