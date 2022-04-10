## 1. 子查询

独立子查询 `(IN)`，相关子查询 `(EXISTS)`

- `EXISTS` 将 `IN` 变为 `EXISTS`

示例1: 查询指定部门的所有员工信息
```sql
SELECT 
    *
FROM
    employees
WHERE
    emp_no IN (SELECT 
            emp_no
        FROM
            dept_emp
        WHERE
            dept_no = 'd005')
LIMIT 10;
```

```sql
SELECT 
    *
FROM
    employees e
WHERE
    EXISTS( SELECT 
            *
        FROM
            dept_emp de
        WHERE
            dept_no = 'd005'
                AND e.emp_no = de.emp_no)
LIMIT 10;

```

示例2: 查询每个月最大的订单信息

```sql
SELECT 
    *
FROM
    orders
WHERE
    o_orderdate IN (SELECT 
            MAX(o_orderdate)
        FROM
            orders
        GROUP BY (DATE_FORMAT(o_orderdate, '%Y%M')));
```
```sql
SELECT 
    *
FROM
    orders a
WHERE
    EXISTS( SELECT 
            MAX(o_orderdate)
        FROM
            orders b
        GROUP BY (DATE_FORMAT(o_orderdate, '%Y%M'))
        HAVING MAX(o_orderdate) = a.o_orderdate);
```

第一条sql语句 `GROUP BY` 仅执行 `1`次，第二条执行 `length(orders)` 次

**区别:**
- 子查询不同
- not in 只会返回 0 或 null, `exist` 返回结果是正确的

## 2. 分页

```sql
select * from employees order by birth_date limit 30;

select * from employees order by birth_date limit 3000000, 30;

alter table employees add index idx_birth_date(birth_date, emp_no);

select * from employees order by birth_date, emp_no limit 30;

select * from employees where (birth_date, emp_no) > ("1952-02-02", 217446) order by birth_date, emp_no limit 30;
```

## 3. 多表连接

例子1: 获取最新员工编号
```sql
SELECT 
    e.emp_no, t.title
FROM
    employees e,
    (SELECT 
        emp_no, title
    FROM
        titles
    WHERE
        (emp_no , to_date) IN (SELECT 
                emp_no, MAX(to_date)
            FROM
                titles
            GROUP BY emp_no)) t
WHERE
    e.emp_no = t.emp_no;
```

### 3.1 JOIN

分为 `外连接` 和 `内连接`

`on` 是做表之间的过滤, `where` 是条件过滤，在内连接中可以替换，但是外连接中不可以

```sql
select * from x,y where x.a = y.a;

select * from x join y on x.a = y.a;    -- 求交集
```

```sql

select * from x where a in (select a from y);   -- 子查询, 也可以称半连接, 对重复数据去重

select distinct x.* from x join y on x.a = y.a;     -- distinct, 用于去重
```

#### 3.1.1 left join and right join

保留哪个表

#### 3.1.2 行号问题

```sql
-- 定义一个初始变量
set @a:=0;

select @a:=@a+1, * from employees limit 10;
```

- 使用了关联的方式
```sql
select @a:=@a+1 as rownum, * from employees, (select @a:=0) a limit 10;
```


## 4. Prepare

```sql
SET @s = 'SELECT * FROM employees where 1=1';

SET @s = concat( @s, ' and gender = "m"' );

SET @s = concat( @s, ' and birth_date >= "1960-01-01"' );

SET @s = concat( @s, ' order by emp_no limit ?,?' );

SET @page_no = 0;

SET @page_count = 10;
PREPARE stmt 
FROM
	@s;
EXECUTE stmt USING @page_no,
@page_count;
DEALLOCATE PREPARE stmt;
```

作用:
- 解析的开销更小
- 防止SQL注入
- 动态查询