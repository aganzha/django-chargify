from chargify_settings import CHARGIFY, CHARGIFY_CC_TYPES
from datetime import datetime
from decimal import Decimal
from django.contrib.auth.models import User
from django.db import models
from django.utils.datetime_safe import new_datetime
from pychargify.api import ChargifyNotFound
import logging
import time
import traceback
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import dateutil.parser
import json
import requests
from requests.auth import HTTPBasicAuth

log = logging.getLogger("chargify")
#logging.basicConfig(level=logging.DEBUG)
log.debug("Loaded chargify/models.py from aganzha. Force!-")

def unique_reference(prefix = ''):
    return '%s%i' %(prefix, time.time()*1000)

class ChargifyBaseModel(object):
    """ You can change the gateway/subdomain used by
    changing the gateway on an instantiated object """
    gateway = CHARGIFY

    def _api(self):
        raise NotImplementedError()
    api = property(_api)

    def _from_cents(self, value):
        return Decimal(str(float(value)/float(100)))

    def _in_cents(self, value):
        return Decimal(str(float(value)*float(100)))

    def update(self):
        raise NotImplementedError()

    def disable(self, commit=True):
        self.active = False
        if commit:
            self.save()

    def enable(self, commit=True):
        self.active = True
        if commit:
            self.save()

class ChargifyBaseManager(models.Manager):
    def _gateway(self):
        return self.model.gateway
    gateway = property(_gateway)

    def _api(self):
        raise NotImplementedError()
    api = property(_api)

    def _check_api(self):
        if self.api is None:
            raise ValueError('Blank API Not Set on Manager')

    def get_or_load(self, chargify_id):
        self._check_api()
        val = None
        loaded = False
        try:
            val = self.get(chargify_id = chargify_id)
            loaded = False
        except:
            pass
        finally:
            if val is None:
                api = self.api.getById(chargify_id)
                val = self.model().load(api)
                loaded = True
        return val, loaded

    def load_and_update(self, chargify_id):
        self._check_api()
        val, loaded = self.get_or_load(chargify_id)
        if not loaded:
            val.update()
        return val

    def reload_all(self):
        self._check_api()
        items = self.api.getAll()
        for item in items:
            val = self.load_and_update(item.id)
            val.save()

class CustomerManager(ChargifyBaseManager):
    def _api(self):
        return self.gateway.Customer()
    api = property(_api)



def toAscii(value):
    if value is None:
        return ''
    retval = value.encode('ascii', errors='ignore')
    if len(retval)==0:
        for ch in value:
            if ch == ' ':
                retval+=' '
            else:
                retval +='X'
    return retval



class Customer(models.Model, ChargifyBaseModel):
    """ The following are mapped fields:
        first_name = User.first_name (required)
        last_name = User.last_name (required)
        email = User.email (required)
        reference = Customer.id
    """
    chargify_id = models.IntegerField(null=True, blank=False, unique=True)
    user = models.ForeignKey(User)
    _first_name = models.CharField(max_length = 50, null=True, blank=False)
    _last_name = models.CharField(max_length = 50, null = True, blank=False)
    _email = models.EmailField(null=True, blank=False)
    _reference = models.CharField(max_length = 50, null=True, blank=True)
    organization = models.CharField(max_length = 75, null=True, blank=True)
    active = models.BooleanField(default=True)

    # Read only chargify fields
    chargify_created_at = models.DateTimeField(null=True)
    chargify_updated_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomerManager()

    def full_name(self):
        if not self.last_name:
            return self.first_name
        else:
            return '%s %s' %(self.first_name, self.last_name)

    def __unicode__(self):
        return self.full_name() + u' - ' + str(self.chargify_id)

    def _get_first_name(self):
        if self._first_name is not None:
            return self._first_name
        return self.user.first_name
    def _set_first_name(self, first_name):
        if self.user.first_name != first_name:
            self._first_name = first_name
    first_name = property(_get_first_name, _set_first_name)

    def _get_last_name(self):
        if self._last_name is not None:
            return self._last_name
        return self.user.last_name
    def _set_last_name(self, last_name):
        if self.user.last_name != last_name:
            self._last_name = last_name
    last_name = property(_get_last_name, _set_last_name)

    def _get_email(self):
        if self._email is not None:
            return self._email
        return self.user.email
    def _set_email(self, email):
        if self.user.email != email:
            self._email = email
    email = property(_get_email, _set_email)

    def _get_reference(self):
        """ You must save the customer before you can get the reference number"""
        if getattr(settings, 'DEVELOPMENT', False) and not self._reference:
            self._reference = unique_reference()

        if self._reference:
            return self._reference
        elif self.id:
            return self.id
        else:
            return ''
    def _set_reference(self, reference):
        self._reference = str(reference)
    reference = property(_get_reference, _set_reference)

    def save(self, save_api = False, **kwargs):
        if save_api:
            if not self.id:
                super(Customer, self).save(**kwargs)
            saved = False
            try:
                saved, customer = self.api.save()
            except ChargifyNotFound, e:
                for error in e.errors:
                    log.exception(error)
                api = self.api
                api.id = None
                saved, customer = api.save()

            if saved:
                log.debug("Customer Saved")
                return self.load(customer, commit=True) # object save happens after load
            else:
                log.debug("Customer Not Saved")
                log.debug(customer)
        self.user.save()
        return super(Customer, self).save(**kwargs)

    def delete(self, save_api = False, commit = True, *args, **kwargs):
        if save_api:
            self.api.delete()
        if commit:
            super(Customer, self).delete(*args, **kwargs)
        else:
            self.update()

    def load(self, api, commit=True):
        if self.id or self.chargify_id:# api.modified_at > self.chargify_updated_at:
            customer = self
        else:
#            log.debug('Not loading api')
            customer = Customer()
        log.debug('Loading Customer API: %s' %(api))
        customer.chargify_id = int(api.id)
        try:
            if customer.user:
                customer.first_name = api.first_name
                customer.last_name = api.last_name
                customer.email = api.email
            else:
                raise User.DoesNotExist
        except User.DoesNotExist: #@UndefinedVariable
            try:
                # user = User.objects.get(email=api.email)
                # aganzha
                user = User.objects.get(username=api.email)
            except:
                user = User(first_name = api.first_name, last_name = api.last_name, email = api.email, username = api.email)
                # aganzha
                log.debug('New user just created for subscription!: %s' %(user))
                user.save()
            customer.user = user
        customer.organization = api.organization
        customer.chargify_updated_at = api.modified_at
        customer.chargify_created_at = api.created_at
        if commit:
            customer.save()
        return customer

    def _gen_username(self, customer):
        """
        Create a unique username for the user
        """
        return("chargify_%s" % (self.id or customer.chargify_id))

    def update(self, commit = True):
        """ Update customer data from chargify """
        api = self.api.getById(self.chargify_id)
        return self.load(api, commit)

    def _api(self, node_name=None):
        """ Load data into chargify api object """
        customer = self.gateway.Customer()
        customer.id = str(self.chargify_id)
        customer.first_name = toAscii(self.first_name)
        customer.last_name = toAscii(self.last_name)
        customer.email = toAscii(self.email)
        customer.organization = toAscii(self.organization)
        customer.reference = str(self.reference)
        return customer
    api = property(_api)

class ProductManager(ChargifyBaseManager):
    def _api(self):
        return self.gateway.Product()
    api = property(_api)

    def reload_all(self):
        products = {}
        for product in self.gateway.Product().getAll():
            try:
                p, loaded = self.get_or_load(product.id)
                if not loaded:
                    p.update()
                p.save()
                products[product.handle] = p
            except:
                log.error('Failed to load product: %s' %(product))
                log.error(traceback.format_exc())

class Product(models.Model, ChargifyBaseModel):
    MONTH = 'month'
    DAY = 'day'
    INTERVAL_TYPES = (
          (MONTH, MONTH.title()),
          (DAY, DAY.title()),
          )
    chargify_id = models.IntegerField(null=True, blank=False, unique=True)
    price = models.DecimalField(decimal_places = 2, max_digits = 15, default=Decimal('0.00'))
    name = models.CharField(max_length=75)
    handle = models.CharField(max_length=75, default='')
    product_family = models.CharField(max_length=75, default='')
    accounting_code = models.CharField(max_length=300, null=True)
    interval_unit = models.CharField(max_length=10, choices = INTERVAL_TYPES, default=MONTH)
    interval = models.IntegerField(default=1)
    active = models.BooleanField(default=True)
    objects = ProductManager()

    trial_price_in_cents = models.IntegerField(default=0)
    trial_interval = models.IntegerField(default=2)
    trial_interval_unit = models.CharField(max_length=32, default='month')


    def __unicode__(self):
        s = ""
        if self.product_family is not None:
            s+= "(%s) " % self.product_family
        s+= self.name
        return s

    def _price_in_cents(self):
        return self._in_cents(self.price)
    def _set_price_in_cents(self, price):
        self.price = self._from_cents(price)
    price_in_cents = property(_price_in_cents, _set_price_in_cents)

    def _set_handle(self, handle):
        self.handle = str(handle)
    product_handle = property(handle, _set_handle)

    def _product_family_handle(self):
        return self.product_family.handle
    product_family_handle = property(_product_family_handle)

    def save(self, save_api = False, **kwargs):
        if save_api:
            try:
                saved, product = self.api.save()
                if saved:
                    return self.load(product, commit=True) # object save happens after load
            except:
                pass
#        self.api.save()
        return super(Product, self).save(**kwargs)

    def load(self, api, commit=True):
        self.chargify_id = int(api.id)
        self.price_in_cents = api.price_in_cents
        self.name = api.name
        self.handle = api.handle
        # aganzha
        # self.product_family = api.product_family
        if type(api.product_family) is str:
            self.product_family = api.product_family
        else:
            self.product_family = str(api.product_family.id)
        self.accounting_code = api.accounting_code
        self.interval_unit = api.interval_unit
        self.interval = api.interval
        if commit:
            self.save()
        return self

    def update(self, commit = True):
        """ Update customer data from chargify """
        api = self.api.getById(self.chargify_id)
        return self.load(api, commit = True)

    def _api(self):
        """ Load data into chargify api object """
        product = self.gateway.Product()
        product.id = str(self.chargify_id)
        product.price_in_cents = self.price_in_cents
        product.name = self.name
        product.handle = self.handle
        product.product_family = self.product_family
        product.accounting_code = self.accounting_code
        product.interval_unit = self.interval_unit
        product.interval = self.interval

        ignores = ['trial_price_in_cents','trial_interval','trial_interval_unit']
        print "....."
        if self.trial_interval:
            print "1"
            product.trial_price_in_cents = self.trial_price_in_cents
            product.trial_interval = self.trial_interval
            product.trial_interval_unit = self.trial_interval_unit
            product.__ignore__ = [i for i in product.__ignore__ if i not in ignores]
        else:
            print "2"
            product.__ignore__+=ignores
            print product.__ignore__
        print "paaaaaaaaaaaaaasas"
        return product

    api = property(_api)

class CreditCardManager(ChargifyBaseManager):
    def _api(self):
        return self.gateway.CreditCard()
    api = property(_api)

class CreditCard(models.Model, ChargifyBaseModel):
    """ This data should NEVER be saved in the database """
    CC_TYPES = CHARGIFY_CC_TYPES
    _full_number = ''
    ccv = ''

    first_name = models.CharField(max_length = 50, null=True, blank=False)
    last_name = models.CharField(max_length = 50, null=True, blank=False)
    masked_card_number = models.CharField(max_length=25, null=True)
    expiration_month = models.IntegerField(null=True, blank=True)
    expiration_year = models.IntegerField(null=True, blank=True)
    credit_type = models.CharField(max_length=25, null=True, blank=False, choices=CC_TYPES)
    billing_address = models.CharField(max_length=75, null=True, blank=False, default='')
    billing_city = models.CharField(max_length=75, null=True, blank=False, default='')
    billing_state = models.CharField(max_length=2, null=True, blank=False, default='')
    billing_zip = models.CharField(max_length=15, null=True, blank=False, default='')
    billing_country = models.CharField(max_length=75, null=True, blank=True, default='United States')
    active = models.BooleanField(default=True)
    objects = CreditCardManager()
    chargify_id = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        s = u''
        if self.first_name:
            s += unicode(self.first_name)
        if self.last_name:
            if s:
                s += u' '
            s += unicode(self.last_name)
        if self.masked_card_number:
            if s:
                s += u'-'
            s += unicode(self.masked_card_number)
        return s

    # you have to set the customer if there is no related subscription yet
    _customer = None
    def _get_customer(self):
        if self._customer:
            return self._customer
        try:
            return self.subscription.all().order_by('-updated_at')[0].customer
        except IndexError:
            return None
    def _set_customer(self, customer):
        self._customer = customer
    customer = property(_get_customer, _set_customer)

    def _get_full_number(self):
        return self._full_number
    def _set_full_number(self, full_number):
        self._full_number = full_number

        if len(full_number) > 4:
            self.masked_card_number = u'XXXX-XXXX-XXXX-' + full_number[-4:]
        else: #not a real CC number, probably a testing number
            self.masked_card_number = u'XXXX-XXXX-XXXX-1111'
    full_number = property(_get_full_number, _set_full_number)

    def save(self,  save_api = False, *args, **kwargs):
        if save_api:
            self.api.save()
        return super(CreditCard, self).save(*args, **kwargs)

    def delete(self, save_api = False, *args, **kwargs):
        if save_api:
            self.api.delete(self.subscription)
        return super(CreditCard, self).delete(*args, **kwargs)


    def load(self, api, commit=True):
        print "load credit caaaaaaaaaaard2!"
        if api is None:
            return self
        self.masked_card_number = api.masked_card_number
        self.expiration_month = api.expiration_month
        self.expiration_year = api.expiration_year
        self.credit_type = api.type
        self.chargify_id = api.id
        if commit:
            self.save(save_api = False)
        return self

    def update(self, commit=True):
        """ Update Credit Card data from chargify """
        print "updating credit card!"
        if self.subscription:
            print "yes!", self.subscription.update
            return self.subscription.update()
        else:
            return self

    def _existent_api(self, node_name=''):
        cc = self.gateway.ExistingCard()
        cc.id = self.chargify_id
        print "eeeeeeeeeeeeeeeeeeeeeeeee"
        print cc, cc.id
        return cc

    def _api(self, node_name = ''):
        """ Load data into chargify api object """
        cc = self.gateway.CreditCard()
        cc.first_name = toAscii(self.first_name)
        cc.last_name = toAscii(self.last_name)
        cc.full_number = self._full_number
        cc.expiration_month = self.expiration_month
        cc.expiration_year = self.expiration_year
        cc.ccv = self.ccv
        cc.billing_address = toAscii(self.billing_address)
        cc.billing_city = toAscii(self.billing_city)
        cc.billing_state = toAscii(self.billing_state)
        cc.billing_zip = toAscii(self.billing_zip)
        cc.billing_country = toAscii(self.billing_country)
        return cc
    api = property(_api)

class SubscriptionManager(ChargifyBaseManager):
    def _api(self):
        return self.gateway.Subscription()
    api = property(_api)

    def get_or_load_component(self, component):
        val = None
        loaded = False
        try:
            val = SubscriptionComponent.objects.get(
                component__id=component.id,
                subscription__id=subscription.id
            )
            loaded = False
        except:
            pass
        finally:
            if val is None:
                val = SubscriptionComponent().load(component)
                loaded = True
        return val, loaded

    def update_list(self, lst):
        for id in lst:
            sub= self.load_and_update(id)
            sub.save()

    def reload_all(self):
        """ You should only run this when you first install the product!
        VERY EXPENSIVE!!! """
        Product.objects.reload_all()
        Customer.objects.reload_all()
        for customer in Customer.objects.filter(active=True):
            subscriptions = self.api.getByCustomerId(str(customer.chargify_id))
            if not subscriptions:
                continue
            for subscription in subscriptions:
                try:
                    sub = self.get(chargify_id = subscription.id)
                except:
                    sub = self.model()
                    if not subscription.current_period_started_at:
                        subscription.current_period_started_at = datetime.now()
                    if not subscription.current_period_ends_at:
                        subscription.current_period_ends_at = datetime.now()

                    sub.load(subscription)
                sub.save()

class Subscription(models.Model, ChargifyBaseModel):
    TRIALING = 'trialing'
    ASSESSING = 'assessing'
    ACTIVE = 'active'
    SOFT_FAILURE = 'soft_failure'
    PAST_DUE = 'past_due'
    SUSPENDED = 'suspended'
    CANCELLED = 'canceled'
    EXPIRED = 'expired'
    UNPAID = 'unpaid'
    STATE_CHOICES = (
         (TRIALING, u'Trialing'),
         (ASSESSING, u'Assessing'),
         (ACTIVE, u'Active'),
         (SOFT_FAILURE, u'Soft Failure'),
         (PAST_DUE, u'Past Due'),
         (SUSPENDED, u'Suspended'),
         (CANCELLED, u'Cancelled'),
         (EXPIRED, u'Expired'),
         (UNPAID, u'Unpaid'),
         )
    chargify_id = models.IntegerField(null=True, blank=True, unique=True)
    state = models.CharField(max_length=15, null=True, blank=True, default='', choices=STATE_CHOICES)
    coupon_code = models.CharField(max_length=256, null=True, blank=True, default='')
    balance = models.DecimalField(decimal_places = 2, max_digits = 15, default=Decimal('0.00'))
    current_period_started_at = models.DateTimeField(null=True, blank=True)
    current_period_ends_at = models.DateTimeField(null=True, blank=True)
    trial_started_at = models.DateTimeField(null=True, blank=True)
    trial_ended_at = models.DateTimeField(null=True, blank=True)
    canceled_at = models.DateTimeField(null=True, blank=True)
    activated_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    customer = models.ForeignKey(Customer, null=True)
    product = models.ForeignKey(Product, null=True)
    credit_card = models.ForeignKey(CreditCard, related_name='subscription', null=True, blank=True)
    active = models.BooleanField(default=True)
    objects = SubscriptionManager()

    total_revenue = models.DecimalField(decimal_places = 2, max_digits = 15, default=Decimal('0.00'))


    def get_amount(self):
        return self.product.price


    def __unicode__(self):
        s = unicode(self.get_state_display())
        if self.product:
            s += u' ' + self.product.name
        if self.chargify_id:
            s += ' - ' + unicode(self.chargify_id)

        return s

    def _balance_in_cents(self):
        return self._in_cents(self.balance)
    def _set_balance_in_cents(self, value):
        self.balance = self._from_cents(value)
    balance_in_cents = property(_balance_in_cents, _set_balance_in_cents)


    def _total_revenue_in_cents(self):
        return self._in_cents(self.total_revenue)
    def _set_total_revenue_in_cents(self, value):
        self.total_revenue = self._from_cents(value)
    total_revenue_in_cents = property(_total_revenue_in_cents, _set_total_revenue_in_cents)


    def _customer_reference(self):
        return self.customer.reference
    customer_reference = property(_customer_reference)

    def _product_handle(self):
        return self.product.handle
    product_handle = property(_product_handle)

    def save(self, save_api = False, *args, **kwargs):
        if self.chargify_id is None:
            save_api = True
        if save_api:
            if self.customer.chargify_id is None:
                self.customer.save(save_api = True)
                customer = self.customer
                self.customer = customer
            if self.product and self.product.chargify_id is None:
                product = self.product.save(save_api = True)
                self.product = product
            api = self.api
            saved, subscription = api.save()
            if saved:
                return self.load(subscription, commit=True) # object save happens after load
        return super(Subscription, self).save(*args, **kwargs)


    def reactivate(self):
        self.last_activation_at = datetime.now()
        self.api.reactivate()
        self.update()

    def cancel_at_end_of_period(self):
        self.api.cancel_at_end_of_period()
        self.update(commit=True)

    def unsubscribe(self, message="", *args, **kwargs):
        self.api.unsubscribe(message=message)
        self.last_deactivation_at = datetime.now()
        self.update(commit=True)

    def delete(self, save_api = False, commit = True, message = None, *args, **kwargs):
        if save_api:
            self.api.delete(message=message)
        self.last_deactivation_at = datetime.now()
        if commit:
            super(Subscription, self).delete(*args, **kwargs)
        else:
            self.update()

    def load(self, api, commit=True):
        self.chargify_id = int(api.id)
        self.state = api.state
        self.balance_in_cents = api.balance_in_cents
        self.total_revenue = api.total_revenue_in_cents
        self.coupon_code = api.coupon_code

        try:
            self.current_period_started_at = new_datetime(api.current_period_started_at)
            self.current_period_ends_at = new_datetime(api.current_period_ends_at)
        except:
            # it could be none, if subscription is cancelled
            pass

        if api.trial_started_at:
            self.trial_started_at = new_datetime(api.trial_started_at)
        else:
            self.trial_started_at = None
        if api.trial_ended_at:
            self.trial_ended_at = new_datetime(api.trial_ended_at)
        else:
            self.trial_ended_at = None
        if api.canceled_at:
            self.canceled_at = new_datetime(api.canceled_at)
        else:
            self.canceled_at = None
        if api.activated_at:
            self.activated_at = new_datetime(api.activated_at)
        else:
            self.activated_at = None
        if api.expires_at:
            self.expires_at = new_datetime(api.expires_at)
        else:
            self.expires_at = None
        self.created_at = new_datetime(api.created_at)
        self.updated_at = new_datetime(api.updated_at)
        try:
            c = Customer.objects.get(chargify_id = api.customer.id)
        except:
            log.debug("cant get customer. will create new one! ")
            c = Customer()
            c = c.load(api.customer)

        self.customer = c

        try:
            p = Product.objects.get(chargify_id = api.product.id)
        except:
            log.debug("cant get product. will create new one! ")
            p = Product()
            p.load(api.product)
            p.save()
        self.product = p


        # aganzha ????
        # credit_card = CreditCard()
        # credit_card.load(api.credit_card, commit=commit)
        # self.credit_card = credit_card
        if self.credit_card:
            self.credit_card.load(api.credit_card)
            # credit_card = self.credit_card
        else:
            log.debug("cant get customer. will create new one!")
            credit_card = CreditCard()
            credit_card.load(api.credit_card)
            self.credit_card = credit_card
        if commit:
            self.save()
        return self

    def update(self, commit=True):
        """ Update Subscription data from chargify """
        subscription = self.gateway.Subscription().getBySubscriptionId(self.chargify_id)
        log.debug('Updating subscription (in models)')
        ld = None
        if subscription:
            ld = self.load(subscription, commit)
        try:
            Transaction.load_for_sub(ld)
        except:
            log.error(u'can not load chargify transactions for {}'.format(ld),exc_info=True)
        return ld

    def charge(self, amount, memo):
        """ Create a one-time charge """
        return self.api.charge(amount, memo)

    def next_billing_date(self):
        self.update(self.api.next_billing_date(self.current_period_ends_at))

    def preview_migration(self, product):
        return self.api.preview_migration(product.handle)

    def migrate(self, product):
        return self.update(self.api.migrate(product.handle))

    def upgrade(self, product):
        """ Upgrade / Downgrade products """
        return self.update(self.api.upgrade(product.handle))

    def _api(self):
        """ Load data into chargify api object """
        subscription = self.gateway.Subscription()
        if self.chargify_id:
            subscription.id = str(self.chargify_id)
        subscription.product = self.product.api
        subscription.product_handle = self.product_handle
        subscription.coupon_code = self.coupon_code
        # aganzha
        ccode = 'None'
        if subscription.coupon_code is not None:
            ccode = subscription.coupon_code
        if self.customer.chargify_id is None:
            subscription.customer = self.customer._api('customer_attributes')
        else:
            subscription.customer = self.customer._api('customer_id')
        # aganzha!
        # we sdave subsription with credit card only if user updates his credit card!
        # if it is, for example, plan upgrade, do not sent credit card!
        if self.credit_card:
            if self.credit_card.chargify_id:
                subscription.credit_card = self.credit_card._existent_api('payment_profile_id')
            else:
                subscription.credit_card = self.credit_card._api('credit_card_attributes')
        return subscription
    api = property(_api)

class Transaction(models.Model):
    chargify_id = models.IntegerField(null=True, blank=True, unique=True)
    type = models.CharField(max_length=32,db_index=True)
    kind = models.CharField(max_length=32, null=True, blank=True)
    success = models.NullBooleanField()
    amount_in_cents = models.IntegerField(default=0)
    refunded_amount_in_cents = models.IntegerField(default=0)
    created_at = models.DateTimeField()
    customer = models.ForeignKey(Customer,blank=True,null=True)
    product = models.ForeignKey(Product,blank=True,null=True)
    subscription = models.ForeignKey(Subscription,blank=True,null=True)
    memo = models.TextField(blank=True, null=True)
    dump = models.TextField(blank=True, null=True)
    parent_account = models.CharField(max_length=32,db_index=True,blank=True, null=True)
    sub_account = models.CharField(max_length=32,db_index=True,blank=True, null=True)
    
    @classmethod
    def load_for_sub(cls, subscription):
        host = settings.CHARGIFY_SUBDOMAIN + ".chargify.com"
        url = 'https://{}/subscriptions/{}/transactions.json'.format(host,subscription.chargify_id)
        r = requests.get(url, data={'per_page':1000},auth=HTTPBasicAuth(settings.CHARGIFY_API_KEY, 'x'))
        js = json.loads(r.text)
        for el in js:
            tr = cls.from_json(el.get('transaction'))
            tr.save()
            log.info(u'Saved transaction {} for sub: {}, customer: {}'.format(tr.chargify_id,tr.subscription,tr.customer))

    @classmethod
    def load_all(cls, min_id,page_size):
        host = settings.CHARGIFY_SUBDOMAIN + ".chargify.com"
        url = 'https://{}/transactions.json'.format(host)
        r = requests.get(url, data={'since_id':min_id,'per_page':page_size,'direction':'asc'},auth=HTTPBasicAuth(settings.CHARGIFY_API_KEY, 'x'))
        js = json.loads(r.text)
        for el in js:
            print "cycle"
            tr = cls.from_json(el.get('transaction'))
            tr.save()
            log.info(u'Saved transaction {} for sub: {}, customer: {}'.format(tr.chargify_id,tr.subscription,tr.customer))
            yield tr

    @classmethod
    def from_json(cls,js):
        try:
            tr = cls.objects.get(chargify_id=js.get('id'))
        except ObjectDoesNotExist:
            tr = Transaction()
            tr.chargify_id = js.get('id')
        tr.customer = None
        if 'customer_id' in js:
            try:
                tr.customer = Customer.objects.get(chargify_id=js.get('customer_id'))
            except ObjectDoesNotExist:
                log.debug(u'No customer {} for transaction {}'.format(js.get('customer_id'),tr.chargify_id))

        tr.subscription = None
        if 'subscription_id' in js:
            try:
                tr.subscription = Subscription.objects.get(chargify_id=js.get('subscription_id'))
            except ObjectDoesNotExist:
                log.debug(u'No subscription for {} for transaction {}'.format(js.get('subscription_id'),tr.chargify_id))
        tr.product = None
        if 'product_id' in js:
            try:
                tr.product = Product.objects.get(chargify_id=js.get('product_id'))
            except ObjectDoesNotExist:
                log.debug(u'No subscription for {} for transaction {}'.format(js.get('subscription_id'),tr.chargify_id))
        tr.amount_in_cents = js.get('amount_in_cents')
        tr.refunded_amount_in_cents = js.get('refunded_amount_in_cents',0)
        tr.created_at = dateutil.parser.parse(js.get('created_at'))
        tr.type = js.get('type')
        if tr.type == 'Refund':
            tr.amount_in_cents = 0 - tr.amount_in_cents
        tr.kind = js.get('kind')
        tr.dump = json.dumps(js)
        tr.memo = js.get('memo')
        tr.success = js.get('success', False)
        return tr
