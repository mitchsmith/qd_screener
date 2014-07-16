from django.contrib.admin import SimpleListFilter

class QuestionListFilter(SimpleListFilter):
    title = 'quiz title'
    parameter_name = 'quiz_title'
 
    def lookups(self, request, model_admin):
        questionaires = set([q.questionaire for q in model_admin.model.objects.all()])
        return [(q.id, q.title) for q in questionaires]
       
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(quiz__id=int(self.value()))
        else:
            return queryset


class AnswerListFilter(SimpleListFilter):
    title = 'question'
    parameter_name = 'question'

    def lookups(self, request, model_admin):
        questions = set([a.question for a in model_admin.model.objects.all()])
        return [(q.id, q.question) for q in questions]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(question__id = int(self.value()))
        else:
            return queryset
