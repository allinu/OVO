# OVO

需要指定的环境变量:

- NOTICE_KEY: http://pushplus.hxtrip.com/index Push+ 密钥

数据库已经包含的表

```sql
CREATE TABLE tasks (
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    school TEXT NOT NULL,
    gps TEXT NOT NULL,
    gps_loc_name TEXT NOT NULL,
    alias TEXT NOT NULL UNIQUE,
    id INTEGER PRIMARY KEY AUTOINCREMENT
);
CREATE INDEX tasks_id_IDX ON tasks (id);
CREATE INDEX tasks_username_IDX ON tasks (username);
```

已经实现的接口：

1. /tasks

   - GET: 获取所有任务
   - POST: 添加任务

     ```
     {
         username: "",
         password: "",
         school: "",
         gps: "",
         gps_loc_name: "",
         alias: ""
     }
     ```

   - PUT: 更新任务
     `username`

     ```
     {
        username: "",
        password: "",
        school: "",
        gps: "",
        gps_loc_name: "",
        alias: ""
     }
     ```

   - DELETE: 删除任务
     `username`
