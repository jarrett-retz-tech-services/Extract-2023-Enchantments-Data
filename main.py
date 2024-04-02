import csv
import os
import re

from pypdf import PdfReader

TITLE_TEXT = "Enchantments Lottery 2023 Application Data"

# Text to remove from the PDF
text_to_remove = [TITLE_TEXT]

# Regex pattern that matches any single digit number followed immediately by a letter, excluding forward slashes until the of the line
PATTERN = r"(\d)([A-Za-z]+)(?![/])"

CSV_ZONE_NAMES = [
    "Core,Enchantment,Zone",
    "Colchuck,Zone",
    "Stuart,Zone",
    "Snow,Zone",
    "Stuart,,Zone",
    "Eightmile/Caroline,Zone",
    "Eightmile/Caroline Zone,(stock)",
    "Stuart Zone,(stock)",
]

CSV_COLUMN_NAMES = [
    "Preferred,Entry,Date,1",
    "Preferred,Zone,1",
    "Minimum,Acceptable,Group,Size,1",
    "Maximum,Requested,Group,Size,1",
    "Preferred,Entry,Date,2",
    "Preferred,Zone,2",
    "Minimum,Acceptable,Group,Size,2",
    "Maximum,Requested,Group,Size,2",
    "Preferred,Entry,Date,3",
    "Preferred,Zone,3",
    "Minimum,Acceptable,Group,Size,3",
    "Maximum,Requested,Group,Size,3",
    "Processing,Sequence",
    "Results,Status",
    "Awarded,Preference",
    "Awarded,Entry,Date",
    "Awarded,Entrance,Code/Name",
    "Awarded,Group,Size",
]

# Combine the zone names and column names into single list
CORRECTION_NAMES = CSV_ZONE_NAMES + CSV_COLUMN_NAMES

# File name in local direction
FILE_NAME = "fseprd1162873.pdf"

# Read the PDF file
reader = PdfReader(FILE_NAME)
text = ""

for page in reader.pages:
    page_text = page.extract_text()
    # Remove unwanted text
    for item in text_to_remove:
        page_text = page_text.replace(item, "")

    # Split the awarded group size and the state code with a space
    page_text = re.sub(PATTERN, r"\1 \2", page_text)

    # Separate 0Cancelled and 0Awarded with a space
    page_text = re.sub(r"(\d)(Cancelled|Awarded)", r"\1 \2", page_text)

    # Add the page text to the text variable
    text += page_text + "\n"

# Save text to temporary CSV file
with open("temp.csv", "w", newline="") as file:
    writer = csv.writer(file, quotechar=None)
    writer.writerows(csv.reader(text.splitlines()))

# Open the input file in read mode and output file in write mode
with open("temp.csv", "r") as input_file, open(
    "2023_results_w_pdf_totals.csv", "w"
) as output_file:
    # Read each line from the input file
    for line in input_file:
        # Replace spaces with commas
        line = line.replace(" ", ",")

        # Check for zone names and replace commas with spaces
        for zone_name in CORRECTION_NAMES:
            line = line.replace(zone_name, zone_name.replace(",", " "))

        # Add four commas after Unsuccessful or Cancelled to fill missing cells
        line = re.sub(r"(Unsuccessful|Cancelled)", r"\1,,,,", line)

        # Count the number of commas in the line
        num_commas = line.count(",")

        # Check if the num_commas is less than 18
        if num_commas < 18:
            # Store the number of commas to add to the line
            num_commas_to_add = 18 - num_commas

            # Regex that matches any series of digits followed by a comma and a result status (Unsuccessful, Cancelled, or Awarded)
            # This pattern is used to add before the processing sequence column for missing entry cells
            pattern = r"(\d+),((Unsuccessful|Cancelled|Awarded))"

            # Add the number of commas infront of the series of digits in the line
            line = re.sub(pattern, r"," * num_commas_to_add + r"\1" + "," + r"\2", line)

        # Match the entire row before the 18th comma
        before_comma_pattern = r"^(.*?,){18}"
        # Store everything before the 18th comma in a variable
        before_18th_comma = re.match(before_comma_pattern, line)

        if before_18th_comma:
            before_18th_comma = before_18th_comma.group()

            # Match everything after the 18th comma, keeping everything before the 18th comma and after the 18th comma
            # but substitude the commas after the 18th comma with spaces
            # This pattern is used to collect the "State" column values (some have spaces in them)
            # and replace the commas with spaces so the word is not split into separate columns
            after_comma_pattern = r"^(.*?,){18}(.*)$"
            replacement_after_18th_comma = re.sub(
                after_comma_pattern,
                lambda x: x.group(2).replace(",", " "),
                line,
            )

            # Combine the before and after 18th comma
            line = before_18th_comma + replacement_after_18th_comma

        # Write the modified line to the output file
        output_file.write(line)

# Remove the temporary CSV file
os.remove("temp.csv")
