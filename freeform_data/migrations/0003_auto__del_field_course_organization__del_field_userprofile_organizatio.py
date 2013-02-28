# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Course.organization'
        db.delete_column('freeform_data_course', 'organization_id')

        # Adding M2M table for field organizations on 'Course'
        db.create_table('freeform_data_course_organizations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm['freeform_data.course'], null=False)),
            ('organization', models.ForeignKey(orm['freeform_data.organization'], null=False))
        ))
        db.create_unique('freeform_data_course_organizations', ['course_id', 'organization_id'])

        # Deleting field 'UserProfile.organization'
        db.delete_column('freeform_data_userprofile', 'organization_id')


        # Changing field 'UserProfile.user'
        db.alter_column('freeform_data_userprofile', 'user_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, null=True))
        # Adding M2M table for field users on 'Organization'
        db.create_table('freeform_data_organization_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('organization', models.ForeignKey(orm['freeform_data.organization'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('freeform_data_organization_users', ['organization_id', 'user_id'])


    def backwards(self, orm):
        # Adding field 'Course.organization'
        db.add_column('freeform_data_course', 'organization',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['freeform_data.Organization']),
                      keep_default=False)

        # Removing M2M table for field organizations on 'Course'
        db.delete_table('freeform_data_course_organizations')

        # Adding field 'UserProfile.organization'
        db.add_column('freeform_data_userprofile', 'organization',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['freeform_data.Organization'], null=True, blank=True),
                      keep_default=False)


        # Changing field 'UserProfile.user'
        db.alter_column('freeform_data_userprofile', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True, null=True))
        # Removing M2M table for field users on 'Organization'
        db.delete_table('freeform_data_organization_users')


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
        'freeform_data.administratorgroup': {
            'Meta': {'object_name': 'AdministratorGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'userprofile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['freeform_data.UserProfile']"})
        },
        'freeform_data.course': {
            'Meta': {'object_name': 'Course'},
            'course_name': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'organizations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['freeform_data.Organization']", 'symmetrical': 'False'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'})
        },
        'freeform_data.essay': {
            'Meta': {'object_name': 'Essay'},
            'additional_predictors': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'essay_text': ('django.db.models.fields.TextField', [], {}),
            'essay_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'has_been_ml_graded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'problem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['freeform_data.Problem']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        },
        'freeform_data.essaygrade': {
            'Meta': {'object_name': 'EssayGrade'},
            'annotated_text': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'confidence': ('django.db.models.fields.DecimalField', [], {'default': '1', 'max_digits': '10', 'decimal_places': '9'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'essay': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['freeform_data.Essay']"}),
            'feedback': ('django.db.models.fields.TextField', [], {}),
            'grader_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'premium_feedback_scores': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'target_scores': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'freeform_data.gradergroup': {
            'Meta': {'object_name': 'GraderGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'userprofile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['freeform_data.UserProfile']"})
        },
        'freeform_data.organization': {
            'Meta': {'object_name': 'Organization'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'organization_name': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'organization_size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'premium_service_subscriptions': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'freeform_data.problem': {
            'Meta': {'object_name': 'Problem'},
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['freeform_data.Course']", 'symmetrical': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_target_scores': ('django.db.models.fields.TextField', [], {'default': "'[1]'"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'number_of_additional_predictors': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'premium_feedback_models': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
            'prompt': ('django.db.models.fields.TextField', [], {'default': "''"})
        },
        'freeform_data.studentgroup': {
            'Meta': {'object_name': 'StudentGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'userprofile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['freeform_data.UserProfile']"})
        },
        'freeform_data.teachergroup': {
            'Meta': {'object_name': 'TeacherGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'userprofile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['freeform_data.UserProfile']"})
        },
        'freeform_data.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['freeform_data']