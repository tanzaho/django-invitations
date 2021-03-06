##Django-invitations - Generic invitations app

[![Build Status](https://travis-ci.org/bee-keeper/django-invitations.svg?branch=master)](https://travis-ci.org/bee-keeper/django-invitations)

[![Coverage Status](https://coveralls.io/repos/bee-keeper/django-invitations/badge.svg?branch=master&service=github)](https://coveralls.io/github/bee-keeper/django-invitations?branch=master)

###About
Generic invitations solution with adaptable backend and support for django-allauth.  All emails and messages are fully customisable.

Originally written as an invitations solution for the excellent [django-allauth](https://github.com/pennersr/django-allauth), this app has been refactored to remove the allauth dependency whilst retaining 100% backwards compatibility.

Generic Invitation flow:

* Priviledged user invites prospective user by email (via either Django admin, form post, JSON post or programmatically)
* User receives invitation email with confirmation link
* User clicks link and is redirected to a preconfigured url (default is accounts/signup)


Allauth Invitation flow:

* As above but..
* User clicks link, their email is confirmed and they are redirected to signup
* The signup URL has the email prefilled and upon signing up the user is logged into the site


###Generic Installation

```
pip install django-invitations

# Add to settings.py, INSTALLED_APPS
'invitations',

# Append to urls.py
url(r'^invitations/', include('invitations.urls', namespace='invitations')),
```

###Allauth Integration

As above but note that invitations must come after allauth in the INSTALLED_APPS

```
# Add to settings.py
ACCOUNT_ADAPTER = 'invitations.models.InvitationsAdapter'
```

###Sending Invites

```
# inviter argument is optional
invite = Invitation.create('email@example.com', inviter=request.user)
invite.send_invitation(request)
```

To send invites via django admin, just add an invite and save.


###Bulk Invites

Bulk invites are supported via JSON.  Post a list of comma separated emails to the dedicated URL and Invitations will return a data object containing a list of valid and invalid invitations.


###Testing

`python manage.py test` or `tox`

###Additional Configuration

**INVITATIONS_INVITATION_EXPIRY** (default=3)

Integer.  How many days before the invitation expires.

**INVITATIONS_INVITATION_ONLY** (default=False)

Boolean.  If the site is invite only, or open to all.

**ALLOW_JSON_INVITES** (default=False)

Expose a URL for authenticated posting of invitees

**INVITATIONS_SIGNUP_REDIRECT** (default='account_signup')

URL name of your signup URL.

**INVITATIONS_ADAPTER** (default='invitations.adapters.BaseInvitationsAdapter')

Used for custom integrations.  ACCOUNT_ADAPTER overrides this setting

###Signals

The following signals are emitted:

* `invite_url_sent`
* `invite_accepted`


###Management Commands
Expired and accepted invites can be cleared as so:

`python manage.py clear_expired_invitations`
