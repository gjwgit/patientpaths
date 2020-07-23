# -*- coding: utf-8 -*-
#
# Time-stamp: <Thursday 2020-07-23 14:48:52 AEST Graham Williams>
#
# Copyright (c) Togaware Pty Ltd. All rights reserved.
# Licensed under the GPLv3
# Author: Graham.Williams@togaware.com
#
# ml demo patientpaths
#
# This demo is based on:
#
# https://github.com/anu-act-health-covid19-support/patientpaths

from mlhub.pkg import mlask, mlcat, mlpreview
from mlhub.utils import get_cmd_cwd

mlcat("Patient Pathways", """\
Runs a model of care algorithm to identify outcomes from a configured health
care system. The input to the model consists of N cohorts (e.g., age groups,
gender, socio-economic, etc.). What the cohort is does not really matter.

For each cohort the daily presentations of patients in that cohort
(i.e., the number of patients arriving each day to the health facility)
is provided as input. These are split into mild and severe cases.

For this demo a spreadsheet of daily presentations is loaded. The spreadsheet
has two workbooks (tabs), one for the mild presentations and another for the
severe presentations. Each column corresponds to a cohort and each row is
a successive day. No headers are used in the spreadsheet.
""")

#----------------------------------------------------------------------
# Setup
#----------------------------------------------------------------------

# Import the required libraries.

import os
import re
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pandas       import read_excel
from patientpaths import outcomes_for_moc

#-----------------------------------------------------------------------
# Read from Spreadsheet
#-----------------------------------------------------------------------

fname = "cohorts4_daily36.xlsx"
mild   = np.asarray(read_excel(fname, sheet_name="mild", header=None).T)
severe = np.asarray(read_excel(fname, sheet_name="severe", header=None).T)

mlcat("", f"""\
The other set of inputs (currently hard-coded) are the proportion
of the population in the ACT jurisdiction ({round(100*426.7/25359.7)}%),
the number of beds in ICU (22),
the number of beds in wards (448), the number of beds in the emergency
department (202), and the total number of GPs (2,607).
""")

risk = np.array([0, 2, 2, 0])

cohorts = mild.shape[0]
days = mild.shape[1]

mlcat("", f"""\
With {cohorts} cohorts and daily presentations
for {days} days we have, over the mild/severe cases,
{cohorts*days*2} inputs.

Each cohort is also identified as at risk or not. For this example cohorts 2 and 3
are considered at risk (the risk vector is 0,2,2,0, and interpreted as Boolean ">1"
though probably better to actually use Booleans in the code).
""")

outcomes = outcomes_for_moc("cohort", mild, severe, risk)
keys = re.sub(r", ([^,]*)$", ", and \\1", ", ".join(list(outcomes.keys())))

mlask(end="\n")


mlcat("Model of Care", f"""\
The model of care is run to calculate the outcomes. The outcomes are reported for:
{keys}.
""")

outcome = "deaths"

mlcat("", f"""\
The first set of outcomes reports the expected {outcome.upper()} per day per cohort.
""")

print("  " + "\t  ".join([str(i) for i in range(1, cohorts + 1)]) + "   TOTAL")
print("-" * (cohorts*8) + "---")
for i in range(days):
    print("\t".join([str(a) for a in list(outcomes[outcome][i].round(decimals=1))])
          + f"\t{round(outcomes[outcome][i].sum(), 1)}")
print("-" * (cohorts*8) + "---")

mlask(True, True)

#-----------------------------------------------------------------------
# Save to Spreadsheet
#-----------------------------------------------------------------------

fname = "results.xlsx"

mlcat("Saving to Spreadsheet", f"""\
The results can be saved to a spreadsheet '{fname}' with a workbook (tab) for each of the
measures listed above. From this spreadsheet it is straightforward for spreadsheet jockeys
to create any required plots.
""")

sys.stdout.write("Do you want to save the results [y/N]? ")
choice = input().lower().strip()

if choice in ("y", "yes"):
    with pd.ExcelWriter(os.path.join(get_cmd_cwd(), fname)) as writer:
        for k in list(outcomes.keys()):
            df = pd.DataFrame(outcomes[k])
            df.to_excel(writer, sheet_name=k, header=False, index=False)
print()

#-----------------------------------------------------------------------
# Plot
#-----------------------------------------------------------------------

measure = "deaths"

mlcat("Generating Plots", f"""\
Pltos can be created from the input and output datasets.
As a simple example we plot the Expected Daily {measure.capitalize()}

Type Ctrl-W to close the plot.
""")
            
ds = np.asarray(outcomes[measure]).T
plt.figure(figsize=(10,5))
for i in range(len(ds)): 
    plt.plot(ds[i], label=1+i)
plt.legend(title="Cohorts")
plt.title(f"Expected Daily {measure.capitalize()}")
plt.show()

mlask(end=True)
