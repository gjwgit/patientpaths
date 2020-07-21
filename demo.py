# -*- coding: utf-8 -*-
#
# Time-stamp: <Tuesday 2020-07-21 20:31:15 AEST Graham Williams>
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

mlcat("Patient Pathways", """\
Runs a model of care algorithm to identify outcomes from a configured health 
care system. The input to the model consists of N cohorts (e.g., age groups, 
gender, socio-economic, etc.). What the cohort is does not really matter.

For each cohort the daily presentations of patients in that cohort 
(i.e., the number of patients arriving each day to the health facility) 
is provided as input. These are split into mild and severe cases.
""")

#----------------------------------------------------------------------
# Setup
#----------------------------------------------------------------------

# Import the required libraries.

import re

import numpy as np

from pandas       import read_excel
from patientpaths import outcomes_for_moc

mlcat("", f"""\
The other set of inputs are the proportion of the population in the
ACT jurisdiction ({round(100*426.7/25359.7)}%), the number of beds in ICU (22),
the number of beds in wards (448), the number of beds in the emergency
deprtment (202), and the total number of GPs (2,607).
""")

fname = "cohorts4_daily36.xlsx"
mild   = np.asarray(read_excel(fname, sheet_name="mild", header=None).T)
severe = np.asarray(read_excel(fname, sheet_name="severe", header=None).T)

risk = np.array([0, 2, 2, 0])

cohorts = mild.shape[0]
days = mild.shape[1]

mlcat("", f"""\
Thus a spreadsheet of daily presentations is loaded in this demo,
having two tabs, one for the mild presentations and another for the
severe presentations. Each column corresponds to a cohort and each row is
a successive day.

From the dataset we see there are {cohorts} cohorts and presentations are
provided for {days} days (that's {cohorts*days*2} numbers).

Each cohort is also identified as at risk or not. For this example cohorts 2 and 3
are considered at risk.
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

