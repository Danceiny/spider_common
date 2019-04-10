# spider-common

Common code used in python spider.

## Project Structure
- common_utils
    >通用全局函数
- clue
    >与clue相关的代码
- notify
    >事件、信号通知相关的代码
    
代码结构：
```
├── README.md
├── VERSION
├── clue
│   ├── __init__.py
│   ├── constants.py
│   ├── models.py
│   └── scrapy
│       ├── __init__.py
│       ├── items.py
│       ├── middlewares.py
│       ├── pipelines.py
│       └── spider.py
├── common_utils
│   └── __init__.py
├── notify
│   ├── __init__.py
│   ├── constants
│   │   ├── __init__.py
│   │   └── signals.py
│   └── scrapy
│       ├── __init__.py
│       └── extensions
│           ├── __init__.py
│           └── signal_notify_extension.py
└── setup.py

```
