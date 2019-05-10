## v0.0
### v0.0.2
>Date: 2019-05-10

**DONE**:

- [x] `dw_logger`的优化。
- [x] 风控内容识别SDK。

### v0.0.1
>Date: 2019-04-16

**DONE**:

- [x] 完成parser_engine.clue模块的迁移，并且将clue的增删改查操作从直接操作db改为服务调用。已在`抖音-齐家网`、`货车-优卡`等实际测试通过。
- [x] 完成了适用于scrapy的`SignalHandler`，运行正常。
- [x] 完成了`DwLogger`的迁移，且实现了接口信息配置化。已实测通过。
- [x] 提供了适用于商户信息抓取的通用数据模型`ShopItem`。

**TODO**：

- [ ] clue模块的服务化调用，应给出具体的服务方接口规范。
- [ ] 优化`SignalHandler`：获取更有价值的信息，如`clue_id`, 'from_clue_id'，`item`，`item class`，`dw action`等。
- [ ] 应给出适用于`DwLogger`的接口规范。