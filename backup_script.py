#!/usr/bin/env python3

from os import path, system, listdir, remove
from datetime import datetime as dt
from pathlib import Path

if __name__ == "__main__":
    backupsPath = "/backup/"
    backupsPathContents = sorted(listdir(backupsPath))
    targetFolderName = dt.utcnow().strftime("%Y-%m-%d_%H:%M:%S")
    Path(path.join(backupsPath, targetFolderName)).mkdir(parents=True, exist_ok=True)
    Path(path.join(backupsPath, "gdrivelink")).mkdir(parents=True, exist_ok=True)
    if len(backupsPathContents) > 0:
        oldestBackup = backupsPathContents[0]
        system("rsync -vaxcH --progress --exclude=/backup/ --compare-dest=/backup/"+oldestBackup+"/. /. /backup/"+targetFolderName+"/")
        system("diff -rq /backup/"+oldestBackup+" / | grep \"Only in /backup/"+oldestBackup+"\" >> /backup/"+targetFolderName+"/delete.txt")
        with open("/backup/"+targetFolderName+"/delete.txt", "r") as f:
            deletions = f.read()
        deletions = deletions.replace("Only in /backup/"+oldestBackup, "").replace(": ", "/")
        remove("/backup/"+targetFolderName+"/delete.txt")
        with open("/backup/"+targetFolderName+"/delete.txt", "w") as f:
            f.write(deletions)
    else:
        system("rsync -vaxcH --progress --exclude=/backup/ /. /backup/"+targetFolderName+"/")
    system("tar -czvf /backup/gdrivelink/"+targetFolderName+".tar.gz /backup/"+targetFolderName)
    system("chown -R stgardner4:stgardner4 /backup/gdrivelink/")
    system("sudo -u stgardner4 rclone sync /backup/gdrivelink/ sam_wx4stg_gdrive:backups --bwlimit=8.5M --progress")
