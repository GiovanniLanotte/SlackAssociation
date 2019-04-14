from multiprocessing import Lock
import shutil
from threading import Thread
from git import Git
import os
import yaml


class ControlFilesRepository(Thread):
    _threadLock: Lock = Lock()

    def __init__(self, name_org, repo):
        Thread.__init__(self)
        self._name_org = name_org
        self._repo = repo
        self._return = None
        self._num_programming = 0
        self._tot_files = 0
        path = 'log'
        if not os.path.isdir(path):
            os.makedirs(path)
        self._filename = path + '/files programming found ' + self._name_org + ' ' + self._repo.name + '.log'
        self._download_complete = path + '/download complete ' + self._name_org + ' ' + self._repo.name + '.log'

    @staticmethod
    def is_programming(ext_file):
        with open("languages.yml", 'r') as stream:
            load = yaml.load(stream)
            keys = list()
            for key in load:
                keys.append(key)
            for key in keys:
                if load[key].get('extensions') is not None:
                    if load[key]['type'] == 'programming':
                        extensions = load[key]['extensions']
                        if ext_file in extensions:
                            return True
        return False

    def contain_programming(self, path):
        for element in os.listdir(path):
            if not element.startswith('.'):
                if os.path.isdir(path + '/' + element):
                    self.contain_programming(path + '/' + element)
                if os.path.isfile(path + '/' + element):
                    self._tot_files = self._tot_files + 1
                    if self.is_programming(os.path.splitext(path + '/' + element)[1]):
                        self._num_programming = self._num_programming + 1

    def run(self):
        self._return = self.count_files_repository()

    def count_files_repository(self):
        clone_url = self._repo.clone_url
        path_org = 'repositories ' + self._name_org
        path_repo = path_org + '/' + self._repo.name
        if self._file_exists():
            self._read_log()
        else:
            if not os.path.isfile(self._download_complete):
                if not os.path.exists(path_org):
                    os.mkdir(path_org)
                if os.path.exists(path_repo):
                    shutil.rmtree(path_repo)
                self._threadLock.acquire()
                Git(path_org).clone(clone_url)
                self._threadLock.release()
                open(self._download_complete, "w").close()
            self.contain_programming(path_repo)
            shutil.rmtree(path_repo)
            self._write_file()
        return [self._num_programming, self._tot_files]

    def join(self, timeout: object = None) -> object:
        Thread.join(self, timeout)
        return self._return

    def _file_exists(self):
        return os.path.exists(self._filename)

    def _read_log(self):
        file = open(self._filename, 'r')
        try:
            self._num_programming = int(file.readline())
            self._tot_files = int(file.readline())
        finally:
            file.close()

    def _write_file(self):

        file = open(self._filename, 'w')
        try:
            file.write(str(self._num_programming) + '\n' + str(self._tot_files))
        finally:
            file.close()
