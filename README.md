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
執行完產生兩個`.log`file

- `pwd_log.log`: 帳號與密碼
- `create_hadoop.log`: container port

### Args:
```
action: [create|remove]
-d, --dry_run: 僅印出指令，不執行
```
### Create
```python
python3 main.py create
```

### Remove
```python
python3 main.py remove
```
> 需提供container批量建立時隨機產生的4位數字(container name prefix)
