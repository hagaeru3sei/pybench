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

