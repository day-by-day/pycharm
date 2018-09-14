# -*- coding: UTF-8 -*-
import os
import time
import string
def   mysql_backup_dump(soft_path,parameter,backup_file):
            user='localdba'
            passwd='18CC8FE478A294B854BC3B3D0CC4E27F'
            sql_comm="%s  -u%s  -p%s  %s |/bin/gzip >%s"%(soft_path,user,passwd,parameter,backup_file)
            if os.system(sql_comm) == 0:
               print  backup_file+'This file backup success!'
            else:
               print backup_file+'This file backup  Failed!!'

if __name__=='__main__':
            backup_path='/data/backup/gz/'

            #备份passport
            backup_file=backup_path+'passport_'+time.strftime('%Y%m%d')+'.tar.gz'
            mysql_backup_dump( '/usr/local/webserver/percona5.6.19/bin/mysqldump','-P3306  -S /data/mysql/3306/run/mysql.sock   --master-data  --single-transaction --quick  passport',backup_file)
            #拷贝passport
            backup_scp='scp -l 500000 '+backup_file+' 10.1.0.10:/data2/backup/10.1.0.20_backup/'
            if os.path.exists(backup_path):
                  os.system(backup_scp)
                  os.system("python /data/shell/mail.py ph.admin@weststarinc.co 异地备份投放_`date '+%Y%m%d'` '10.1.0.20_hc_passport backupex Offsite Backup OK' ")
            else:
                  os.system("python /data/shell/mail.py ph.admin@weststarinc.co 异地备份投放_`date '+%Y%m%d'` '10.1.0.20_hc_passport backupex Offsite Backup ERROR' ")

            #backup lotterycms
            backup_file=backup_path+'lotterycms_'+time.strftime('%Y%m%d')+'.tar.gz'
            mysql_backup_dump( '/usr/local/webserver/percona5.6.19/bin/mysqldump','-P3306  -S /data/mysql/3306/run/mysql.sock   --master-data  --single-transaction --quick  lotterycms ',backup_file)
            #拷贝lotterycms
            backup_scp='scp -l 500000 '+backup_file+' 10.1.0.10:/data2/backup/10.1.0.20_backup/'
            if os.path.exists(backup_path):
                  os.system(backup_scp)
                  os.system("python /data/shell/mail.py ph.admin@weststarinc.co 异地备份投放_`date '+%Y%m%d'` '10.1.0.20_hc_lotterycms backupex Offsite Backup OK' ")
            else:
                  os.system("python /data/shell/mail.py ph.admin@weststarinc.co 异地备份投放_`date '+%Y%m%d'` '10.1.0.20_hc_lotterycms backupex Offsite Backup ERROR' ")

            #backup lotteryserver
            backup_file=backup_path+'lotteryserver_'+time.strftime('%Y%m%d')+'.tar.gz'
            mysql_backup_dump( '/usr/local/webserver/percona5.6.19/bin/mysqldump','-P3306  -S /data/mysql/3306/run/mysql.sock   --master-data  --single-transaction --quick  lotteryserver ',backup_file)
            #拷贝lotteryserver
            backup_scp='scp -l 500000 '+backup_file+' 10.1.0.10:/data2/backup/10.1.0.20_backup/'
            if os.path.exists(backup_path):
                  os.system(backup_scp)
                  os.system("python /data/shell/mail.py ph.admin@weststarinc.co 异地备份投放_`date '+%Y%m%d'` '10.1.0.20_hc_lotteryserver backupex Offsite Backup OK' ")
            else:
                  os.system("python /data/shell/mail.py ph.admin@weststarinc.co 异地备份投放_`date '+%Y%m%d'` '10.1.0.20_hc_lotteryserver backupex Offsite Backup ERROR' ")

            #删除14天之前的
            clear_expire_back='find  '+backup_path+'  -mtime  +14|grep "\.gz"  |xargs rm -f '
            os.system(clear_expire_back)

