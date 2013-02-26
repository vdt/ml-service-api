# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Organization'
        db.create_table('freeform_data_organization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organization_size', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('organization_name', self.gf('django.db.models.fields.TextField')()),
            ('premium_service_subscriptions', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('freeform_data', ['Organization'])

        # Adding model 'UserProfile'
        db.create_table('freeform_data_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True, null=True, blank=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['freeform_data.Organization'])),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('freeform_data', ['UserProfile'])

        # Adding model 'Course'
        db.create_table('freeform_data_course', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['freeform_data.Organization'])),
            ('course_name', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('freeform_data', ['Course'])

        # Adding M2M table for field users on 'Course'
        db.create_table('freeform_data_course_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm['freeform_data.course'], null=False)),
            ('userprofile', models.ForeignKey(orm['freeform_data.userprofile'], null=False))
        ))
        db.create_unique('freeform_data_course_users', ['course_id', 'userprofile_id'])

        # Adding model 'Problem'
        db.create_table('freeform_data_problem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('max_target_scores', self.gf('django.db.models.fields.TextField')()),
            ('number_of_additional_predictors', self.gf('django.db.models.fields.IntegerField')()),
            ('prompt', self.gf('django.db.models.fields.TextField')()),
            ('premium_feedback_models', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('freeform_data', ['Problem'])

        # Adding M2M table for field course on 'Problem'
        db.create_table('freeform_data_problem_course', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('problem', models.ForeignKey(orm['freeform_data.problem'], null=False)),
            ('course', models.ForeignKey(orm['freeform_data.course'], null=False))
        ))
        db.create_unique('freeform_data_problem_course', ['problem_id', 'course_id'])

        # Adding model 'Essay'
        db.create_table('freeform_data_essay', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('problem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['freeform_data.Problem'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['freeform_data.UserProfile'])),
            ('essay_text', self.gf('django.db.models.fields.TextField')()),
            ('additional_predictors', self.gf('django.db.models.fields.TextField')()),
            ('essay_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('freeform_data', ['Essay'])

        # Adding model 'EssayGrade'
        db.create_table('freeform_data_essaygrade', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('essay', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['freeform_data.Essay'])),
            ('target_scores', self.gf('django.db.models.fields.TextField')()),
            ('grader_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('feedback', self.gf('django.db.models.fields.TextField')()),
            ('annotated_text', self.gf('django.db.models.fields.TextField')()),
            ('premium_feedback_scores', self.gf('django.db.models.fields.TextField')()),
            ('success', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['freeform_data.UserProfile'], null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('freeform_data', ['EssayGrade'])


    def backwards(self, orm):
        # Deleting model 'Organization'
        db.delete_table('freeform_data_organization')

        # Deleting model 'UserProfile'
        db.delete_table('freeform_data_userprofile')

        # Deleting model 'Course'
        db.delete_table('freeform_data_course')

        # Removing M2M table for field users on 'Course'
        db.delete_table('freeform_data_course_users')

        # Deleting model 'Problem'
        db.delete_table('freeform_data_problem')

        # Removing M2M table for field course on 'Problem'
        db.delete_table('freeform_data_problem_course')

        # Deleting model 'Essay'
        db.delete_table('freeform_data_essay')

        # Deleting model 'EssayGrade'
        db.delete_table('freeform_data_essaygrade')


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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'freeform_data.course': {
            'Meta': {'object_name': 'Course'},
            'course_name': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['freeform_data.Organization']"}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['freeform_data.UserProfile']", 'symmetrical': 'False'})
        },
        'freeform_data.essay': {
            'Meta': {'object_name': 'Essay'},
            'additional_predictors': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'essay_text': ('django.db.models.fields.TextField', [], {}),
            'essay_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'problem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['freeform_data.Problem']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['freeform_data.UserProfile']"})
        },
        'freeform_data.essaygrade': {
            'Meta': {'object_name': 'EssayGrade'},
            'annotated_text': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'essay': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['freeform_data.Essay']"}),
            'feedback': ('django.db.models.fields.TextField', [], {}),
            'grader_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'premium_feedback_scores': ('django.db.models.fields.TextField', [], {}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'target_scores': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['freeform_data.UserProfile']", 'null': 'True', 'blank': 'True'})
        },
        'freeform_data.organization': {
            'Meta': {'object_name': 'Organization'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'organization_name': ('django.db.models.fields.TextField', [], {}),
            'organization_size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'premium_service_subscriptions': ('django.db.models.fields.TextField', [], {})
        },
        'freeform_data.problem': {
            'Meta': {'object_name': 'Problem'},
            'course': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['freeform_data.Course']", 'symmetrical': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_target_scores': ('django.db.models.fields.TextField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'number_of_additional_predictors': ('django.db.models.fields.IntegerField', [], {}),
            'premium_feedback_models': ('django.db.models.fields.TextField', [], {}),
            'prompt': ('django.db.models.fields.TextField', [], {})
        },
        'freeform_data.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['freeform_data.Organization']"}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['freeform_data']