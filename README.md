# README.md

## Introduction

Recently, I investigated the 2021 and 2022 Enchantments Lottery data published on the USFS website to calculate probabilities of winning given your application selections. I wanted to test out some common advice and discover if the advice was true.

Analyzing the data for 2021 and 2022 was fairly straightforward because data for those years is available on the USFS website in a data-friendly format (.xlsx, .csv). Unfortunately, they provide the 2023 application data in the Portable Document Format (.pdf). I requested the data in similar formats to previous years but after not hearing back I decided to extract the data myself.

This article is a brief overview of that process using Python.

## The Program

I knew there were libraries for extracting text from PDF files but I didn't know there was such a variety. I tried textract, but ran into problems immediately. After reading a few SO posts, I tried pypdf and it worked immediately.

### Source Code

The steps in the program are simple:

- Extract the text from the pdf file (fseprd1162873.pdf)
- Make corrections or format the text for CSV storage
- Store the text data in a temporary CSV document
- Read the temporary file
- Make corrections to the data by adding cells and combining cells that should be one data cell (i.e., "British,Columbia" -> "British Columbia")
- Save the modified CSV data to a new CSV file

I ran into a series of problems when parsing the text for CSV storage.

### Difficulties

First, not all spaces are replaceable with a comma because some data points in the file have spaces (i.e., "Core Enchantment Zone" or "British Columbia").

Second, some of the data that should be in separate cells is parsed as one cell (i.e., "2Awarded" should be "2,Awarded" denoting the group size and awarded status).

Finally, and the most complex when parsing the data, no value appears for an "empty" cell. Applicants are only required to enter one application entry option, but they're allowed to apply for three different options. Therefore, some application rows had fewer cells than other full rows. This same problem manifested between awarded and unsuccessful permits. The awarded permits had awarded permit data (i.e., awarded group size), but all the unsuccessful permits had no such data.

### PDF Statistic Totals

The USFS, or someone else, put the awarded permit totals broken down by zone near the top of the PDF file next to the first ten rows. What that meant was ~99.75% of this pdf is normal, but ten rows that are not.

Instead of writing custom code to remove those data rows, I decided that I would go into the document after parsing and remove them which is what I did.

## Conclusion

I'm appreciative that the USFS provides the Enchantments lottery data on their website. I think it's interesting and fun to look at. The 2023 data has new columns ("Processing Sequence" and "State") which makes this year's data even more exciting.

Now, I'm eagerly anticipating the 2024 results.
