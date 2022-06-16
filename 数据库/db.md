# 数据库隔离级别与锁

- [美团技术博客：Innodb中的事务隔离级别和锁的关系](https://tech.meituan.com/2014/08/20/innodb-lock.html)
- [CSNotes: 数据库原理](https://github.com/CyC2018/CS-Notes/blob/master/notes/%E6%95%B0%E6%8D%AE%E5%BA%93%E7%B3%BB%E7%BB%9F%E5%8E%9F%E7%90%86.md#%E6%95%B0%E6%8D%AE%E5%BA%93%E7%B3%BB%E7%BB%9F%E5%8E%9F%E7%90%86)

#　Oracle 执行计划

- [Oracle 执行计划](https://www.cnblogs.com/xqzt/p/4467867.html)
- [执行计划中的多表连接](https://www.cnblogs.com/xqzt/p/4469673.html)

## 什么是 autotrace

The autotrace provides instantaneous feedback including the returned rows, execution plan, and statistics.


## 什么是 oracle 中的 hint

Oracle的Hint是用来提示Oracle的优化器，用来选择用户期望的执行计划。

使用Hint可以实现以下功能：

- 改变SQL中的表的关联顺序。
- 改变SQL中的表的关联方式。
- 实现并行方式执行DML、DDL以及SELECT语句。
- 改变表的访问路径 即数据读取方式
- 调整查询转换类型，重写SQL。
- 调整优化器优化目标。
- 调整优化器类型
