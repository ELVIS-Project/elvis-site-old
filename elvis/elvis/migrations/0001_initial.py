# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Attachment'
        db.create_table(u'elvis_attachment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=255, null=True)),
            ('uploader', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('elvis', ['Attachment'])

        # Adding model 'Corpus'
        db.create_table(u'elvis_corpus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('old_id', self.gf('django.db.models.fields.IntegerField')()),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('elvis', ['Corpus'])

        # Adding model 'Movement'
        db.create_table(u'elvis_movement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('old_id', self.gf('django.db.models.fields.IntegerField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('uploader', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('corpus', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elvis.Corpus'])),
            ('composer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elvis.Composer'])),
            ('date_of_composition', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('number_of_voices', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('elvis', ['Movement'])

        # Adding M2M table for field tags on 'Movement'
        db.create_table(u'elvis_movement_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('movement', models.ForeignKey(orm['elvis.movement'], null=False)),
            ('tag', models.ForeignKey(orm['elvis.tag'], null=False))
        ))
        db.create_unique(u'elvis_movement_tags', ['movement_id', 'tag_id'])

        # Adding M2M table for field attachments on 'Movement'
        db.create_table(u'elvis_movement_attachments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('movement', models.ForeignKey(orm['elvis.movement'], null=False)),
            ('attachment', models.ForeignKey(orm['elvis.attachment'], null=False))
        ))
        db.create_unique(u'elvis_movement_attachments', ['movement_id', 'attachment_id'])

        # Adding model 'Piece'
        db.create_table(u'elvis_piece', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('old_id', self.gf('django.db.models.fields.IntegerField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('uploader', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('corpus', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elvis.Corpus'])),
            ('composer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elvis.Composer'])),
            ('date_of_composition', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('number_of_voices', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('elvis', ['Piece'])

        # Adding M2M table for field tags on 'Piece'
        db.create_table(u'elvis_piece_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('piece', models.ForeignKey(orm['elvis.piece'], null=False)),
            ('tag', models.ForeignKey(orm['elvis.tag'], null=False))
        ))
        db.create_unique(u'elvis_piece_tags', ['piece_id', 'tag_id'])

        # Adding M2M table for field attachments on 'Piece'
        db.create_table(u'elvis_piece_attachments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('piece', models.ForeignKey(orm['elvis.piece'], null=False)),
            ('attachment', models.ForeignKey(orm['elvis.attachment'], null=False))
        ))
        db.create_unique(u'elvis_piece_attachments', ['piece_id', 'attachment_id'])

        # Adding model 'Composer'
        db.create_table(u'elvis_composer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('old_id', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('birth_date', self.gf('django.db.models.fields.DateField')()),
            ('death_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('elvis', ['Composer'])

        # Adding model 'Tag'
        db.create_table(u'elvis_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('old_id', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('elvis', ['Tag'])

        # Adding model 'TagHierarchy'
        db.create_table(u'elvis_taghierarchy', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(related_name='in_hierarchy', to=orm['elvis.Tag'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='has_hierarchy', null=True, to=orm['elvis.Tag'])),
        ))
        db.send_create_signal('elvis', ['TagHierarchy'])


    def backwards(self, orm):
        # Deleting model 'Attachment'
        db.delete_table(u'elvis_attachment')

        # Deleting model 'Corpus'
        db.delete_table(u'elvis_corpus')

        # Deleting model 'Movement'
        db.delete_table(u'elvis_movement')

        # Removing M2M table for field tags on 'Movement'
        db.delete_table('elvis_movement_tags')

        # Removing M2M table for field attachments on 'Movement'
        db.delete_table('elvis_movement_attachments')

        # Deleting model 'Piece'
        db.delete_table(u'elvis_piece')

        # Removing M2M table for field tags on 'Piece'
        db.delete_table('elvis_piece_tags')

        # Removing M2M table for field attachments on 'Piece'
        db.delete_table('elvis_piece_attachments')

        # Deleting model 'Composer'
        db.delete_table(u'elvis_composer')

        # Deleting model 'Tag'
        db.delete_table(u'elvis_tag')

        # Deleting model 'TagHierarchy'
        db.delete_table(u'elvis_taghierarchy')


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
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'elvis.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uploader': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'elvis.composer': {
            'Meta': {'object_name': 'Composer'},
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'death_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'old_id': ('django.db.models.fields.IntegerField', [], {})
        },
        'elvis.corpus': {
            'Meta': {'object_name': 'Corpus'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'old_id': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'elvis.movement': {
            'Meta': {'object_name': 'Movement'},
            'attachments': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['elvis.Attachment']", 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'composer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elvis.Composer']"}),
            'corpus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elvis.Corpus']"}),
            'date_of_composition': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number_of_voices': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'old_id': ('django.db.models.fields.IntegerField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['elvis.Tag']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uploader': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'elvis.piece': {
            'Meta': {'object_name': 'Piece'},
            'attachments': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['elvis.Attachment']", 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'composer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elvis.Composer']"}),
            'corpus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elvis.Corpus']"}),
            'date_of_composition': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number_of_voices': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'old_id': ('django.db.models.fields.IntegerField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['elvis.Tag']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uploader': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'elvis.tag': {
            'Meta': {'object_name': 'Tag'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'old_id': ('django.db.models.fields.IntegerField', [], {})
        },
        'elvis.taghierarchy': {
            'Meta': {'object_name': 'TagHierarchy'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'has_hierarchy'", 'null': 'True', 'to': "orm['elvis.Tag']"}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'in_hierarchy'", 'to': "orm['elvis.Tag']"})
        }
    }

    complete_apps = ['elvis']