# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Questionaire'
        db.create_table('questionaire_questionaire', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True, null=True)),
            ('sub_title', self.gf('django.db.models.fields.CharField')(blank=True, null=True, max_length=512, default='')),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=32, default='')),
            ('overline_text', self.gf('django.db.models.fields.CharField')(blank=True, null=True, max_length=128)),
            ('score_text', self.gf('django.db.models.fields.CharField')(max_length=512)),
        ))
        db.send_create_signal('questionaire', ['Questionaire'])

        # Adding model 'QuestionaireManager'
        db.create_table('questionaire_questionairemanager', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('current_questionaire', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questionaire.Questionaire'])),
        ))
        db.send_create_signal('questionaire', ['QuestionaireManager'])

        # Adding model 'Question'
        db.create_table('questionaire_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now=True)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('questionaire', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questionaire.Questionaire'], related_name='parent_questionaire')),
            ('sequence_order', self.gf('django.db.models.fields.IntegerField')()),
            ('related_content_link', self.gf('django.db.models.fields.CharField')(blank=True, max_length=512, default='')),
            ('related_content_text', self.gf('django.db.models.fields.CharField')(blank=True, max_length=512, default='')),
        ))
        db.send_create_signal('questionaire', ['Question'])

        # Adding model 'Answer'
        db.create_table('questionaire_answer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now=True)),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questionaire.Question'])),
            ('is_eligible', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sequence_order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('questionaire', ['Answer'])


    def backwards(self, orm):
        # Deleting model 'Questionaire'
        db.delete_table('questionaire_questionaire')

        # Deleting model 'QuestionaireManager'
        db.delete_table('questionaire_questionairemanager')

        # Deleting model 'Question'
        db.delete_table('questionaire_question')

        # Deleting model 'Answer'
        db.delete_table('questionaire_answer')


    models = {
        'questionaire.answer': {
            'Meta': {'object_name': 'Answer'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_eligible': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionaire.Question']"}),
            'sequence_order': ('django.db.models.fields.IntegerField', [], {})
        },
        'questionaire.question': {
            'Meta': {'object_name': 'Question'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'questionaire': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionaire.Questionaire']", 'related_name': "'parent_questionaire'"}),
            'related_content_link': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '512', 'default': "''"}),
            'related_content_text': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '512', 'default': "''"}),
            'sequence_order': ('django.db.models.fields.IntegerField', [], {})
        },
        'questionaire.questionaire': {
            'Meta': {'object_name': 'Questionaire'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'overline_text': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '128'}),
            'score_text': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'sub_title': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '512', 'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '32', 'default': "''"})
        },
        'questionaire.questionairemanager': {
            'Meta': {'object_name': 'QuestionaireManager'},
            'current_questionaire': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionaire.Questionaire']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['questionaire']