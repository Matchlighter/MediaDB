# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field mediums on 'TVSeason'
        db.delete_table(db.shorten_name(u'mediadb_tvseason_mediums'))


    def backwards(self, orm):
        # Adding M2M table for field mediums on 'TVSeason'
        m2m_table_name = db.shorten_name(u'mediadb_tvseason_mediums')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tvseason', models.ForeignKey(orm[u'mediadb.tvseason'], null=False)),
            ('mediaobject', models.ForeignKey(orm[u'mediadb.mediaobject'], null=False))
        ))
        db.create_unique(m2m_table_name, ['tvseason_id', 'mediaobject_id'])


    models = {
        u'mediadb.location': {
            'Meta': {'object_name': 'Location'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        u'mediadb.mediaobject': {
            'Meta': {'unique_together': "(('location', 'index'),)", 'object_name': 'MediaObject'},
            'format': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mediadb.MFormat']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mediadb.Location']"}),
            'ripped': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '15'})
        },
        u'mediadb.mformat': {
            'Meta': {'object_name': 'MFormat'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'mediadb.movie': {
            'Meta': {'object_name': 'Movie'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mediums': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'movies'", 'blank': 'True', 'through': u"orm['mediadb.MovieMedia']", 'to': u"orm['mediadb.MediaObject']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tmdb_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'mediadb.moviemedia': {
            'Meta': {'object_name': 'MovieMedia'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medium': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mediadb.MediaObject']"}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mediadb.Movie']"})
        },
        u'mediadb.tvepisode': {
            'Meta': {'object_name': 'TVEpisode'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mediadb.TVSeason']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'mediadb.tvseason': {
            'Meta': {'object_name': 'TVSeason'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mediums': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'tv_seasons'", 'blank': 'True', 'through': u"orm['mediadb.TVSeasonMedia']", 'to': u"orm['mediadb.MediaObject']"}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'series': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mediadb.TVSeries']"})
        },
        u'mediadb.tvseasonmedia': {
            'Meta': {'ordering': "('order',)", 'object_name': 'TVSeasonMedia'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medium': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mediadb.MediaObject']"}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'tvseason': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mediadb.TVSeason']"})
        },
        u'mediadb.tvseries': {
            'Meta': {'object_name': 'TVSeries'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tmdb_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['mediadb']