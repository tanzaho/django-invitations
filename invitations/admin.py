from django.contrib import admin

from .models import Invitation
from .forms import InvitationAdminAddForm, InvitationAdminChangeForm


class InvitationAdmin(admin.ModelAdmin):
    list_display = ('email', 'sent', 'accepted', 'confirmed', 'want_mails')
    actions = ['switchReceiveMailTrue', 'switchReceiveMailFalse']

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            kwargs['form'] = InvitationAdminChangeForm
        else:
            kwargs['form'] = InvitationAdminAddForm
            kwargs['form'].user = request.user
            kwargs['form'].request = request
        return super(InvitationAdmin, self).get_form(request, obj, **kwargs)

    def switchReceiveMailTrue(self, request, queryset):
        for invitation in queryset:
            if invitation.email != '91decf@gmail.com':
                invitation.want_mails = True;
                invitation.save()
        self.message_user(request, "%s invitations successfully turned to True." % len(queryset))
    switchReceiveMailTrue.short_description = "Turn 'want mail' to True"

    def switchReceiveMailFalse(self, request, queryset):
        for invitation in queryset:
            if invitation.email != '91decf@gmail.com':
                invitation.want_mails = False;
                invitation.save()
        self.message_user(request, "%s invitations successfully turned to False." % len(queryset))
    switchReceiveMailFalse.short_description = "Turn 'want mail' to False"


admin.site.register(Invitation, InvitationAdmin)
