# spider-common

Common code used in python spider.

## Changelog
See [CHANGELOG](CHANGELOG.md)

## Project Structure
- common_utils
    >通用全局函数
- clue
    >clue(爬虫线索)模块
- notify
    >事件、信号通知
- persistent
    >通用数据模型
    
    >抓取数据持久化
    
代码结构：
```
├── clue
│   ├── api.py
│   ├── constants.py
│   ├── __init__.py
│   ├── models.py
│   └── scrapy
│       ├── extensions.py
│       ├── __init__.py
│       ├── items.py
│       ├── middlewares.py
│       ├── pipelines.py
│       └── spider.py
├── common_utils
│   ├── exceptions.py
│   ├── __init__.py
│   └── time.py
├── __init__.py
├── notify
│   ├── constants
│   │   ├── __init__.py
│   │   └── signals.py
│   ├── __init__.py
│   ├── __pycache__
│   └── scrapy
│       ├── extensions
│       │   ├── __init__.py
│       │   └── signal_handler.py
│       └── __init__.py
├── persistent
│   ├── __init__.py
│   ├── items
│   │   ├── base.py
│   │   ├── __init__.py
│   │   └── shop.py
│   └── scrapy
│       ├── dw_logger.py
│       ├── __init__.py
│       └── pipelines
│           ├── dw_pipeline.py
│           ├── __init__.py
│           └── mysql_pipeline.py
```
