# -*- coding: utf-8 -*-
# Copyright (C) Duncan Macleod (2020-2021)
#
# This file is part of GWpy.
#
# GWpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# GWpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GWpy.  If not, see <http://www.gnu.org/licenses/>.

"""Tests for :mod:`gwpy.table.io.ligolw`
"""

import pytest

import numpy
from numpy.testing import assert_array_equal

from .. import EventTable
from ...testing.utils import skip_missing_dependency


# -- fixtures -----------------------------------------------------------------

@pytest.fixture()
def llwtable():
    from ligo.lw.lsctables import (New, SnglBurstTable)
    llwtab = New(SnglBurstTable, columns=["peak_frequency", "snr"])
    for i in range(10):
        row = llwtab.RowType()
        row.peak_frequency = float(i)
        row.snr = float(i)
        llwtab.append(row)
    return llwtab


# -- test to_astropy_table() via EventTable conversions -----------------------

@skip_missing_dependency('ligo.lw.lsctables')
def test_to_astropy_table(llwtable):
    tab = EventTable(llwtable)
    assert set(tab.colnames) == {"peak_frequency", "snr"}
    assert_array_equal(tab["snr"], llwtable.getColumnByName("snr"))


@skip_missing_dependency('ligo.lw.lsctables')
def test_to_astropy_table_rename(llwtable):
    tab = EventTable(llwtable, rename={"peak_frequency": "frequency"})
    assert set(tab.colnames) == {"frequency", "snr"}
    assert_array_equal(
        tab["frequency"],
        llwtable.getColumnByName("peak_frequency"),
    )


@skip_missing_dependency('ligo.lw.lsctables')
def test_to_astropy_table_empty():
    from ligo.lw.lsctables import (New, SnglBurstTable)
    llwtable = New(
        SnglBurstTable,
        columns=["peak_time", "peak_time_ns", "ifo"],
    )
    tab = EventTable(llwtable, columns=["peak", "ifo"])
    assert set(tab.colnames) == {"peak", "ifo"}
    assert tab['peak'].dtype.type is numpy.object_
    assert tab['ifo'].dtype.type is numpy.unicode_
