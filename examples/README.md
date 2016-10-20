# Example debugging applications

Some of example debugging applications supported by PathDump. To run an
application, the PathDump controller and the end-host agent must be running.

## Query registration 

A debugging application consists of a front-end interface Python script (and a
query (or two queries)). If a debugging application has a query (or queries),
the query (queries) must be registered at the PathDump controller before it
(they) is executed on end-host(s). The following command shows how to register
a query.

```
sudo ./registerquery.py <query path>
```

\<query path\> is a path to a query file. If the user has write permission on
the target directory, 'sudo' can be omitted.

Note: the PathDump controller agent must be running before this command is
executed.

## Examples

### Example 1: Top-*K* flows

The application obtains top-*k* flows out of all flows stored in the entire
end-hosts. The application consists of three Python scripts (topk.py,
topk_query.py, and topk_query_agg.py). topk.py is a front-end script,
topk_query.py is a query to obtain local top-*k* flows from each end-host and
topk_query_agg.py aggregates those local top-*k* flows at intermediate end-hosts
in a query aggregation tree.

In order to run topk_query.py and topk_query_agg.py at end-hosts, they must be
first registered at the controller.

```
sudo ./registerquery.py <path_to_example>/topk_query.py
sudo ./registerquery.py <path_to_example>/topk_query_agg.py
```

Then, run the following:

```
sudo python topk.py [<k>]
```

\<k\> denotes the number of top-$k$ flows. Without \<k\>, default is 10.


### Example 2: Path conformance test

This application checks whether there is any policy violation on path and report
flows and their corresponding paths that violate the policy. It consists of two
scripts -- pathconf.py (front-end script) and pathconf_check.py (actual query
exeucted in end-hosts).

First, to register pathconf_check.py:

```
sudo ./registerquery.py <path_to_example>/pathconf_check.py
```

```
sudo python pathconf.py <command>
```

Options for \<command\>: install or uninstall. 'install' makes the query
(pathconf_check.py) get installed in end-hosts that subsequently run the query
forever until it gets uninstalled. When the policy on path is violated, the
script returns flows and their corresponding paths that violate the policy.

To uninstall the query:

```
sudo python pathconf.py uninstall
```

## Dependency

Any front-end Python script (e.g., topk.py) requires ctrlapi module as it
includes at the beginning of the script:

```
import ctrlapi as capi
```

Thus, a front-end Python script (e.g., topk.py) must be put in the same
directory of the PathDump controller. Alternatively, the following lines can be
added before 'import ctrlapi as capi':

```
import sys
sys.path.insert (0, '<pathdump_directory>')
```

\<pathdump_directory\> is the directory path where the controller is installed.
