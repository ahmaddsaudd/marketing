from django.contrib import admin
from .models import Users, BackgroundTasks, Tags, Response, TaggedResponses, Results

admin.site.register(Users)
admin.site.register(BackgroundTasks)
admin.site.register(Tags)
admin.site.register(Response)
admin.site.register(TaggedResponses)
admin.site.register(Results)
