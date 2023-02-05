from pathlib import Path

import numpy as np
import pytest
from numpy.testing import assert_array_equal, assert_equal, assert_raises

from cvrplib.read import read_instance

from .._utils import CVRPLIB_DATA_DIR, LKH_3_DATA_DIR, selected_cases


@pytest.mark.parametrize("instance_format", ["CVRPLIB", "LKH", "VRP"])
def test_raise_unknown_instance_format(tmp_path, instance_format):
    """
    Tests if a ValueError is raised when an unknown instance format is passed.
    """
    path = tmp_path / "tmp.txt"
    path.write_text("test")

    with assert_raises(ValueError):
        read_instance(path, instance_format)


instances = [
    (
        CVRPLIB_DATA_DIR / "X-n101-k25.vrp",
        {
            "name": "X-n101-k25",
            "type": "CVRP",
            "dimension": 101,
            "capacity": 206,
        },
        {
            "node_coord": [365, 689],
            "demand": 0,
            "depot": 0,
        },
    ),
    (
        CVRPLIB_DATA_DIR / "tai75a.vrp",
        {
            "name": "Tai75a",
            "type": "CVRP",
            "dimension": 76,
            "capacity": 1445,
            "edge_weight_type": "EUC_2D",
        },
        {
            "node_coord": [0, 0],
            "demand": 0,
            "depot": 0,
        },
    ),
]


@pytest.mark.parametrize("path, specifications, sections", instances)
def test_read_instance_vrplib(path, specifications, sections):
    instance = read_instance(path)

    for k, v in specifications.items():
        assert_equal(instance[k], v)

    for k, v in sections.items():
        if np.isscalar(instance[k]):
            assert_equal(instance[k], v)
        else:
            # Always test for first element in data arrays
            assert_array_equal(instance[k][0], v)


@pytest.mark.parametrize("case", selected_cases())
def test_read(case):
    """
    Read the case and verify a subest its attributes.
    """
    instance = read_instance(case.instance_path, "vrplib")

    assert_equal(instance["name"], case.instance_name)
    assert_equal(instance["dimension"], case.dimension)
    assert_equal(instance["capacity"], case.capacity)


def test_C101():
    instance = read_instance(CVRPLIB_DATA_DIR / "C101.txt", "solomon")
    N = 100

    assert_equal(instance["name"], "C101")
    assert_equal(instance["vehicles"], 25)
    assert_equal(instance["capacity"], 200)
    assert_equal(instance["node_coord"][N], [55, 85])
    assert_equal(instance["demand"][N], 20)
    assert_equal(instance["service_time"][N], 90)
    assert_equal(instance["time_window"][N], [647, 726])


@pytest.mark.parametrize(
    "path", Path(LKH_3_DATA_DIR).glob("*/INSTANCES/*vrp*")
)
def test_lkh_3_vrplib(path):
    """
    TODO Test for instance values
    """
    read_instance(path)


@pytest.mark.parametrize("path", Path("data/euro-neurips/").glob("*.txt"))
def test_euro_neurips_vrplib(path):
    """
    TODO Test for instance values
    """
    read_instance(path)
