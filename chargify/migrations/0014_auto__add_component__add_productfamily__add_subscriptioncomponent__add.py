# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'Component'
        db.create_table('chargify_component', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('chargify_id', self.gf('django.db.models.fields.IntegerField')(unique=True, null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('product_family', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chargify.ProductFamily'], null=True)),
            ('kind', self.gf('django.db.models.fields.CharField')(default='metered_component', max_length=30)),
            ('pricing_scheme', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('price_per_unit', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=15, decimal_places=2)),
            ('unit_name', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('chargify', ['Component'])

        # Adding model 'ProductFamily'
        db.create_table('chargify_productfamily', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('chargify_id', self.gf('django.db.models.fields.IntegerField')(unique=True, null=True)),
            ('accounting_code', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
            ('handle', self.gf('django.db.models.fields.CharField')(default='', max_length=75)),
        ))
        db.send_create_signal('chargify', ['ProductFamily'])

        # Adding model 'SubscriptionComponent'
        db.create_table('chargify_subscriptioncomponent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('component', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chargify.Component'], null=True)),
            ('subscription', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chargify.Subscription'], null=True)),
            ('unit_balance', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=15, decimal_places=2)),
            ('allocated_quantity', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=15, decimal_places=2)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('chargify', ['SubscriptionComponent'])

        # Adding field 'Product.product_family'
        db.add_column('chargify_product', 'product_family', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chargify.ProductFamily'], null=True), keep_default=False)


    def backwards(self, orm):

        # Deleting model 'Component'
        db.delete_table('chargify_component')

        # Deleting model 'ProductFamily'
        db.delete_table('chargify_productfamily')

        # Deleting model 'SubscriptionComponent'
        db.delete_table('chargify_subscriptioncomponent')

        # Deleting field 'Product.product_family'
        db.delete_column('chargify_product', 'product_family_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'chargify.component': {
            'Meta': {'object_name': 'Component'},
            'chargify_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'default': "'metered_component'", 'max_length': '30'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'price_per_unit': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '15', 'decimal_places': '2'}),
            'pricing_scheme': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'product_family': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chargify.ProductFamily']", 'null': 'True'}),
            'unit_name': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'chargify.creditcard': {
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'masked_card_number': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'})
        },
        'chargify.customer': {
            'Meta': {'object_name': 'Customer'},
            '_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            '_first_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            '_last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            '_reference': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'chargify_created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'chargify_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True'}),
            'chargify_updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'chargify.product': {
            'Meta': {'object_name': 'Product'},
            'accounting_code': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'chargify_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True'}),
            'handle': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'interval_unit': ('django.db.models.fields.CharField', [], {'default': "'month'", 'max_length': '10'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '15', 'decimal_places': '2'}),
            'product_family': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chargify.ProductFamily']", 'null': 'True'})
        },
        'chargify.productfamily': {
            'Meta': {'object_name': 'ProductFamily'},
            'accounting_code': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'chargify_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'handle': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75'})
        },
        'chargify.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'activated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'balance': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '15', 'decimal_places': '2'}),
            'chargify_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'credit_card': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'subscription'", 'unique': 'True', 'null': 'True', 'to': "orm['chargify.CreditCard']"}),
            'current_period_ends_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'current_period_started_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chargify.Customer']", 'null': 'True'}),
            'expires_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_activation_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_deactivation_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'next_assessment_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'next_billing_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chargify.Product']", 'null': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'trial_ended_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'trial_started_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'chargify.subscriptioncomponent': {
            'Meta': {'object_name': 'SubscriptionComponent'},
            'allocated_quantity': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '15', 'decimal_places': '2'}),
            'component': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chargify.Component']", 'null': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chargify.Subscription']", 'null': 'True'}),
            'unit_balance': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '15', 'decimal_places': '2'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['chargify']
