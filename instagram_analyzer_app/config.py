WTF_CSRF_ENABLED = True
SECRET_KEY = "makesureyouupdateinpr0duction"
base_url = "https://api.instagram.com/v1"
cols = [
    'user.username',
    'caption.text',
    'tags',
    'comments.count',
    'likes.count',
    'filter',
    'type',
    'created_time',
    'user.full_name',
    'user.id',
    'link',
    'location.latitude',
    'location.longitude'
]