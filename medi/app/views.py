from django.shortcuts import render
from .models import Woman, FamilyMember, FamilyMembership, Child, Other
import datetime
from django.db.models import Q
from dal import autocomplete


def index(request):
    return render(request, 'index.html')

def date_test(request):
    '''
    List all women from before 1350 in ascending order by date.
    '''
    qs = Woman.objects.filter(date_cal__lt=datetime.date(1350, 1, 1)) \
                      .filter(date_cal__gt=datetime.date(1, 1, 1)).order_by('date_cal')
    context = {'women': qs}
    return render(request, 'date_test.html', context)

def men_test(request):
    '''
    Men who have fathered more than one illegitimate child by different women
    '''
    men_with_illegitimate_children_by_different_women = []
    qs = Child.objects.filter(Q(legitimacy__status='illegitimate')) \
                      .filter(father__isnull=False)
    men_dict = {}
    for child in qs:
        if child.father.id not in men_dict.keys():
            men_dict[child.father.id] = [child.woman.id]
        else:
            men_dict[child.father.id].append(child.woman.id)
    for man in men_dict.keys():
        if len(set(men_dict[man])) > 1:
            men_with_illegitimate_children_by_different_women.append(man)

    men = FamilyMember.objects.filter(pk__in=men_with_illegitimate_children_by_different_women)
    context = {'men':men}
    return render(request, 'men_test.html', context)

def women_test(request):
    '''
    Women who had illegitimate children
    '''
    children = Child.objects.filter(Q(legitimacy__status='illegitimate'))
    women = [x.woman.id for x in children]
    women = Woman.objects.filter(pk__in=women)
    context = {'women':women}
    return render(request, 'women_test.html', context)

class WomanAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Woman.objects.none()

        qs = Woman.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs

class FamilyMemberAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return FamilyMember.objects.none()

        qs = FamilyMember.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs

class OtherAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Other.objects.none()

        qs = Other.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs
