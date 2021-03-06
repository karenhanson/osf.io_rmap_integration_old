# -*- coding: utf-8 -*-
"""OSF mailing utilities.

Email templates go in website/templates/emails
Templates must end in ``.txt.mako`` for plaintext emails or``.html.mako`` for html emails.

You can then create a `Mail` object given the basename of the template and
the email subject. ::

    CONFIRM_EMAIL = Mail(tpl_prefix='confirm', subject="Confirm your email address")

You can then use ``send_mail`` to send the email.

Usage: ::

    from website import mails
    ...
    mails.send_mail('foo@bar.com', mails.CONFIRM_EMAIL, user=user)

"""
import os
import logging

from mako.lookup import TemplateLookup, Template

from framework.email import tasks
from website import settings

logger = logging.getLogger(__name__)

EMAIL_TEMPLATES_DIR = os.path.join(settings.TEMPLATES_PATH, 'emails')

_tpl_lookup = TemplateLookup(
    directories=[EMAIL_TEMPLATES_DIR],
)

TXT_EXT = '.txt.mako'
HTML_EXT = '.html.mako'


class Mail(object):
    """An email object.

    :param str tpl_prefix: The template name prefix.
    :param str subject: The subject of the email.
    :param iterable categories: Categories to add to the email using SendGrid's
        SMTPAPI. Used for email analytics.
        See https://sendgrid.com/docs/User_Guide/Statistics/categories.html
    """

    def __init__(self, tpl_prefix, subject, categories=None):
        self.tpl_prefix = tpl_prefix
        self._subject = subject
        self.categories = categories

    def html(self, **context):
        """Render the HTML email message."""
        tpl_name = self.tpl_prefix + HTML_EXT
        return render_message(tpl_name, **context)

    def text(self, **context):
        """Render the plaintext email message"""
        tpl_name = self.tpl_prefix + TXT_EXT
        return render_message(tpl_name, **context)

    def subject(self, **context):
        return Template(self._subject).render(**context)


def render_message(tpl_name, **context):
    """Render an email message."""
    tpl = _tpl_lookup.get_template(tpl_name)
    return tpl.render(**context)


def send_mail(to_addr, mail, mimetype='plain', from_addr=None, mailer=None,
            username=None, password=None, callback=None, **context):
    """Send an email from the OSF.
    Example: ::

        from website import mails

        mails.send_email('foo@bar.com', mails.TEST, name="Foo")

    :param str to_addr: The recipient's email address
    :param Mail mail: The mail object
    :param str mimetype: Either 'plain' or 'html'
    :param function callback: celery task to execute after send_mail completes
    :param **context: Context vars for the message template

    .. note:
         Uses celery if available
    """

    from_addr = from_addr or settings.FROM_EMAIL
    mailer = mailer or tasks.send_email
    subject = mail.subject(**context)
    message = mail.text(**context) if mimetype in ('plain', 'txt') else mail.html(**context)
    # Don't use ttls and login in DEBUG_MODE
    ttls = login = not settings.DEBUG_MODE
    logger.info('Sending email...')
    logger.info(u'To: {to_addr}\nFrom: {from_addr}\nSubject: {subject}\nMessage: {message}'.format(**locals()))

    kwargs = dict(
        from_addr=from_addr,
        to_addr=to_addr,
        subject=subject,
        message=message,
        mimetype=mimetype,
        ttls=ttls,
        login=login,
        username=username,
        password=password,
        categories=mail.categories,
    )

    if settings.USE_EMAIL:
        if settings.USE_CELERY:
            return mailer.apply_async(kwargs=kwargs, link=callback)
        else:
            ret = mailer(**kwargs)
            if callback:
                callback()

            return ret

# Predefined Emails

TEST = Mail('test', subject='A test email to ${name}', categories=['test'])

EXTERNAL_LOGIN_CONFIRM_EMAIL_CREATE = Mail('external_confirm_create', subject='Open Science Framework Account Verification')
EXTERNAL_LOGIN_CONFIRM_EMAIL_LINK = Mail('external_confirm_link', subject='Open Science Framework Account Verification')
EXTERNAL_LOGIN_LINK_SUCCESS = Mail('external_confirm_success', subject='Open Science Framework Account Verification Success')

INITIAL_CONFIRM_EMAIL = Mail('initial_confirm', subject='Open Science Framework Account Verification')
CONFIRM_EMAIL = Mail('confirm', subject='Add a new email to your OSF account')
CONFIRM_EMAIL_PREREG = Mail('confirm_prereg', subject='Open Science Framework Account Verification, Preregistration Challenge')
CONFIRM_EMAIL_ERPC = Mail('confirm_erpc', subject='Open Science Framework Account Verification, Election Research Preacceptance Competition')
CONFIRM_EMAIL_PREPRINTS_OSF = Mail('confirm_preprints_osf', subject='Open Science Framework Account Verification, Preprints Service')

CONFIRM_MERGE = Mail('confirm_merge', subject='Confirm account merge')

REMOVED_EMAIL = Mail('email_removed', subject='Email address removed from your OSF account')
PRIMARY_EMAIL_CHANGED = Mail('primary_email_changed', subject='Primary email changed')

INVITE_DEFAULT = Mail('invite_default', subject='You have been added as a contributor to an OSF project.')
INVITE_PREPRINT = Mail('invite_preprint', subject='You have been added as a contributor to an OSF preprint.')

CONTRIBUTOR_ADDED_DEFAULT = Mail('contributor_added_default', subject='You have been added as a contributor to an OSF project.')
CONTRIBUTOR_ADDED_PREPRINT = Mail('contributor_added_preprint', subject='You have been added as a contributor to an OSF preprint.')

FORWARD_INVITE = Mail('forward_invite', subject='Please forward to ${fullname}')
FORWARD_INVITE_REGISTERED = Mail('forward_invite_registered', subject='Please forward to ${fullname}')

FORGOT_PASSWORD = Mail('forgot_password', subject='Reset Password')
PASSWORD_RESET = Mail('password_reset', subject='Your OSF password has been reset')
PENDING_VERIFICATION = Mail('pending_invite', subject='Your account is almost ready!')
PENDING_VERIFICATION_REGISTERED = Mail('pending_registered', subject='Received request to be a contributor')

REQUEST_EXPORT = Mail('support_request', subject='[via OSF] Export Request')
REQUEST_DEACTIVATION = Mail('support_request', subject='[via OSF] Deactivation Request')

CONFERENCE_SUBMITTED = Mail(
    'conference_submitted',
    subject='Project created on Open Science Framework',
)
CONFERENCE_INACTIVE = Mail(
    'conference_inactive',
    subject='Open Science Framework Error: Conference inactive',
)
CONFERENCE_FAILED = Mail(
    'conference_failed',
    subject='Open Science Framework Error: No files attached',
)

DIGEST = Mail(
    'digest', subject='OSF Notifications',
    categories=['notifications', 'notifications-digest']
)
TRANSACTIONAL = Mail(
    'transactional', subject='OSF: ${subject}',
    categories=['notifications', 'notifications-transactional']
)

# Retraction related Mail objects
PENDING_RETRACTION_ADMIN = Mail(
    'pending_retraction_admin',
    subject='Withdrawal pending for one of your projects.'
)
PENDING_RETRACTION_NON_ADMIN = Mail(
    'pending_retraction_non_admin',
    subject='Withdrawal pending for one of your projects.'
)
# Embargo related Mail objects
PENDING_EMBARGO_ADMIN = Mail(
    'pending_embargo_admin',
    subject='Registration pending for one of your projects.'
)
PENDING_EMBARGO_NON_ADMIN = Mail(
    'pending_embargo_non_admin',
    subject='Registration pending for one of your projects.'
)
# Registration related Mail Objects
PENDING_REGISTRATION_ADMIN = Mail(
    'pending_registration_admin',
    subject='Registration pending for one of your projects.'
)
PENDING_REGISTRATION_NON_ADMIN = Mail(
    'pending_registration_non_admin',
    subject='Registration pending for one of your projects.'
)
PENDING_EMBARGO_TERMINATION_ADMIN = Mail(
    'pending_embargo_termination_admin',
    subject='Request to end an embargo early for one of your projects.'
)
PENDING_EMBARGO_TERMINATION_NON_ADMIN = Mail(
    'pending_embargo_termination_non_admin',
    subject='Request to end an embargo early for one of your projects.'
)

FILE_OPERATION_SUCCESS = Mail(
    'file_operation_success',
    subject='Your ${action} has finished',
)
FILE_OPERATION_FAILED = Mail(
    'file_operation_failed',
    subject='Your ${action} has failed',
)

UNESCAPE = '<% from website.util.sanitize import unescape_entities %> ${unescape_entities(src.title)}'
PROBLEM_REGISTERING = 'Problem registering ' + UNESCAPE
PROBLEM_REGISTERING_STUCK = PROBLEM_REGISTERING + '- Stuck Registration'

ARCHIVE_SIZE_EXCEEDED_DESK = Mail(
    'archive_size_exceeded_desk',
    subject=PROBLEM_REGISTERING
)
ARCHIVE_SIZE_EXCEEDED_USER = Mail(
    'archive_size_exceeded_user',
    subject=PROBLEM_REGISTERING
)

ARCHIVE_COPY_ERROR_DESK = Mail(
    'archive_copy_error_desk',
    subject=PROBLEM_REGISTERING
)
ARCHIVE_COPY_ERROR_USER = Mail(
    'archive_copy_error_user',
    subject=PROBLEM_REGISTERING

)
ARCHIVE_FILE_NOT_FOUND_DESK = Mail(
    'archive_file_not_found_desk',
    subject=PROBLEM_REGISTERING
)
ARCHIVE_FILE_NOT_FOUND_USER = Mail(
    'archive_file_not_found_user',
    subject='Registration failed because of altered files'
)

ARCHIVE_UNCAUGHT_ERROR_DESK = Mail(
    'archive_uncaught_error_desk',
    subject=PROBLEM_REGISTERING
)

ARCHIVE_REGISTRATION_STUCK_DESK = Mail(
    'archive_registration_stuck_desk',
    subject=PROBLEM_REGISTERING_STUCK
)

ARCHIVE_UNCAUGHT_ERROR_USER = Mail(
    'archive_uncaught_error_user',
    subject=PROBLEM_REGISTERING
)

ARCHIVE_SUCCESS = Mail(
    'archive_success',
    subject='Registration of ' + UNESCAPE + ' complete'
)

WELCOME = Mail(
    'welcome',
    subject='Welcome to the Open Science Framework'
)

WELCOME_OSF4I = Mail(
    'welcome_osf4i',
    subject='Welcome to the Open Science Framework'
)

PREREG_CHALLENGE_REJECTED = Mail(
    'prereg_challenge_rejected',
    subject='Revisions required, your submission for the Preregistration Challenge is not yet registered'
)

PREREG_CHALLENGE_ACCEPTED = Mail(
    'prereg_challenge_accepted',
    subject='Your research plan has been registered and accepted for the Preregistration Challenge'
)

EMPTY = Mail('empty', subject='${subject}')
