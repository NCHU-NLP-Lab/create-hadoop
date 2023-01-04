# -*- coding:utf-8 -*-
import argparse
import csv
import os
import random
import re
import string

parser = argparse.ArgumentParser()
parser.add_argument("action", type=str, help="create|remove")
parser.add_argument('-d','--dry-run', action='store_true')
args = parser.parse_args()

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def cmd(cmd_str):
    print(cmd_str)
    if(not args.dry_run):
        os.system(cmd_str)

def popen(cmd_str):
    print(cmd_str)
    if(not args.dry_run):
        return os.popen(cmd_str).read().split()
    else:
        return []

def remove():
    print("======")
    print("remove")
    print("======")
    random_prefix = int(input("4 digts random_prefix:"))
    # remove live or dead container
    docker_ids = popen('docker ps -a -q -f "name=%d_udic_hadoop_"'%random_prefix)
    # stop all
    for d_id in docker_ids: cmd('docker stop %s'%d_id)
    # rm all
    for d_id in docker_ids: cmd('docker rm %s'%d_id)

def create():
    print("======")
    print("create")
    print("======")

    create_log = open('create_hadoop.log','w',encoding='utf-8')
    pwd_log = open('pwd_log.log','w',encoding='utf-8')

    hadoop_should_create_count = int(input("how many hadoop env to open? :"))
    slave_should_create_count = int(input("how many slave for each master? :"))

    random_prefix = random.randint(1000,9999)
    base_image = 'udic_hadoop:latest'
    master_name_prefix = '%d_udic_hadoop_master_'%random_prefix
    slave_name_prefix = '%d_udic_hadoop_slave_'%random_prefix

    host_info_dict = {}
    fieldnames = ["index", "host_type", "account", "password", "ssh_port", "web_port"]
    idx = 0
    for m_i in range(hadoop_should_create_count):
        pwd_log.write("------------%d------------\n"%(m_i))

        master_name = master_name_prefix + str(m_i)
        master_user_name = master_name
        master_user_pwd = get_random_string(6)

        pwd_log.write("%s\n"%master_user_name)
        pwd_log.write("%s\n"%master_user_pwd)
        pwd_log.write("\n")

        host_info_dict[master_user_name] = {
            "index": idx,
            "host_type": "master",
            "account": master_user_name,
            "password": master_user_pwd
        }
        idx += 1

        cmd('docker run --name %s --hostname %s -itd -p 22 -p 8088 -p 8080 -p 8000 -p 8888 -e"NAME"=%s -e"PASSWORD"=%s %s'%(master_name,master_name,master_user_name,master_user_pwd,base_image))
        for s_i in range(slave_should_create_count):
            slave_name = slave_name_prefix + '%d-%d'%(m_i,s_i)
            slave_user_name = slave_name
            slave_user_pwd = get_random_string(6)

            pwd_log.write("%s\n"%slave_user_name)
            pwd_log.write("%s\n"%slave_user_pwd)
            pwd_log.write("\n")

            host_info_dict[slave_user_name] = {
                "index": idx,
                "host_type": "slave",
                "account": slave_user_name,
                "password": slave_user_pwd
            }
            idx += 1
            cmd('docker run --name %s --hostname %s -itd -p 22 -e"NAME"=%s -e"PASSWORD"=%s %s'%(slave_name,slave_name,slave_user_name,slave_user_pwd,base_image))
    
    # show create
    create_result = os.popen('docker ps --format "{{.Names}}, {{.Ports}}" -f "name=%d_udic_hadoop_"'%random_prefix).read().split("\n")
    create_result.pop(-1)

    # get ports
    for r in create_result:
        username = r.split(",")[0]
        match = re.search(r"0.0.0.0:(\d+)->22/tcp", r)
        host_info_dict[username]["ssh_port"] = match.group(1)
        match = re.search(r"0.0.0.0:(\d+)->8088/tcp", r)
        if match:
            host_info_dict[username]["web_port"] = match.group(1)
    
    # write csv file
    with open("pwd.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writeheader()
        host_info_rows = sorted(host_info_dict.values(), key=lambda d: d["index"])
        for row in host_info_rows:
            writer.writerow(row)
        

    for i,r in enumerate(create_result):
        r = ' '.join(r.split())
        create_log.write(r+'\n')
        if((i+1)%(slave_should_create_count+1)==0):
            create_log.write('\n')


if __name__ == "__main__":
    if args.action == 'create':
        create()
    elif args.action == 'remove':
        remove()
    else:
        assert False,'action=[create|remove]'
