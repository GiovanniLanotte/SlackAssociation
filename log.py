import os


class Log:
    @staticmethod
    def control_write_log(name_file, index, value=None):
        if os.path.exists(name_file):
            index_prev = Log.read_log(name_file)
            if index != index_prev:
                Log.write_log(name_file, index, value)
        else:
            Log.write_log(name_file, index, value)

    @staticmethod
    def write_log(name_file, index, value=None):
        os.makedirs(os.path.dirname(name_file), exist_ok=True)
        file = open(name_file, 'w')
        try:
            if value is None:
                file.write(str(index) + '\n')
            else:
                file.write(str(index) + '\n' + str(value))
        finally:
            file.close()

    @staticmethod
    def search_file_log(name_file):
        if os.path.exists(name_file):
            num, value = Log.read_log(name_file)
            if num > 0:
                num = num + 1
        else:
            num = 0
            value = False
        return num, value

    @staticmethod
    def read_log(name_file):
        file = open(name_file, 'r')
        try:
            index = int(file.readline())
            line = file.readline()
            if line != "":
                value = bool(line)
            else:
                value = None
        finally:
            file.close()
        return index, value
