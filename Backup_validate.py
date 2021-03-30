import os
import datetime
import sys
import shutil
import distutils
from distutils import dir_util
from shutil import copytree, ignore_patterns

def backup():
    Date=str(datetime.datetime.now()).split(' ')[0]
    backup_dir = '/var/tmp'
    if not backup_dir.startswith('/'):
        print ("Please Specify the absolute path ,Example :/backup ")
        sys.exit()
    mode = 0o666
    backup_path = os.path.join(backup_dir,Date)
    if os.path.isdir(backup_path.strip()):
        old_backup = ((backup_path)+'-'+str(datetime.datetime.now()).split(' ')[1])
        os.rename(backup_path, old_backup)
    print ("Backup Directory is : "+(backup_path))
    backup_files = ('/var/tmp/backup_files')
    backup = open(backup_files,'r')
    for path in backup:
        path=path.strip()
        if os.path.isdir(path):
            ddir = (backup_path+path)
            distutils.dir_util.copy_tree (path,ddir,preserve_mode=1, preserve_times=1, preserve_symlinks=1, update=0, verbose=0)
            print((path)+ (": Directoy Backup Completed in ") +(ddir))
        if os.path.isfile(path.strip()):
            dfile = (backup_path+path)
            try:
                shutil.copy(path, dfile)
            except IOError as io_err:
                os.makedirs(os.path.dirname(dfile))
                shutil.copy(path, dfile)
            print((path) + (": File Backup taken as ") + (dfile))
        if '*' in (path):
            print ("EXISTING :Please dont mention * in backup configuration. Replace it with absolute Directory of File name ")
            break

def validate():
    backup_dir = raw_input("Please Specify the backup directory : ").strip()
    print ("The Backup directory is "+(backup_dir)+ ' This validation only applied to files in /var/tmp/backup_files, not to directories' )
    backup_files = ('/var/tmp/backup_files')
    backup = open(backup_files, 'r')
    for path in backup:
        path = path.strip()
        if os.path.isfile(path.strip()):
            file1 = path
            file2 = (backup_dir)+(path)
            with open(file1, 'r') as file1:
                with open(file2, 'r') as file2:
                    difference = set(file2).difference(file1)
                difference.discard('\n')
            if len(difference) > 0:
                print ( "\033[1;31;40m  File Name : "+str(path)+ " differs from "+str((backup_dir)+(path)) )
            for entries in (difference):
                print ('Entry: '+str(entries))

if 0<len(sys.argv)>1:
    if (sys.argv[1]).lower() == 'backup':
        print ("\033[1;32;40m Starting the Function : "+(sys.argv[1]) )
        backup()
        print('\x1b[0m')
    elif (sys.argv[1]).lower() == 'validate':
        print ("\033[1;32;40m Starting the Function : "+(sys.argv[1]) )
        print('\x1b[0m')
        validate()
        print('\x1b[0m')
    else:
        print ("\033[1;31;40m Unidentified request,please specify backup or validate ")
        print('\x1b[0m')
        sys.exit()
else:
    print "\033[1;31;40m This Script requires arguments (Example: backup,validate)"
    print('\x1b[0m')
    sys.exit()
