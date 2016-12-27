# timeparse

[pyplus](https://github.com/tornadoyi/pyplus) is extension libarary of python.


## Quick Install

```bash
    # setup pyplus
    git clone https://github.com/tornadoyi/pyplus.git
    cd pyplus
    sudo python setup.py install
```


# Document

QDict (use dict like lua table)
```python
    from pyplus import *
    d = qdict(a=1, b=2)
    d.c = 3
    print(d)
    # {'a': 1, 'c': 3, 'b': 2}
```

Enum
```python
    from pyplus import *
    e = enum(a=1,b=2)
```

Singleton
```python
    from pyplus import *
    @singleton
    class Manager(object):
        def __init__(self):
            print("init once")
        def unused(self): return
        
    Manager().unused()
    Manager().unused()
```



## Support

For any bugs or feature requests please:

File a new [issue](https://github.com/tornadoyi/timeparse/issues) or submit
a new [pull request](https://github.com/tornadoyi/timeparse/pulls) if you
have some code you'd like to contribute

For other questions and discussions please post a email to 390512308@qq.com


## License

We are releasing [timeparse](https://github.com/tornadoyi/timeparse) under an open source
[Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) License. We welcome you to contact us (390512308@qq.com) with your use cases.
