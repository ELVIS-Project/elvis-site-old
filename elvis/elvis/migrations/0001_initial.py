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
        ))
        db.send_create_signal('elvis', ['Attachment'])

        # Adding model 'Corpus'
        db.create_table(u'elvis_corpus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('elvis', ['Corpus'])

        # Adding model 'Movement'
        db.create_table(u'elvis_movement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('corpus', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elvis.Corpus'])),
            ('composer', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date_of_composition', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('number_of_voices', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('elvis', ['Movement'])

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
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('corpus', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elvis.Corpus'])),
            ('composer', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date_of_composition', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('number_of_voices', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('elvis', ['Piece'])

        # Adding M2M table for field attachments on 'Piece'
        db.create_table(u'elvis_piece_attachments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('piece', models.ForeignKey(orm['elvis.piece'], null=False)),
            ('attachment', models.ForeignKey(orm['elvis.attachment'], null=False))
        ))
        db.create_unique(u'elvis_piece_attachments', ['piece_id', 'attachment_id'])


    def backwards(self, orm):
        # Deleting model 'Attachment'
        db.delete_table(u'elvis_attachment')

        # Deleting model 'Corpus'
        db.delete_table(u'elvis_corpus')

        # Deleting model 'Movement'
        db.delete_table(u'elvis_movement')

        # Removing M2M table for field attachments on 'Movement'
        db.delete_table('elvis_movement_attachments')

        # Deleting model 'Piece'
        db.delete_table(u'elvis_piece')

        # Removing M2M table for field attachments on 'Piece'
        db.delete_table('elvis_piece_attachments')


    models = {
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'elvis.corpus': {
            'Meta': {'object_name': 'Corpus'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'elvis.movement': {
            'Meta': {'object_name': 'Movement'},
            'attachments': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['elvis.Attachment']", 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'composer': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'corpus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elvis.Corpus']"}),
            'date_of_composition': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number_of_voices': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'elvis.piece': {
            'Meta': {'object_name': 'Piece'},
            'attachments': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['elvis.Attachment']", 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'composer': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'corpus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elvis.Corpus']"}),
            'date_of_composition': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number_of_voices': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_tagged_items'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_items'", 'to': u"orm['taggit.Tag']"})
        }
    }

    complete_apps = ['elvis']