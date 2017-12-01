from django.contrib import admin
from Insta_Web.models import InstagramAccounts,TargetFunctionalityDB,AccountDetails,MessageFunctionalityDB

class InstagramAdmin(admin.ModelAdmin):
    list_display = ('username', 'instagram_username', 'instagram_account_status', 'paid_date')

class InstagramTarget(admin.ModelAdmin):
    list_display = ('username', 'instagram_username', 'target', 'target_value' , 'pid')


class AccountInfo(admin.ModelAdmin):
    list_display = ('username', 'instagram_username', 'likes', 'following' , 'messages_sent')

class InstagramMessages(admin.ModelAdmin):
    list_display = ('username', 'instagram_username', 'messages_sent', 'status' , 'pid')

admin.site.register(InstagramAccounts, InstagramAdmin)

admin.site.register(TargetFunctionalityDB, InstagramTarget)

admin.site.register(AccountDetails,AccountInfo)

admin.site.register(MessageFunctionalityDB,InstagramMessages)


