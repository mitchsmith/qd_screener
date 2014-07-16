from django.contrib import admin
from django.forms import ModelChoiceField, ModelForm, Textarea
from questionnaire.models import *
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from questionnaire import admin_helper

############################################### HELPER METHODS ###########################################

def is_strictly_monotonically_increasing(sequence):
    """
    Determines if sequence is strictly monotically increasing. Used to validate the order specified for
    Questions and Answers.
    """
    return all(x<y for x, y in zip(sequence, sequence[1:]))

############################################### Questionnaire Manager ##############################################

class CustomQuestionnaireModelField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.title

class QuestionnaireManagerAdminForm(ModelForm):
    current_questionnaire = CustomQuestionnaireModelField(queryset=Questionnaire.objects.all())
    class Meta:
        model = QuestionnaireManager

class QuestionnaireManagerAdmin(admin.ModelAdmin):
    form = QuestionnaireManagerAdminForm

admin.site.register(QuestionnaireManager, QuestionnaireManagerAdmin)

################################################ Answer ###################################################

class CustomQuestionField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.question

class AnswerAdminForm(ModelForm):
    question = CustomQuestionField(queryset=Question.objects.all())          

def Question_Text(obj):
    return obj.question.question

class AnswerFormSet(BaseInlineFormSet):
    def clean(self):
        """
        Check that:
        1. There's only one correct answer (this must be checked to be eligible)
        2. A valid  order in which to display answers has been specified
        3. There are at least 2 answers
        """
        super(AnswerFormSet, self).clean()
        # Check #1
        specified_sequence = []
        num_correct_answers = 0
        num_answers = 0
        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue
            data = form.cleaned_data
            if data.get('is_correct', False):
                num_correct_answers += 1
            data = data.get('sequence_order', -1)
            if data > -1:
                specified_sequence.append(data)
                num_answers += 1

        if num_correct_answers != 1:
            raise ValidationError('Need to choose one "correct" answer')
          
        # Check #2
        specified_sequence = sorted(specified_sequence)
        if not is_strictly_monotonically_increasing(specified_sequence):
            message = """ The order you've specified in which to display answers doens't make sense.
                Please enter a sequence starting with 1, without skipping or repeating numbers. """
            raise ValidationError(message)

        # Check #3
        if num_answers < 2:
            message = 'There should be at least 2 answers'
            raise ValidationError(message)

class AnswerInline(admin.TabularInline):
    model = Answer
    formset = AnswerFormSet
    ordering = ('-created_on',)

################################################# Question ##############################################


def Questionnaire_Title(obj):
    return obj.questionnaire.title

class QuestionAdminForm(ModelForm):
    # questionnaire = CustomQuestionnaireModelField(queryset=Questionnaire.objects.all())
     
    def check_url(self, url):
        if len(url) > 0:
            return url.startswith('http')
        return True

    def clean(self):
        cleaned_data = super(QuestionAdminForm, self).clean()
        related_content_link = cleaned_data.get('related_content_link')
        related_content_text = cleaned_data.get('related_content_text')
        at_least_one_field_has_text = (len(related_content_link.strip()) + len(related_content_text.strip())) > 0
        both_fields_have_text = (len(related_content_link.strip()) * len(related_content_text.strip())) > 0
        if at_least_one_field_has_text and not both_fields_have_text:
            raise ValidationError('Both related_content_link and related_content_text need to be either set or empty')
        if not self.check_url(related_content_link):
            raise ValidationError('%s does not seem to be a valid url' % related_content_link)
        return cleaned_data

    class Meta:
        model = Question
        widgets = {
            'question': Textarea
        }

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ AnswerInline, ]
    search_fields = ['questionnaire__title', 'question' ]
    list_display = ['question', Questionnaire_Title, 'sequence_order', 'created_on']
    list_filter = ['created_on', admin_helper.QuestionListFilter]
    ordering = ('-created_on',)
    form = QuestionAdminForm

admin.site.register(Question, QuestionAdmin)

class QuestionFormSet(BaseInlineFormSet):
    def clean(self):
        """
        1. Check that all answers have been assigned a sequence (1..k)
           in order, without skipping indices, and unique!
        2. Check that related_content_link and related_content_text are both either 
           specified or blank
        """
        super(QuestionFormSet, self).clean()
        # Check #1
        specified_sequence = []
        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue
            data = form.cleaned_data
            data = data.get('sequence_order', -1)
            if data > -1:
                specified_sequence.append(data)

        specified_sequence = sorted(specified_sequence)
        if not is_strictly_monotonically_increasing(specified_sequence):
            message = """ The order you've specified in which to display questions doens't make sense.
                          Please enter a sequence starting with 1, without skipping or repeating numbers. """
            raise ValidationError(message)
        
        # Check #2
        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue
            data = form.cleaned_data
            related_content_link = data.get('related_content_link', '').strip()
            related_content_text = data.get('related_content_text', '').strip()

            at_least_one_field_has_text = (len(related_content_link.strip()) + len(related_content_text.strip())) > 0
            both_fields_have_text = (len(related_content_link.strip()) * len(related_content_text.strip())) > 0
            if at_least_one_field_has_text and not both_fields_have_text:
                raise ValidationError('Both related_content_link and related_content_text need to be either set or empty')

class QuestionInline(admin.TabularInline):
    model = Question
    formset = QuestionFormSet
    ordering = ('-created_on',)
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'question':
            kwargs['widget'] = Textarea()
        return super(QuestionInline,self).formfield_for_dbfield(db_field,**kwargs)

############################################## Questionnaire ###############################################

class QuestionnaireAdmin(admin.ModelAdmin):
    inlines = [ QuestionInline ]
    list_display = ['title', 'description', 'created_on']
    list_filter = ['created_on']
    search_fields = ['title', 'sub_title']
    ordering = ('-created_on',)

admin.site.register(Questionnaire, QuestionnaireAdmin)

class StudyAdmin(admin.ModelAdmin):
    list_display = ['protocol_number', 'created_on']
    list_filter = ['created_on']
    search_fields = ['protocol_number']
    ordering = ('-created_on',)

admin.site.register(Study, StudyAdmin)
