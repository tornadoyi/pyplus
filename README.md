# timeparse

[timeparse](https://github.com/tornadoyi/timeparse) is parser for extract and format time word in chinese sentence.


## Quick Install

```bash
    # setup pyplus
    git clone https://github.com/tornadoyi/pyplus.git
    cd pyplus
    sudo python setup.py install

    # setup timeparse
    git clone https://github.com/tornadoyi/timeparse.git
    cd timeparse
    sudo python setup.py install
```


# Document

Easy to use
```python
    # -*- coding: utf-8 -*-
    import timeparse
    times = timeparse.parse(u"16年3月2号到7号")
    for t in times: print(t)
    # (2016-03-02, 2016-03-07)
```

Part of sentence extractor
```python
    # -*- coding: utf-8 -*-
    import timeparse
    times = timeparse.parse(u"16年5月1号 16年3月2", pos=7, endpos=14)
    for t in times: print(t) 
    # (2016-03-02, 2016-03-02)
```

Use timecore to fix your current timestamp
```python
    # -*- coding: utf-8 -*-
    from pyplus import *
    import timeparse
    import time
    
    args = qdict(timecore=timeparse.TimeCore())
    times = timeparse.parse(u"昨天", args=args)
    for t in times: print(t)
    # (2016-12-26, 2016-12-26)

    args.timecore.timestamp = time.time() - 24*3600
    times = timeparse.parse(u"昨天", args=args)
    for t in times: print(t)
    # (2016-12-25, 2016-12-25)
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
