# -*- coding: utf-8 -*-
import re
from five import grok
from cgi import escape
from Acquisition import aq_inner

from zope.schema import TextLine, Text, ValidationError
from z3c.form import field, button
from plone.directives import form

from plone.formwidget.recaptcha.widget import ReCaptchaFieldWidget

from Products.CMFPlone.utils import safe_unicode
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.interfaces import IPloneSiteRoot

from genweb.alternatheme.browser.interfaces import IGenwebTheme

from genweb.core.utils import genweb_config
from zope.component import getMultiAdapter


grok.templatedir("views_templates")


MESSAGE_TEMPLATE = u"""\
Heu rebut aquest correu perquè en/na %(name)s (%(from_address)s) ha enviat \
comentaris sobre l'espai Genweb que administreu a \

%(genweb)s

El missatge és:

%(message)s
--
%(from_name)s
"""


# Define a validation method for email addresses
class NotAnEmailAddress(ValidationError):
    __doc__ = _(u"Invalid email address")

check_email = re.compile(r"[a-zA-Z0-9._%-]+@([a-zA-Z0-9-]+\.)*[a-zA-Z]{2,4}").match


def validate_email(value):
    if not check_email(value):
        raise NotAnEmailAddress(value)
    return True


class IContactForm(form.Schema):
    """Define the fields of our form
    """

    nombre = TextLine(title=_('genweb_sender_fullname', default=u"Name"),
                      required=True)

    from_address = TextLine(title=_('genweb_sender_from_address', default=u"E-Mail"),
                            required=True,
                            constraint=validate_email)

    asunto = TextLine(title=_('genweb_subject', default="Subject"),
                      required=True)

    mensaje = Text(title=_('genweb_message', default="Message"),
                   description=_("genweb_help_message", default="Please enter the message you want to send."),
                   required=True)

    captcha = TextLine(title=_('genweb_type_the_code', default="Type the code"),
                       description=_('genweb_help_type_the_code', default="Type the code from the picture shown below"),
                       required=True)


class ContactForm(form.Form):
    grok.name('contact')
    grok.context(IPloneSiteRoot)
    grok.template("contact")
    grok.require('zope2.View')
    grok.layer(IGenwebTheme)

    ignoreContext = True

    fields = field.Fields(IContactForm)
    fields['captcha'].widgetFactory = ReCaptchaFieldWidget

    # This trick hides the editable border and tabs in Plone
    def update(self):
        self.request.set('disable_border', True)
        super(ContactForm, self).update()

    @button.buttonAndHandler(_(u"Send"))
    def action_send(self, action):
        """Send the email to the configured mail address in properties and redirect to the
        front page, showing a status message to say the message was received.
        """
        data, errors = self.extractData()
        if 'recaptcha_response_field' in self.request.keys():
            # Verify the user input against the captcha
            if self.context.restrictedTraverse('@@recaptcha').verify():
                pass
            else:
                return
        else:
            return

        if not 'asunto' in data or \
           not 'from_address' in data or \
           not 'mensaje' in data or \
           not 'nombre' in data:
            return

        context = aq_inner(self.context)
        mailhost = getToolByName(context, 'MailHost')
        urltool = getToolByName(context, 'portal_url')
        portal = urltool.getPortalObject()
        email_charset = portal.getProperty('email_charset')

        to_address = portal.getProperty('email_from_address')
        from_name = portal.getProperty('email_from_name')


        source = "%s <%s>" % (escape(safe_unicode(data['nombre'])), escape(safe_unicode(data['from_address'])))
        subject = "[Formulari Contacte] %s" % (escape(safe_unicode(data['asunto'])))
        message = MESSAGE_TEMPLATE % dict(name=data['nombre'],
                                          from_address=data['from_address'],
                                          genweb=portal.absolute_url(),
                                          message=data['mensaje'],
                                          from_name=from_name)

        mailhost.secureSend(escape(safe_unicode(message)), to_address, source,
                            subject=subject, subtype='plain',
                            charset=email_charset, debug=False,
                            )

        confirm = _(u"Mail sent.")
        IStatusMessage(self.request).addStatusMessage(confirm, type='info')

        self.request.response.redirect('contact_feedback')

        return ''

    def pref_lang(self):
        """ Extracts the current language for the current user
        """
        lt = getToolByName(self.context, 'portal_languages')
        return lt.getPreferredLanguage()

    def getURLDirectori(self, codi):
        return "http://directori.upc.edu/directori/dadesUE.jsp?id=%s" % codi

    def getURLMaps(self, codi):
        return "//maps.upc.edu/new/index.php/embed?iu=%s" % codi

    def getContactPersonalized (self):
        not_customized = not genweb_config().contacte_BBDD_or_page
        return not_customized

    def getContactPage (self):
        """
        Funcio que retorna la pagina de contacte personalitzada. Te en compte els permissos de lusuari validat, amb un
        restrictedTraverse sobre lobjecte (tenint en compte lidioma)
        """
        page = {}
        portal_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_portal_state')
        portal = portal_state.portal()
        context = aq_inner(self.context)
        isCustomized = getattr(context, 'contactepersonalitzat', False)

        if isCustomized:
            FrontPageObj = portal.contactepersonalitzat.getTranslation()
            page['body'] = FrontPageObj.CookedBody()
            return page
        else:
            page['body'] = ""
            return page
