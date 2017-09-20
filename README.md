# pybench

### Overview

python3 benchmark tool

### Requirements:

```
pip3 install injector
pip3 install fudge
```

### Usage: 

```
$PROJECT_ROOT/src/main/python/main.py --help/-h
```

And copy src/main/resources *.txt.sample to *.txt
If need cookie for request Please add values to cookies.txt
```
name1=value1
name2=value2
.
.
```

### Example:

```
cd $PROJECT_ROOT
src/main/python/main.py -u http://localhost -n 10 -c 2
```

##### QPS mode

QPS is Query Per Seconds.
If you want to use the QPS mode, Please add the -q and -s options.

```
src/main/python/main.py -u http://localhost -n 600 -c 2 -q 10 -s 1
```
