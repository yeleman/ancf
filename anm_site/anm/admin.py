
from django.contrib import admin
from models import (Member, Report, Organization_chart, News, Newsletter,
                    TypeReport, TypePost, TextStatic)

admin.site.register(TextStatic)
admin.site.register(Member)
admin.site.register(TypePost)
admin.site.register(Organization_chart)
admin.site.register(Report)
admin.site.register(TypeReport)
admin.site.register(News)
admin.site.register(Newsletter)
