# VRPLIB
[![PyPI version](https://badge.fury.io/py/vrplib.svg)](https://badge.fury.io/py/vrplib)
[![vrplib](https://github.com/leonlan/vrplib/actions/workflows/vrplib.yaml/badge.svg)](https://github.com/leonlan/vrplib/actions/workflows/vrplib.yaml)
[![codecov](https://codecov.io/gh/leonlan/VRPLIB/branch/master/graph/badge.svg?token=X0X66LBNZ7)](https://codecov.io/gh/leonlan/VRPLIB)

`vrplib` is a Python package for reading Vehicle Routing Problem (VRP) instances. It currently supports:
- reading VRPLIB and Solomon instances and solutions, and
- downloading instances and best known solutions from [CVRPLIB](http://vrp.atd-lab.inf.puc-rio.br/index.php/en/).

# Installation
This library works with Python 3.8+ and only depends on `numpy`. Install the latest version of `vrplib`:

```shell
pip install vrplib
```

# Example usage
## Reading VRPLIB instances and solutions
```{python, prompt=TRUE}
import vrplib

instance = vrplib.read_instance("/path/to/X-n101-k25.vrp")
solution = vrplib.read_solution("/path/to/X-n101-k25.sol")

instance.keys()
dict_keys(['name', 'comment', 'type', 'dimension', 'edge_weight_type', 'capacity', 'node_coord', 'demand', 'depot', 'edge_weight'])

solutions.keys()
dict_keys(['routes', 'cost'])
```


## Reading Solomon instances and solutions
``` python
instance = vrplib.read_instance("/path/to/C101.txt", instance_format="solomon")
solution = vrplib.read_solution("/path/to/C101.sol") # only VRPLIB solution format


```

## Downloading instances from CVRPLIB 
``` python
import vrplib

instance = vrplib.download_instance("X-n101-k25.vrp")
solution = vrplib.download_solution("X-n101-k25.sol")

# List instance names that can be downloaded 
vrplib.list_names()                      # All instance names
vrplib.list_names(low=100, high=200)     # Instances with between [100, 200] customers
vrplib.list_names(vrp_type='cvrp')       # Only CVRP instances
vrplib.list_names(vrp_type='vrptw')      # Only VRPTW instances
```


# Notes
This section contains additional notes about the `vrplib` package.

## Instance formats
`vrplib` currently supports the two VRP instance formats:
- **VRPLIB**: this format is most commonly used for Capacitated Vehicle Routing Problem (CVRP) instances.  See the [X-n101-k25](http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/X/X-n101-k25.vrp) instance for an example. VRPLIB is an extension of the TSPLIB95 format. Additional information about this format can be found [here](  http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp95.pdf) and [here]( http://webhotel4.ruc.dk/~keld/research/LKH-3/LKH-3_REPORT.pdf). 
- **Solomon**: this format was used to introduce the Solomon instances [1] for the Vehicle Routing Problem with Time Window (VRPTW) and also the Homberger and Gehring [2] instances. See the [C101](http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/Solomon/C101.txt) instance for an example.

## How instances are parsed
`vrplib` parses an instance and returns a dictionary of keyword-value pairs. There are two types of instance data: 
- Problem specifications, which may contain metadata or problem-specific information such as the max number of vehicles. 
- Problem data, which are often arrays of values describing, for example, customer service times and time windows. 

### VRPLIB
A VRPLIB instance consists of two parts, one part for problem specifications (as keyword-value pairs) and one part for problem data sections (as arrays).

### Solomon
A Solomon instance contains a section for vehicle data and a section for customer data.

The keywords of a Solomon instance are modified in the returned `instance` object. 

## On distances 
The VRP literature uses a number of different conventions for how the distances matrix are computed. The `vrplib` library tries to follow the instance specifications as strictly as possible to compute the distances. 

For VRPLIB instances, the distances computation is determined by the `EDGE_WEIGHT_TYPE` and possibly the `EDGE_WEIGHT_FORMAT` specifications. We currently support two categories of edge weight types:
- `*_2D`: compute the Euclidean distances using the node coordinate data.
    - `EUC_2D`: Double precision distances without rounding.
    - `FLOOR_2D`: Round down all distances to down to an integer.
    - `EXACT_2D`: Multiply the distances by 1000, round to the nearest integer.
- `EXPLICIT`: the distance data is explicitly provided, in partial or full form. For explicit matrices, the `EDGE_WEIGHT_FORMAT` must be specified. We support the following two formats:
  - `LOWER_ROW`: Lower row triangular matrix without diagonal entries.  
  - `FULL_MATRIX`: Explicit full matrix representation.
  
More information about how VRPLIB specifications can be found [here](  http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp95.pdf) and [here]( http://webhotel4.ruc.dk/~keld/research/LKH-3/LKH-3_REPORT.pdf).

Note that there are VRPLIB instances that use different rounding conventions in the literature, which are not necessarily specified in the instance. For example, the X instance set proposed by [Uchoa et al. (2017)](http://vrp.atd-lab.inf.puc-rio.br/index.php/en/new-instances) assumes that the distances are rounded to the nearest integer. When you use the `vrplib` package to read this instance, the distances are not rounded because it uses the `EUC_2D` edge weight type specification, which does not assume rounding. But this can be easily solved by round the distances matrix manually.

For Solomon-type instances, we compute the Euclidean distances and do not round the edges. A recent convention that was proposed during the [2021 DIMACS Vehicle Routing Implementation Challenge](http://dimacs.rutgers.edu/programs/challenge/vrp/vrptw/) is to round the Euclidean distances to one decimal. Similar to the X instance set, you can manually round the distances matrix after reading in the file.

## Additional remarks
- Downloading instances may take up to a few seconds. 
- The `XML100` benchmark set is not listed in `list_names` and cannot be downloaded through this package. You can download these instances directly from [CVRPLIB](http://vrp.atd-lab.inf.puc-rio.br/index.php/en/).

    
