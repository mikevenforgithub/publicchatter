from django.contrib import admin
from .models import User
from .models import Tweet
from .models import Comment
from .models import Following
from .models import Like
# Register your models here.


admin.site.register(User)
admin.site.register(Tweet)
admin.site.register(Comment)
admin.site.register(Following)
admin.site.register(Like)