import argparse
import os 
import shutil
import hashlib
import time
import datetime


""" 
    Author: Ivan Santos
    
    This module provides synchronization process methods.
"""
def main():
    parser = argparse.ArgumentParser(description='Synchronizes two folders: source and replica')
    parser.add_argument('-s', '--source', help='Source folder path', type=str, required=True)
    parser.add_argument('-r', '--replica', help='Replica folder path', type=str, required=True)
    parser.add_argument('-p', '--period', help='Period of time in seconds between each synchronization', type=int, required=True)
    parser.add_argument('-l', '--logs', help='Logs file path', type=str, required=True)
    args = parser.parse_args()
    synchronization(args.source, args.replica, args.period, args.logs)

def synchronization(source_folder_path, replica_folder_path, period, logs_path):
    '''
    synchronization: starts the synchronisation process and calls the necessary methods.
    
    Args:
        source_folder_path (string): source folder path.
        replica_folder_path (string): replica folder path.
        period (int): period of time in seconds between each synchronization.
        logs_path (string): logs file path.
    
    Return:
        Synchronizes two folders: source and replica.
    '''

    check_path_source_folder(source_folder_path)
    check_path_replica_folder(replica_folder_path)

    if os.path.isdir(source_folder_path):
        while True:
            syncFolder(source_folder_path, replica_folder_path, logs_path)
            time.sleep(period)
    else:
        raise Exception('#ERROR#: {} IS NOT A FOLDER!'.format(source_folder_path))


def syncFolder(source_folder_path, replica_folder_path, logs_path):
    """
    syncFolder: synchronizes two folders: source and replica.

    Args:
        source_folder_path (string): source folder path.
        replica_folder_path (string): replica folder path.
        logs_path (string): logs file path.
    
    Return:
        Synchronizes two folders: source and replica.
    """

    # delete itens in replica folder that are not in source folder
    for item in os.listdir(replica_folder_path):
        source_folder_item_path = os.path.join(source_folder_path, item)
        replica_folder_item_path = os.path.join(replica_folder_path, item)

        if os.path.isdir(replica_folder_item_path):
            if not os.path.exists(source_folder_item_path):
                deleteFolder(replica_folder_item_path, logs_path)
        if os.path.isfile(replica_folder_item_path):
            if not os.path.exists(source_folder_item_path):
                deleteFile(replica_folder_item_path, logs_path)

    for item in os.listdir(source_folder_path):
        source_folder_item_path = os.path.join(source_folder_path, item)
        replica_folder_item_path = os.path.join(replica_folder_path, item)

        if os.path.isdir(source_folder_item_path):

            if not os.path.exists(replica_folder_item_path):
                os.mkdir(replica_folder_item_path)
            elif os.path.isfile(replica_folder_item_path):
                os.remove(replica_folder_item_path)

            syncFolder(source_folder_item_path, replica_folder_item_path, logs_path)
        elif os.path.isfile(source_folder_item_path):

            if os.path.exists(replica_folder_item_path):
                if os.path.isdir(replica_folder_item_path):
                    os.removedirs(replica_folder_item_path)

            syncFile(source_folder_item_path, replica_folder_item_path, logs_path)
        else:
            raise Exception('#ERROR#: {} IS NEITHER A FILE NOR A FOLDER!'.
                            format(source_folder_item_path))

def syncFile(source_file_path, replica_file_path, logs_path):
    """
    syncFile: synchronizes two files: source and replica.

    Args:
        source_file_path (string): source file path.
        replica_file_path (string): replica file path.
        logs_path (string): logs file path.
    
    Return:
        Synchronizes two files: source and replica.
    """
    sourceFileTime = getFileStamp(source_file_path)
    
    if not os.path.exists(replica_file_path):
        createFile(source_file_path, replica_file_path, logs_path, sourceFileTime)
        return
    
    replicaFileTime = getFileStamp(replica_file_path)
    
    sourceFileSize = getFileSize(source_file_path)
    replicaFileSize = getFileSize(replica_file_path)
    
    sourceFileHash = getFileHash(source_file_path)
    replicaFileHash = getFileHash(replica_file_path)

    if (sourceFileTime != replicaFileTime
            or sourceFileSize != replicaFileSize or sourceFileHash != replicaFileHash):
        copyFile(source_file_path, replica_file_path, logs_path, sourceFileTime)
        return

def check_path_source_folder(source_folder_path):
    """
    check_path_source_folder: checks if the source folder path is valid.

    Args:
        source_folder_path (string): source folder path.

    Return:
        Raises an exception if the source folder path is not valid.
    """
    if not os.path.exists(source_folder_path):
        raise Exception('#ERROR#: {} NOT EXISTS!'.format(source_folder_path))

def check_path_replica_folder(replica_folder_path):
    """
    check_path_replica_folder: checks if the replica folder path is valid.

    Args:
        replica_folder_path (string): replica folder path.

    Return:
        Raises an exception if the replica folder path is not valid.
    """
    if not os.path.exists(replica_folder_path):
        new_dir = input('WARNING! {} not exists, do you want to make a new dir? yes(y) or exit(n): '.format(replica_folder_path)).strip()
        while len(new_dir) < 1:
            new_dir = input('WARNING! {} not exists, do you want to make a new dir? yes(y) or exit(n): '.format(replica_folder_path)).strip()

        if new_dir == 'y' or new_dir == 'yes':
            os.mkdir(replica_folder_path)
        else:
            print('Thanks for your visit!')
            time.sleep(2)
            os._exit(os.X_OK)

def getFileStamp(file):
    """
    getFileTime: gets the file time.

    Args:
        file (string): file path.

    Return:
        Returns the file last modification time.
    """
    return os.path.getmtime(file)

def getFileSize(file):
    """
    getFileSize: gets the file size.

    Args:
        file (string): file path.

    Return:
        Returns the file size.
    """
    return os.path.getsize(file)

def getFileHash(file):
    """
    getFileHash: gets the file hash.

    Args:
        file (string): file path.

    Return:
        Returns the file hash.
    """
    return hashlib.md5(open(file,'rb').read()).hexdigest()

def deleteFolder(replica, logs_path):
    """
    deleteFolder: delete a folder.

    Args:
        replica (string): replica folder path.
        logs_path (string): logs file path.
    
    Return:
        Deletes the folder.
    """
    os.rmdir(replica)
    saveLogs(datetime.datetime.now(), 'DELETE', replica=replica, path=logs_path)

def deleteFile(replica, logs_path):
    """
    deleteFile: delete a file.

    Args:
        replica (string): replica file path.
        logs_path (string): logs file path.
    
    Return:
        Deletes the file and records in the logs.
    """
    os.remove(replica)
    saveLogs(datetime.datetime.now(), 'DELETE', replica=replica, path=logs_path)

def createFile(source, replica, logs_path, src_modifitcationTime):
    """
    createFile: create a file.

    Args:
        source (string): source file path.
        replica (string): replica file path.
        logs_path (string): logs file path.
        src_modifitcationTime (string): source file modification time.

    Return:
        Creates the file.
    """
    if not os.path.exists(os.path.dirname(replica)):
        os.makedirs(os.path.dirname(replica))
    shutil.copy(source, replica)
    os.utime(replica, (datetime.datetime.now().timestamp(), src_modifitcationTime))
    saveLogs(datetime.datetime.now(), 'CREATE', source, replica, path=logs_path)

def copyFile(source, replica, logs_path, src_modifitcationTime):
    """
    copyFile: copy a file from source to replica.

    Args:
        source (string): source file path.
        replica (string): replica file path.ç
        logs_path (string): logs file path.
        src_modifitcationTime (string): source file modification time.
    
    Return:
        Copies the file from source to replica.
    """
    if not os.path.exists(os.path.dirname(replica)):
        os.makedirs(os.path.dirname(replica))
    shutil.copy(source, replica)
    os.utime(replica, (datetime.datetime.now().timestamp(), src_modifitcationTime))
    saveLogs(datetime.datetime.now(), 'COPY', source, replica, path=logs_path)

def saveLogs(timestamp, action, source=None, replica=None, user='ADMIN', path='logs/logs.txt'):
    """
    saveLogs: save logs in a file.

    Args:
        timestamp (string): timestamp of the action.
        action (string): action to take. Can be: COPY, DELETE, CREATE.
        source (string): source file path.
        replica (string): replica file path.
        user (string): user.
        path (string): logs file path.

    Return:
        Saves the logs in a file and print to console.
    """
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path))
    if action == 'DELETE':
        message = 'Timestamp: {} | Action: {} | From: {} | User: {} |'.format(timestamp, action, replica, user)
    elif action == 'COPY':
        message = 'Timestamp: {} | Action: {} | From: {} | To: {} | User: {} |'.format(timestamp, action, source, replica, user)
    elif action == 'CREATE':
        message = 'Timestamp: {} | Action: {} | From: {} | To: {} | User: {} |'.format(timestamp, action, source, replica, user)
    with open(path, 'a') as f:
        f.write(message)
        f.write('\n')
    print("\n")
    print(message)
    print("\n")

# syncFolder("source", "replica", "logs/logs.txt")

if __name__ == "__main__":
    main()