import sys
import jstyleson
import re


PASS = 0
FAIL = 1


def parse_version(ver) -> tuple:
    """Parse a version string into a tuple of integers for comparison."""
    return tuple(int(part) for part in re.findall(r'\d+', ver))

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