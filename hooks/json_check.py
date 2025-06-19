import sys
import jstyleson
import re


PASS = 0
FAIL = 1


def parse_version(ver) -> tuple:
    """
    Parse a version string into a tuple of up to 3 integers (major, minor, patch) for comparison.
    Raises ValueError if the version is not in the form X.Y or X.Y.Z with only non-negative integers (no leading zeroes).
    """
    # Match only valid versions: 1.2, 1.2.3, etc. No leading zeroes, only digits and dots.
    if not re.fullmatch(r'(0|[1-9]\d*)(\.(0|[1-9]\d*)){1,2}', ver):
        raise ValueError(
            f"Invalid version format: '{ver}'. Must be in the form X.Y or X.Y.Z with no leading zeroes."
        )
    parts = ver.split('.')
    # Only take up to the first 3 parts (major, minor, patch)
    return tuple(int(part) for part in parts[:3])

def validate_version_field(json_data) -> None:
    """Validate that the JSON data contains a 'version' field."""
    if "version" not in json_data:
        raise ValueError("Missing 'version' field")

def validate_changelog_field(json_data) -> None:
    """Validate that the JSON data contains a 'changelog' field."""
    if "changelog" not in json_data or not isinstance(json_data["changelog"], dict):
        raise ValueError("Does not have a valid 'changelog' field")

def validate_mod_ver(json_data) -> None:
    """Validate the 'version' field against the 'changelog' field."""
    if "changelog" in json_data and isinstance(json_data["changelog"], dict):
        changelog_versions = list(json_data["changelog"].keys())
        highest_changelog_version = max(changelog_versions, key=parse_version)
        mod_version = json_data["version"]
        if parse_version(mod_version) < parse_version(highest_changelog_version):
            raise ValueError(
                f"Version mismatch: 'version' is {mod_version}, but changelog contains higher version {highest_changelog_version}"
            )
        if parse_version(mod_version) > parse_version(highest_changelog_version) and mod_version not in changelog_versions:
            raise ValueError(
                f"Version {mod_version} is newer than any version documented in changelog"
            )

def main() -> int:  
    exit_code = PASS
    files = sys.argv[1:]
    for path in files:
        path_str = str(path)
        try:
            with open(path_str, "r") as file:
                json_data = jstyleson.load(file)
                if file.name.endswith("mod.json"):
                    validate_version_field(json_data)
                    validate_mod_ver(json_data)
                    if file.name == "mod.json":
                        validate_changelog_field(json_data)
                print(f"✅ {path_str}")
        except Exception as exc:
            print(f"❌ {path_str}: {exc}")
            exit_code = FAIL
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())