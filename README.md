# trent
Convenient Collection/Sequence/Iterable processing for python.

Inspired by Clojure mapping and threading macros.

Supprot full python12 (and later vesrsion) typing, unlike default `map` and `filter` functions.
Which allows for production-grade development. 
Provides some work-around for python typing issues (like inability to filter out types from aggregate type).
Provides some auxiliary side funtions, like `first`, `second`, `nth`, `getter` etc.
Also, provide some additional usefull functionality, like `group_by` and `partition_by` (see more examples below)