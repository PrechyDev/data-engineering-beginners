#! /usr/bin/bash

#backup all databases
#To backup just one database -> mysqldump db_name > backup-file.sql
mysqldump --host=[enter value here] --port=[enter value like 3306] --all-databases --user=root --password=[enter password] > all-databases-backup.sql

#get path of the backup file
curr=$(pwd)
backup_file=$curr/all-databases-backup.sql

#create /tmp/mysqldumps/<current date>/. This part can be changed into anypath
cd ~
cd /tmp
curr_date=$(date +'%Y%M%d')
mkdir $curr_date

# get path of destination directory
cd $curr_date
dest_dir=$(pwd)

#move file into destination directory
mv $backup_file $dest_dir

echo 'Database backup complete'

