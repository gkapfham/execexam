import json
import re
import requests


def update_coverage_badge():
    # Load the coverage.json file
    try:
        with open("coverage.json") as f:
            data = json.load(f)
            print("Loaded coverage.json successfully.")
    except FileNotFoundError:
        print("Error: coverage.json file not found. Run your tests first.")
        return

    # Extract total coverage percentage
    try:
        total_coverage = data["totals"]["percent_covered_display"]
        print(f"Total coverage found: {total_coverage}%")
    except KeyError:
        print("Error: Unable to find the total coverage in the report.")
        return

    # Ensure coverage is formatted properly as an integer
    total_coverage = int(float(total_coverage))

    # Determine the color based on the coverage percentage
    if total_coverage >= 90:
        color = "brightgreen"
    elif total_coverage >= 75:
        color = "yellow"
    elif total_coverage >= 50:
        color = "orange"
    else:
        color = "red"

    print(f"Coverage color set to: {color}")

    # Generate the badge markdown with dynamic color
    badge = f"![Coverage](https://img.shields.io/badge/coverage-{total_coverage}%25-{color})"
    print(f"Generated badge: {badge}")

    # Read the README.md and update the badge
    try:
        with open("README.md", "r+") as f:
            content = f.read()
            if re.search(
                r"!\[Coverage\]\(https://img.shields.io/badge/coverage-[0-9]+%25-[a-z]+\)",
                content,
            ):
                print("Existing badge found, updating...")
                new_content = re.sub(
                    r"!\[Coverage\]\(https://img.shields.io/badge/coverage-[0-9]+%25-[a-z]+\)",
                    badge,
                    content,
                )
                f.seek(0)
                f.write(new_content)
                f.truncate()
                print("README.md updated successfully.")
            else:
                print(
                    "No existing badge found, please ensure it's in the correct format."
                )
    except FileNotFoundError:
        print("Error: README.md file not found.")
        return


if __name__ == "__main__":
    update_coverage_badge()


# Path to your local JSON file from Open Source Insights
json_file_path = "version.json"

# Load the JSON data from the file
with open(json_file_path, "r") as f:
    data = json.load(f)

# Extract the latest version from the JSON data
# Adjust this depending on the structure of your JSON file
latest_version = data["info"]["version"]  # Modify this if necessary
print(f"Latest version: {latest_version}")

# Now create/update the badge using Shields.io
badge_url = f"https://img.shields.io/badge/version-{latest_version}-blue.svg"

# Download the badge and save it locally (optional)
badge_response = requests.get(badge_url)
if badge_response.status_code == 200:
    with open("version-badge.svg", "wb") as f:
        f.write(badge_response.content)
    print("Badge updated successfully!")
else:
    print("Error fetching badge from Shields.io.")
