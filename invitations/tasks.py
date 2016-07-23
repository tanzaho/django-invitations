# -*- coding: utf-8 -*-
from django_rq import job, enqueue, get_queue, get_scheduler
from django.conf import settings
from django.template import loader, Context
from django.core.mail.message import EmailMessage
from datetime import timedelta
import logging

from .models import Invitation
from .app_settings import app_settings

logger = logging.getLogger(__name__)


def resend_inactive_invitations(invitation_id, ctx):
    logger.info('We added invitations to be sent to user. Should be sent in -')
    logger.info(app_settings.INVITATION_EXPIRY)
    try:
        scheduler = get_scheduler(name='default', interval=30)
    except:
        logger.info('Could not find scheduler')

    # Send two days before expiration
    scheduler.enqueue_in(timedelta(days=1), send_reminder, ctx['email'], 'invitation_reminder_24hrs', '[Elokenz] Invitation to discover Repost - Reminder', ctx, invitation_id)
    scheduler.enqueue_in(timedelta(days=2), send_reminder, ctx['email'], 'invitation_reminder_48hrs', '[Elokenz] Do you still want to discover Repost ?', ctx, invitation_id)
    scheduler.enqueue_in(timedelta(days=7), send_reminder, ctx['email'], 'invitation_reminder_7days', '[Elokenz] Are you still interested by Repost ?', ctx, invitation_id)

    scheduler.enqueue_in(timedelta(days=app_settings.INVITATION_EXPIRY - 2), send_reminder, ctx['email'], 'invitation_reminder_48hrs_left', '[Elokenz] Your invitation is expiring tomorrow', ctx, invitation_id)
    scheduler.enqueue_in(timedelta(days=app_settings.INVITATION_EXPIRY - 1), send_reminder, ctx['email'], 'invitation_reminder_24hrs_left', '[Elokenz] Your invitation is expiring today', ctx, invitation_id)


@job
def send_reminder(email, newsletter_name, title, ctx, invitation_id):
    """
    Sends a newsletter to email,
    Can also use AP splitting

    -- Parameters --
    email = "jice@gmail.com"
    newsletter_name = "step1"
    """
    logger.info('We prepare to send a reminder to :' + unicode(email))
    # If invitation has been accepted, don't do nothing
    invitation = Invitation.objects.get(id=invitation_id)
    if invitation.accepted:
        return

    #  Newsletter specific info (change them for each NL !!!!!!!)
    nl_folder = "invitations/email/" + str(newsletter_name)

    html_content = nl_folder + ".txt"
    # select the template by default first
    tpl_html = loader.select_template([html_content])

    # Rendering
    context = Context(ctx)
    html_content = tpl_html.render(context)

    # Sending email
    email = EmailMessage(subject=title, body=html_content, from_email=settings.JICE_FROM_EMAIL, to=[email], bcc=["jice@lavocat.name"])
    # email.content_subtype = "text/html"  # Main content is now text/html (or just html?)
    tag = newsletter_name
    email.tags = [tag]
    email.send()

    # Setting the flag to True
    logger.info('Reminder sent to :' + unicode(email))

