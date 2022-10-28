from django.core.exceptions import ValidationError


def get_path_upload_avatar(instance, file):
    """Путь к аватару пользователя"""
    """(media)/avatar/user_id/photo.jpg"""
    return f'avatar/user_{instance.id}/{file}'


def get_path_upload_cover_album(instance, file):
    """Путь к фото альбома"""
    """(media)/album/user_id/photo.jpg"""
    return f'album/user_{instance.id}/{file}'


def get_path_upload_cover_playlist(instance, file):
    """Путь к фото плейлиста"""
    """(media)/playlist/user_id/photo.jpg"""
    return f'playlist/user_{instance.id}/{file}'


def get_path_upload_track(instance, file):
    """Путь к песне"""
    """(media)/track/user_id/music.mp3"""
    return f'track/user_{instance.id}/{file}'


def validate_size_image(file_obj):
    """Проверка размера файла"""
    megabyte_limit = 2
    if file_obj.size > megabyte_limit * 1024 * 1024:
        raise ValidationError(f"Максимальный размер файла {megabyte_limit}")