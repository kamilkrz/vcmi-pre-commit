# vcmi-pre-commit

Pre-commit hooks for validating VCMI mod JSON files.

## Overview

This repository provides a pre-commit hook to check the correctness and consistency of `.json` files for VCMI mods. It ensures that required fields are present and that versioning in the changelog matches the main version field.

## Hook: `mods`

- **ID:** `mods`
- **Description:** Checks `.json` files for required fields and version consistency.
- **Language:** Python
- **Entry Point:** `mod_check_version`
- **Supported file types:** JSON

## What it checks

- Presence of the `version` field.
- Presence and structure of the `changelog` field.
- Ensures the `version` field matches the highest version in the changelog.
- Ensures no undocumented versions are present.

## Usage

### 1. Add to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/your/repo
  rev: 0.0.1  # Use the appropriate tag or commit
  hooks:
    - id: check_json_files