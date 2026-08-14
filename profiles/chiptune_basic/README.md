# Chiptune Basic Profile

This is a **generic, non-platform-specific scaffold** for chip-inspired rendering.

It exists so composition, project data and future renderers have a stable place to meet. It is not a NES, Game Boy, C64, POKEY, SID or other real-hardware profile.

## Intended use

Use this profile for early experiments where the project needs an explicit limited voice layout but does not yet claim hardware accuracy.

The profile deliberately separates:

- abstract voice slots;
- musical role assignment;
- synthesis implementation;
- renderer/backend mapping.

Renderer mappings are intentionally unresolved until a future agent implements and validates them.

## Upgrade path

Future platform-specific profiles should live beside this directory, for example:

```text
profiles/<validated_platform_profile>/
  README.md
  profile.json
  provenance.md
```

A real-platform profile should document where hardware constraints came from and should not inherit generic assumptions silently.
