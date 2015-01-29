# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Subscription'
        db.create_table(u'chargify_subscription', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('chargify_id', self.gf('django.db.models.fields.IntegerField')(unique=True, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(default='', max_length=15, null=True, blank=True)),
            ('coupon_code', self.gf('django.db.models.fields.CharField')(default='', max_length=256, null=True, blank=True)),
            ('balance', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=15, decimal_places=2)),
            ('current_period_started_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('current_period_ends_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('trial_started_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('trial_ended_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('activated_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('expires_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chargify.Customer'], null=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chargify.Product'], null=True)),
            ('credit_card', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='subscription', unique=True, null=True, to=orm['chargify.CreditCard'])),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('total_revenue', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=15, decimal_places=2)),
        ))
        db.send_create_signal(u'chargify', ['Subscription'])

        # Adding model 'Customer'
        db.create_table(u'chargify_customer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('chargify_id', self.gf('django.db.models.fields.IntegerField')(unique=True, null=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('_first_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('_last_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('_email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True)),
            ('_reference', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('chargify_created_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('chargify_updated_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'chargify', ['Customer'])

        # Adding model 'Product'
        db.create_table(u'chargify_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('chargify_id', self.gf('django.db.models.fields.IntegerField')(unique=True, null=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=15, decimal_places=2)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('handle', self.gf('django.db.models.fields.CharField')(default='', max_length=75)),
            ('product_family', self.gf('django.db.models.fields.CharField')(default='', max_length=75)),
            ('accounting_code', self.gf('django.db.models.fields.CharField')(max_length=300, null=True)),
            ('interval_unit', self.gf('django.db.models.fields.CharField')(default='month', max_length=10)),
            ('interval', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'chargify', ['Product'])

        # Adding model 'CreditCard'
        db.create_table(u'chargify_creditcard', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('masked_card_number', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('expiration_month', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('expiration_year', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('credit_type', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('billing_address', self.gf('django.db.models.fields.CharField')(default='', max_length=75, null=True)),
            ('billing_city', self.gf('django.db.models.fields.CharField')(default='', max_length=75, null=True)),
            ('billing_state', self.gf('django.db.models.fields.CharField')(default='', max_length=2, null=True)),
            ('billing_zip', self.gf('django.db.models.fields.CharField')(default='', max_length=15, null=True)),
            ('billing_country', self.gf('django.db.models.fields.CharField')(default='United States', max_length=75, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'chargify', ['CreditCard'])


    def backwards(self, orm):
        # Deleting model 'Subscription'
        db.delete_table(u'chargify_subscription')

        # Deleting model 'Customer'
        db.delete_table(u'chargify_customer')

        # Deleting model 'Product'
        db.delete_table(u'chargify_product')

        # Deleting model 'CreditCard'
        db.delete_table(u'chargify_creditcard')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'chargify.creditcard': {
            'Meta': {'object_name': 'CreditCard'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'billing_address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '75', 'null': 'True'}),
            'billing_city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '75', 'null': 'True'}),
            'billing_country': ('django.db.models.fields.CharField', [], {'default': "'United States'", 'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'billing_state': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2', 'null': 'True'}),
            'billing_zip': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15', 'null': 'True'}),
            'credit_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'expiration_month': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'expiration_year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'masked_card_number': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'})
        },
        u'chargify.customer': {
            'Meta': {'object_name': 'Customer'},
            '_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            '_first_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            '_last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            '_reference': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'chargify_created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'chargify_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True'}),
            'chargify_updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'chargify.product': {
            'Meta': {'object_name': 'Product'},
            'accounting_code': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'chargify_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True'}),
            'handle': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'interval_unit': ('django.db.models.fields.CharField', [], {'default': "'month'", 'max_length': '10'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '15', 'decimal_places': '2'}),
            'product_family': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '75'})
        },
        u'chargify.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'activated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'balance': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '15', 'decimal_places': '2'}),
            'chargify_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'coupon_code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'credit_card': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'subscription'", 'unique': 'True', 'null': 'True', 'to': u"orm['chargify.CreditCard']"}),
            'current_period_ends_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'current_period_started_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['chargify.Customer']", 'null': 'True'}),
            'expires_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['chargify.Product']", 'null': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'total_revenue': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '15', 'decimal_places': '2'}),
            'trial_ended_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'trial_started_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['chargify']