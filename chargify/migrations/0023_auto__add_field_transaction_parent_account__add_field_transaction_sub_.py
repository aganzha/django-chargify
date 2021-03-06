# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Transaction.parent_account'
        db.add_column(u'chargify_transaction', 'parent_account',
                      self.gf('django.db.models.fields.CharField')(db_index=True, max_length=32, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Transaction.sub_account'
        db.add_column(u'chargify_transaction', 'sub_account',
                      self.gf('django.db.models.fields.CharField')(db_index=True, max_length=32, null=True, blank=True),
                      keep_default=False)


        # Changing field 'Transaction.success'
        db.alter_column(u'chargify_transaction', 'success', self.gf('django.db.models.fields.NullBooleanField')(null=True))

        # Changing field 'Transaction.kind'
        db.alter_column(u'chargify_transaction', 'kind', self.gf('django.db.models.fields.CharField')(max_length=32, null=True))

        # Changing field 'Transaction.type'
        db.alter_column(u'chargify_transaction', 'type', self.gf('django.db.models.fields.CharField')(max_length=32))

    def backwards(self, orm):
        # Deleting field 'Transaction.parent_account'
        db.delete_column(u'chargify_transaction', 'parent_account')

        # Deleting field 'Transaction.sub_account'
        db.delete_column(u'chargify_transaction', 'sub_account')


        # Changing field 'Transaction.success'
        db.alter_column(u'chargify_transaction', 'success', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Transaction.kind'
        db.alter_column(u'chargify_transaction', 'kind', self.gf('django.db.models.fields.CharField')(max_length=16, null=True))

        # Changing field 'Transaction.type'
        db.alter_column(u'chargify_transaction', 'type', self.gf('django.db.models.fields.CharField')(max_length=16))

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
            'chargify_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
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
            'product_family': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '75'}),
            'trial_interval': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'trial_interval_unit': ('django.db.models.fields.CharField', [], {'default': "'month'", 'max_length': '32'}),
            'trial_price_in_cents': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'chargify.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'activated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'balance': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '15', 'decimal_places': '2'}),
            'canceled_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'chargify_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'coupon_code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'credit_card': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subscription'", 'null': 'True', 'to': u"orm['chargify.CreditCard']"}),
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
        u'chargify.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'amount_in_cents': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'chargify_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['chargify.Customer']", 'null': 'True', 'blank': 'True'}),
            'dump': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'memo': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'parent_account': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['chargify.Product']", 'null': 'True', 'blank': 'True'}),
            'refunded_amount_in_cents': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sub_account': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['chargify.Subscription']", 'null': 'True', 'blank': 'True'}),
            'success': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'})
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