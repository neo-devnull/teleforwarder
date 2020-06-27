def get_media_type(message):
    if message.photo:
        return 'photo'
    if message.video:
        return 'video'
    if message.audio:
        return 'audio'
    if message.video_note:
        return 'video_note'
    if message.voice:
        return 'voice'
    if message.gif:
        return 'gif'
    if message.sticker:
        return 'sticker'
    if message.web_preview:
        return 'web_preview'

