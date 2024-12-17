import os
import uuid
from django.core.files.storage import default_storage
from django.conf import settings

class FileService:
    @staticmethod
    def upload_file(file, base_path='uploads/'):
        """
        通用檔案上傳方法
        :param file: 上傳的檔案物件
        :param base_path: 儲存的基本路徑
        :return: 檔案的相對路徑
        """
        # 生成唯一檔名
        filename = f"{uuid.uuid4()}_{file.name}"
        file_path = os.path.join(base_path, filename)
        
        # 儲存檔案
        saved_path = default_storage.save(file_path, file)
        return saved_path

    @staticmethod
    def delete_file(file_path):
        """
        刪除檔案
        :param file_path: 要刪除的檔案路徑
        """
        if default_storage.exists(file_path):
            default_storage.delete(file_path)

    @staticmethod
    def get_file_url(file_path):
        """
        取得檔案的完整 URL
        :param file_path: 檔案路徑
        :return: 檔案的完整 URL
        """
        return default_storage.url(file_path)