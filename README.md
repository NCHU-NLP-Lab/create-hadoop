# Create Hadoop
批量建立教學用hadoop

首次使用請先在本地建立映像檔:
```sh
$ docker build -t udic_hadoop .
```
## port 說明
- `22`: ssh
- `8888`: jupyter
- `8080`: spark
- `8088`: hadoop

## main.py
執行完產生兩個`.log`file和一個`.csv`file

- `pwd_log.log`: 帳號與密碼
- `create_hadoop.log`: container port
- `pwd.csv`: 帳號、密碼、port表格，方便直接複製。csv格式如下表:

|index|host_type|account|password|ssh_port|web_port|
|:-:|:-:|:-:|:-:|:-:|:-:|
|0|master|8953_udic_hadoop_master_0|magxrr|49477|49474|
|1|slave|8953_udic_hadoop_slave_0-0|inyupj|49478||
|2|master|8953_udic_hadoop_master_1|khiwmd|49483|49480|
|3|slave|8953_udic_hadoop_slave_1-0|gzlssf|49484||


### Args:
```
action: [create|remove]
-d, --dry_run: 僅印出指令，不執行
```
### Create
批量建立
```python
python3 main.py create
```

### Remove
批量刪除
```python
python3 main.py remove
```
> 需提供container批量建立時隨機產生的4位數字(container name prefix)
