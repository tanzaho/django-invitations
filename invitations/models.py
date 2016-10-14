import datetime
from binascii import hexlify
import os

from django.db import models
from django.dispatch import receiver
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.encoding import python_2_unicode_compatible

from allauth.account.signals import user_signed_up

from .managers import InvitationManager
from .app_settings import app_settings
from .adapters import get_invitations_adapter
from . import signals


def _create_unsubscribe_slug():
    """
    """
    invitations_slug = Invitation.objects.all().values_list("unsubscribe_slug", flat=True)
    length_slug = 10
    slug = hexlify(os.urandom(length_slug))
    try:
        # Test if duplicates and update if necessary
        duplicate = slug in invitations_slug
        while duplicate:
            slug = hexlify(os.urandom(length_slug))
            duplicate = slug in invitations_slug
    except:
        pass

    return slug


@python_2_unicode_compatible
class Invitation(models.Model):

    email = models.EmailField(unique=True, verbose_name=_('e-mail address'))
    confirmed = models.BooleanField(verbose_name=_('confirmed'), default=False)
    accepted = models.BooleanField(verbose_name=_('clicked'), default=False)
    created = models.DateTimeField(verbose_name=_('created'),
                                   default=timezone.now)
    key = models.CharField(verbose_name=_('key'), max_length=64, unique=True)
    sent = models.DateTimeField(verbose_name=_('sent'), null=True)
    inviter = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True)

    unsubscribe_slug = models.SlugField(max_length=32, unique=True, default=_create_unsubscribe_slug)  # the unsubscribe token
    want_mails = models.BooleanField(default=True)

    objects = InvitationManager()

    @classmethod
    def create(cls, email, inviter=None):
        key = get_random_string(64).lower()
        instance = cls._default_manager.create(
            email=email,
            key=key,
            inviter=inviter)
        return instance

    def key_expired(self):
        expiration_date = (
            self.sent + datetime.timedelta(
                days=app_settings.INVITATION_EXPIRY))
        return expiration_date <= timezone.now()

    def send_invitation(self, request, **kwargs):
        current_site = (kwargs['site'] if 'site' in kwargs
                        else Site.objects.get_current())
        invite_url = reverse('invitations:accept-invite',
                             args=[self.key])
        invite_url = request.build_absolute_uri(invite_url)

        domain = Site.objects.get_current().domain
        unsubscribe_url = domain + reverse('invitations:unsubscribe_invitation', kwargs={"token": self.unsubscribe_slug})

        ctx = {
            'invite_url': invite_url,
            'site_name': current_site.name,
            'email': self.email,
            'key': self.key,
            'inviter': self.inviter,
            'unsubscribe_url': unsubscribe_url

        }

        email_template = 'invitations/email/email_invite'

        get_invitations_adapter().send_mail(
            email_template,
            self.email,
            ctx)
        self.sent = timezone.now()
        self.save()

        signals.invite_url_sent.send(
            sender=self.__class__,
            instance=self,
            invite_url_sent=invite_url,
            inviter=self.inviter)

        from .tasks import resend_inactive_invitations
        resend_inactive_invitations(self.pk, ctx)

    def __str__(self):
        return "Invite: {0}".format(self.email)


# here for backwards compatibility, historic allauth adapter
if hasattr(settings, 'ACCOUNT_ADAPTER'):
    if settings.ACCOUNT_ADAPTER == 'invitations.models.InvitationsAdapter':
        from allauth.account.adapter import DefaultAccountAdapter

        class InvitationsAdapter(DefaultAccountAdapter):

            def is_open_for_signup(self, request):
                if hasattr(request, 'session') and request.session.get(
                        'account_verified_email'):
                    return True
                elif app_settings.INVITATION_ONLY is True:
                    # Site is ONLY open for invites
                    return False
                else:
                    # Site is open to signup
                    return True


@receiver(user_signed_up, dispatch_uid="confirm_invitation")
def confirmInvitation(request, user, **kwargs):

    email = user.email
    try:
        invitation = Invitation.objects.get(email=email)
        invitation.confirmed = True
        invitation.save()
    except:
        pass
