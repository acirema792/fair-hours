# Disclosures

## Principal functionality developed for this Hackathon

The whole Skill was written during the UGREEN Hackathon 2026 on AI NAS: the visit-by-visit workflow across five registered experts, the matching rules and their results, the passage rules that separate `Not seen` from `Inconclusive` without naming anyone else, the two-direction totals, the bill arithmetic check, Draft mode, the privacy limits and the report format. No earlier Skill or submission material is reused.

## Third-party components and open source libraries

None. The package contains only original Markdown files: `SKILL.md` and the files in `references/`. It includes no scripts, executables, binaries, manifests, models, datasets or downloaded content.

## Platform capabilities used at run time

The Skill delegates to the experts registered on UGREEN AI NAS (security-monitor-agent, document-agent, photo-agent, file-agent, knowledge-agent) and uses the AI models those experts run on the NAS. The Skill itself calls no external service and sends no data off the device; which chat model Uliya uses to orchestrate it is a Uliya setting outside the Skill.

## AI tools used and their principal uses

- **Claude (Anthropic)**: drafting and editing the Skill text, the matching rules and the documentation, and building the off-device synthetic test bench used to check the rules.
- **UGOS Skill Creation Tool (uliya-skill-kit 0.7.3, from the UGREEN Hackathon Starter Kit)**: the capability catalog used to choose CLIs and experts, and the official static checker. The kit is a development tool only and is not included in this package.

## Status

Independent entry for the UGREEN Hackathon 2026 on AI NAS. Not an official UGREEN Skill.
