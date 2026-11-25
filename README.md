# Graduate voter outreach

I built this for a candidate in my family who was contesting a graduates' constituency of the Maharashtra Legislative Council. In that election the voters are registered graduates. The constituency here covers five districts: Kolhapur, Sangli, Pune, Solapur, and Satara.

The campaign had one month and a small group of helpers. The rolls were public PDFs on a government site, one part after another, in English and Marathi. Helpers had been visiting without a map of who was actually on the roll, or where a single stop would reach the most people.

I turned those PDFs into one visit list: who is still eligible, which village to go to first, and what the graduates in that place studied and how old they are. Using that route, the campaign received about 50% more votes than it had expected.

The pages below are the aggregate picture. Names, addresses, and voter ID numbers stay off this repository.

## What I built

Four steps. The first three run on a laptop. The last one runs in Google Colab, because the cleaned workbook is large.

1. **`collect_en_pdfs.py`** copies the English roll PDFs (`*_EN.pdf`) out of the district zip into one folder. Marathi PDFs are a second copy of the same parts, so they are skipped. Running it again does not duplicate files.
2. **`pdfs_to_excel.py`** reads every English PDF with pdfplumber and writes one row per voter. It keeps the roll columns (name, relative, address, qualification, occupation, age, gender, EPIC) and adds the district, part, page, and file. A name marked shifted, deleted, expired, or crossed out with a line is labelled, so it does not go on the walking list. PDFs are read in batches of 40. If the job stops, run it again: finished batches are kept and skipped.
3. **`clean_addresses.py`** collapses repeated place names and writes the address in title case.

   `AMBA, AMBA, AMBA, Shahuwadi, KOLHAPUR, 415101` becomes `Amba, Shahuwadi, Kolhapur, 415101`.

4. **`electoral_rolls_to_excel.ipynb`** splits each address into locality, village, taluka, district, and pincode. It groups messy degree spellings (a B.Ed written as `beed` or `techer` still counts as education), flags duplicates, and writes `outreach_analysis.xlsx`.

The visit list is every voter still marked active, with same-file duplicates removed. The workbook has nine sheets:

| Sheet | What the team used it for |
|---|---|
| Outreach_List | Names and addresses to visit. Biggest villages are at the top. |
| Village_Plan | Which village a team should take. Includes women, voters aged 21–35, teachers, and farmers. |
| Taluka_Plan | Which taluka to schedule on which day. |
| Part_Plan | Booth / part numbers, for dividing one village among helpers. |
| Qualification_Mix | Degree groups, so the conversation can differ. |
| Age_Gender | Where younger voters and women are concentrated. |
| Occupation_Mix | Farmer, teacher, engineer, and the rest. |
| Shifted_Followup | People marked shifted. Look them up in the new part, not at the old address. |
| Data_Quality | Missing age, pincode, or qualification, checked before trusting a total. |

On disk this was **746 English PDFs** and **394,603 rows**.

## Who was actually worth a visit

![Rows read from the rolls, and the list left after shifted, deleted, and duplicate names were removed](images/district-outreach-summary.png)

| District | Received | Shifted | Deleted | Duplicate extras (same file) | Final outreach |
|---|---:|---:|---:|---:|---:|
| Kolhapur | 116,580 | 1,374 | 644 | 1,877 | 112,685 |
| Sangli | 90,238 | 2 | 2,167 | 1,102 | 86,967 |
| Pune | 88,363 | 124 | 37 | 649 | 87,553 |
| Solapur | 49,904 | 53 | 130 | 651 | 49,070 |
| Satara | 49,518 | 1,880 | 219 | 252 | 47,167 |
| **Total** | **394,603** | **3,433** | **3,197** | **4,531** | **383,442** |

Final outreach is the received rows minus shifted, deleted, and same-file duplicates. That removed **11,161 names (2.8%)**. As a percentage it looks small. As a walking plan it is a lot of doors: a moved voter, a deleted name, or the same person printed twice.

Three districts hold the month. Kolhapur, Pune, and Sangli together are **287,205 people, 74.9%** of the visit list. Kolhapur alone is 29.4%.

Two districts needed a different kind of attention:

- **Sangli** had 2,167 of the 3,197 deletions, about two thirds. Those names had to come off the Sangli route.
- **Satara** had 1,880 of the 3,433 shifts, more than half. Those voters were followed up in the part they had moved to, which is what `Shifted_Followup` is for.

## Where one visit reached the most people

The visit list is sorted so the largest village is first. A helper who starts at the top covers more graduates per stop, then keeps moving down the same list for the rest of the month.

![Fifteen villages where one visit reaches the most graduates](images/top-15-villages.png)

| Village | Taluka | District | Eligible voters | Aged 21–35 |
|---|---|---|---:|---:|
| Ichalkaranji | Hatkanangle | Kolhapur | 4,655 | 2,224 |
| Islampur | Walwa | Sangli | 3,145 | 1,473 |
| Kundal | Palus | Sangli | 2,662 | 1,507 |
| Vita | Khanapur | Sangli | 2,508 | 1,428 |
| Tasgaon | | Sangli | 1,394 | 660 |
| Jaysingpur | Shirol | Kolhapur | 1,271 | 506 |
| Baramati | | Pune | 1,233 | 507 |
| Hupari | Hatkanangle | Kolhapur | 1,013 | 616 |
| Murgud | Kagal | Kolhapur | 997 | 476 |
| Sangola | Sangole | Solapur | 947 | 401 |
| Gargoti | Bhudargad | Kolhapur | 925 | 376 |
| Kagal | | Kolhapur | 905 | 448 |
| Palus | | Sangli | 837 | 445 |
| Ashta | Walwa | Sangli | 781 | 371 |
| Borgaon | Walwa | Sangli | 726 | 415 |

Ichalkaranji is the best single stop, at 4,655 graduates, and it is still about 1% of the roll. The top 15 together are **23,999 people, 6.3%** of the visit list. The ranking is the order of the stops: start at Ichalkaranji, then keep moving down the list for the rest of the month. In Kundal and Vita, more than half of those graduates are 35 or under.

Tasgaon, Baramati, Kagal, and Palus have a blank taluka in the table. The address on the roll did not include one. The town name was still right, which is why they appear on the chart with empty parentheses.

The largest talukas on the plan, where a whole day could be booked, were:

| Taluka | District | Eligible voters | Women | Aged 21–35 |
|---|---|---:|---:|---:|
| Walwa | Sangli | 20,375 | 37.3% | 54.3% |
| Hatkanangle | Kolhapur | 19,921 | 36.3% | 52.9% |
| Kagal | Kolhapur | 15,478 | 33.2% | 56.0% |
| Haveli | Pune | 14,766 | 42.1% | 35.9% |
| Palus | Sangli | 14,562 | 39.4% | 54.9% |
| Karvir | Kolhapur | 14,550 | 34.7% | 54.9% |

These six are **99,652 voters**, a quarter of the list. Walwa and Hatkanangle are both large and young. Haveli is large and older, with a higher share of women. The taluka column is only this clean at the top. Further down, a locality or a peth sometimes landed in the taluka slot because that is where it sat in the address. Scheduling used the village ranking for the actual stop.

## Who the voters are

![Eligible voters by qualification group](images/voters-by-qualification.png)

| Qualification | Eligible voters | Share |
|---|---:|---:|
| Arts | 149,416 | 39.0% |
| Commerce | 66,129 | 17.2% |
| Science | 66,046 | 17.2% |
| Engineering | 47,233 | 12.3% |
| Education (B.Ed / M.Ed) | 15,017 | 3.9% |
| Other / unclear | 11,359 | 3.0% |
| Medical / pharma | 10,521 | 2.7% |
| Graduate, subject not specified | 8,199 | 2.1% |
| Diploma | 4,197 | 1.1% |
| PhD | 2,159 | 0.6% |
| Missing | 1,675 | 0.4% |
| Law | 1,491 | 0.4% |

Arts, commerce, science, and engineering are **328,824 people, 85.8%** of the visit list. The conversation at most doors was with a general graduate. Teachers were a smaller group and still worth a separate pass: one teacher talks to a lot of families. The degree field shows **15,017** education graduates. The occupation field shows **30,174** people recorded as teachers, many of them with an Arts degree rather than a B.Ed.

Age on the visit list:

| Age | Women | Men | Voters | Share |
|---|---:|---:|---:|---:|
| 25 and under | 12,810 | 16,185 | 28,995 | 7.6% |
| 26–30 | 32,718 | 54,750 | 87,477 | 22.8% |
| 31–35 | 26,892 | 48,023 | 74,917 | 19.5% |
| 36–40 | 21,420 | 37,104 | 58,528 | 15.3% |
| 41–50 | 25,493 | 50,780 | 76,279 | 19.9% |
| 51–60 | 9,239 | 32,978 | 42,217 | 11.0% |
| 61–70 | 1,492 | 9,565 | 11,057 | 2.9% |
| Over 70 | 353 | 3,617 | 3,970 | 1.0% |

**191,389 people, half the list, are 35 or under.** The single largest band is 26–30. Women are 130,417 of the visit list (34.0%), and that share is higher in the younger bands: about 44% at 25 and under, and about 9% over 70. A route aimed at younger graduates also reached more women graduates. Twenty-two rows have no gender and two have no age, so in a few bands the women and men columns sit slightly under the voter total.

The occupation cell on the roll was the word "Other" for 295,653 people (77%). Degree and age were the reliable way to describe a town. Where a real job was written, the usable counts were teachers (30,174), farmers (21,009), engineers (13,054), government service (10,107), business (7,280), and doctors (3,168). Farmers change the kind of stop: a field visit, not only a door in town.

## What the campaign changed

Before this, helpers chose where to go from memory. After it, they had four concrete changes in how the month was spent:

- They walked an ordered list of **383,442** eligible people, starting where one stop reached the most graduates.
- **11,161** shifted, deleted, or duplicate names were not visited.
- People marked shifted were looked up in the new part. In Satara that was most of the moved voters.
- The pitch could follow the room. Most doors were Arts, commerce, science, or engineering graduates. Teachers, farmers, and the 26–35 age band were visible town by town, so a helper knew which of those groups they were about to meet.

The campaign received about **50% more votes than it had expected.**

## What I learned

- A government PDF is a layout. Pulling 394,603 rows out of 746 files meant reading the ruled tables, skipping the column-number header, and noticing a line drawn through a name.
- Status is part of the data. A shifted or deleted line still looks like a voter until the mark is parsed. Leaving those names in would have sent helpers to the wrong door for a month.
- Addresses in these rolls repeat the village on purpose. Cleaning is "keep each place once, in the order it was written," then read from the right: pincode, district, taluka, village.
- Free-text degrees only become useful after the spellings are grouped. `beed`, `techer`, `btec`, and `B.E.` have to land in a bucket before a bar chart can change a conversation.
- With one month and a few people, the product is a sort order. The question is which stop reaches the most graduates, then the next one, then the next one.
- Batches and checkpoints matter at this size. A failed PDF should not throw away the files already read.
- The public story is the totals. The personal records stay local.

## Limits

A few things in the output need a person, not a blind total.

- The English tables left the EPIC cell empty on **303,083** visit-list rows (79%). Duplicates are detected from the part number, the name, and gender, because the voter ID usually was not there. Where an EPIC was present and shared by more than one row, **2,994** rows are flagged.
- **5,536** visit-list rows (1.4%) may be the same person in more than one part of the same district. They stay on the list and are marked for someone to check. They were not deleted automatically.
- Part numbers start again in each district, and the within-part duplicate key does not include the district. A small share of the 4,531 "duplicate extras" can be two different people who share a part number and a similar name.
- Grouping addresses produced about **97,000** place rows. Many addresses never shared a village name with the next house, so those groups stayed small. The towns at the top of the chart are where the same village name occurred thousands of times. That top is what got scheduled. The long tail still needs the street address.
- **11,359** qualifications (3%) stayed in Other / unclear. The notebook prints the raw spellings so another keyword can be added.
- Age was missing on 1 row, the pincode on 1 row, and gender on 22 rows. One hundred ages fell under 21 or over 100.

## What is not in this repository

The rolls are public, and they are still personal data: full name, father's or husband's name, address, age, gender, and EPIC number. This repo has the code and the three aggregate pictures above.

Kept on the machine, and ignored by git:

- the district zip and the 746 English PDFs (`all_together/`)
- `all_english_voters.xlsx` and `all_english_voters_cleaned.xlsx`
- `outreach_analysis.xlsx`, including `Outreach_List` and `Shifted_Followup`

Before the first commit, `git status` should show the Python, the notebook, `requirements.txt`, and `images/`. It should not show a `.xlsx`, a `.pdf`, or a `.zip`. If the notebook is run again, clear its outputs before committing. A printed slice of the visit list would contain names.

## Project files

```
.
├── README.md
├── requirements.txt
├── collect_en_pdfs.py              # English PDFs out of the zip
├── pdfs_to_excel.py                # one row per voter, with status
├── clean_addresses.py              # repeated place names removed
├── electoral_rolls_to_excel.ipynb  # village ranking and outreach workbook
└── images/
    ├── district-outreach-summary.png
    ├── top-15-villages.png
    └── voters-by-qualification.png
```

## How to run

The zip of roll PDFs has to sit next to the scripts. The default name in `collect_en_pdfs.py` is `496_without.zip`. Pass another path if yours is different.

```powershell
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt

python collect_en_pdfs.py
python pdfs_to_excel.py
python clean_addresses.py
```

`pdfs_to_excel.py` reads every page. Expect it to take a long time. If it stops, run the same command again.

Then upload `electoral_rolls_output/all_english_voters_cleaned.xlsx` to Google Drive and run `electoral_rolls_to_excel.ipynb` from the top. The notebook looks for:

`MyDrive/electoral_rolls_output/all_english_voters_cleaned.xlsx`

It writes `outreach_analysis.xlsx` next to that file. The charts in this README are the two plots from the notebook, plus the district summary of the visit list.
