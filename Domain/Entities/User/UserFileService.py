from Infrastructure.Services.FileService import FileService

class UserFileService:
    @classmethod
    def handle_user_avatar_upload(cls, user, avatar_file):
        """
        處理用戶頭像上傳
        :param user: 用戶模型實例
        :param avatar_file: 上傳的頭像檔案
        :return: 頭像檔案路徑
        """
        # 如果已有舊頭像，先刪除
        if user._AvatarPath:
            FileService.delete_file(user._AvatarPath)
        
        # 上傳新頭像
        avatar_path = FileService.upload_file(
            avatar_file, 
            base_path='uploads/avatars/'
        )
        
        return avatar_path

    @classmethod
    def handle_user_document_upload(cls, user, document_file):
        """
        處理用戶文件上傳
        :param user: 用戶模型實例
        :param document_file: 上傳的文件
        :return: 文件檔案路徑
        """
        document_path = FileService.upload_file(
            document_file, 
            base_path='uploads/documents/'
        )
        
        return document_path