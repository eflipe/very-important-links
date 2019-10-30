from django.contrib import admin
from vil_app.models import Category, Page, UserProfile



class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'created_by')


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
