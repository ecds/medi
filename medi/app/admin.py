from django.contrib import admin
from admin_auto_filters.filters import AutocompleteFilter
from import_export import resources
from import_export.admin import ExportMixin
from rangefilter.filter import DateRangeFilter
from djangoql.admin import DjangoQLSearchMixin


from .models import *
from .forms import *

#h/t: https://stackoverflow.com/a/21223908/2402028
# def custom_titled_filter(title):
#     class Wrapper(admin.FieldListFilter):
#         def __new__(cls, *args, **kwargs):
#             instance = admin.FieldListFilter.create(*args, **kwargs)
#             instance.title = title
#             return instance
#     return Wrapper

class IdentifierFilter(AutocompleteFilter):
    title = 'identifier'
    field_name = 'identifier'

class EnslavementStatusFilter(AutocompleteFilter):
    title = 'enslavement status'
    field_name = 'enslavement_status'

class OriginFilter(AutocompleteFilter):
    title = "place of origin"
    field_name = 'origin'

class LocationOfTransactionFilter(AutocompleteFilter):
    title = "location of transaction"
    field_name = 'location_of_transaction'

class LocationSoldFilter(AutocompleteFilter):
    title = 'location sold'
    field_name = 'location_sold'

class TypeFilter(AutocompleteFilter):
    title = 'type of document'
    field_name = 'document_type'

class FamilyMemberInline(admin.TabularInline):
    model = Woman.family_members.through
    form = FamilyMembershipForm
    extra = 1

class ChildInline(admin.TabularInline):
    model = Child
    extra = 1

class RelatedOtherInline(admin.TabularInline):
    model = Woman.others.through
    form = RelatedOtherForm
    extra = 1
    verbose_name_plural = 'Related Others'

class RelatedWomenInline(admin.TabularInline):
    model = RelatedWoman
    form = RelatedWomanForm
    fk_name = 'woman'
    extra = 1
    verbose_name_plural = 'Related Women'

class WomanResource(resources.ModelResource):

    class Meta:
        model = Woman
        fields = ('id', 'name', 'name_variations', 'marital_status', 'identifier__name', 'conc_or_pro', 'age_literal', 'age_category', 'activity', 'origin__name', 'location_of_transaction__name', 'occupation', 'enslavement_status__status', 'location_sold__name', 'sale_freq', 'sale_details', 'enslavement_details', 'enslavement_occupation', 'date_as_written', 'date_cal', 'date_range', 'document_type__document_type', 'description__description', 'transcription', 'comments', 'archive', 'shelfmark', 'data_enterer')

class WomanAdmin(DjangoQLSearchMixin, ExportMixin, admin.ModelAdmin):
    djangoql_completion_enabled_by_default = False
    resource_class = WomanResource
    list_display = ['id', 'name', 'age_category', 'occupation', 'date_cal']
    search_fields = ['name', 'name_variations', 'marital_status', 'identifier__name', 'conc_or_pro', 'age_literal', 'age_category', 'activity', 'origin__name', 'location_of_transaction__name',  'occupation', 'enslavement_status__status', 'location_sold__name', 'sale_details', 'enslavement_details', 'enslavement_occupation', 'date_as_written', 'date_range', 'document_type__document_type', 'description__description', 'transcription', 'comments', 'archive', 'shelfmark', 'data_enterer']
    fieldsets = (
        (None, {
            'fields': ('name', 'name_variations', 'marital_status', 'identifier', 'conc_or_pro', 'age_literal', 'age_category', 'origin', 'activity',  'location_of_transaction', 'occupation')
        }),
        ('Enslavement Details', {
            #'classes': ('collapse',),
            'fields': ('enslavement_status', 'location_sold', 'sale_freq', 'sale_details', 'enslavement_details', 'enslavement_occupation')
        }),
        ('Document Details', {
            #'classes': ('collapse',),
            'fields': ('date_as_written', 'date_cal', 'date_range', 'document_type', 'description', 'transcription', 'comments', 'archive', 'shelfmark', 'folio', 'pub_reg_title', 'pub_reg_vol', 'pub_reg_doc', 'pub_reg_page')
        }),
        (None, {
            'fields': ('data_enterer', 'document_image')
        }),
    )
    list_filter = (('date_cal', DateRangeFilter),
                    'marital_status',
                    'conc_or_pro',
                    IdentifierFilter,
                    EnslavementStatusFilter,
                    OriginFilter,
                    LocationOfTransactionFilter,
                    LocationSoldFilter,
                    'occupation',
                    TypeFilter)
    inlines = [RelatedWomenInline, ChildInline, FamilyMemberInline, RelatedOtherInline]
    autocomplete_fields = ['origin', 'location_of_transaction', 'location_sold']
    exclude = ('family_members',)

    class Media:
        pass


class PlaceAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    djangoql_completion_enabled_by_default = False
    list_display = ['id', 'name', 'lat', 'lon']
    search_fields = ['name']


class RelatedWomanAdmin(admin.ModelAdmin):
    list_display = ['woman', 'related_woman', 'relationship']

class FamilyMembershipAdmin(admin.ModelAdmin):
    list_display = ['id', 'woman', 'family_member', 'relationship']

class RelatedOtherAdmin(admin.ModelAdmin):
    list_display = ['id', 'woman', 'other', 'role']


class FamilyMemberAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    djangoql_completion_enabled_by_default = False
    list_display = ['id', 'name', 'age_category']
    search_fields = ['name', 'age_category']
    list_filter = ['age_category']
    #inlines = [ChildInline, FamilyMemberInline]


class ChildAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    djangoql_completion_enabled_by_default = False
    list_display = ['id', 'name', 'woman', 'age_category', 'father', 'legitimacy']
    search_fields = ['woman__name', 'name', 'age_category', 'father', 'legitimacy']
    list_filter = ['age_category', 'legitimacy']


class OtherAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    djangoql_completion_enabled_by_default = False
    list_display = ['id', 'name']
    search_fields = ['name']


class IdentifierAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


class EnslavementStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'status']
    search_fields = ['status']

class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'role']


class ChildAgeAdmin(admin.ModelAdmin):
    list_display = ['id', 'category']


class ChildLegitimacyAdmin(admin.ModelAdmin):
    list_display = ['id', 'status']


class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'document_type']
    search_fields = ['document_type']


class DocumentDescriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'description']

admin.site.register(Woman, WomanAdmin)
admin.site.register(FamilyMember, FamilyMemberAdmin)
admin.site.register(Child, ChildAdmin)
admin.site.register(Other, OtherAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Identifier, IdentifierAdmin)
admin.site.register(EnslavementStatus, EnslavementStatusAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(ChildAge, ChildAgeAdmin)
admin.site.register(ChildLegitimacy, ChildLegitimacyAdmin)
admin.site.register(DocumentType, DocumentTypeAdmin)
admin.site.register(DocumentDescription, DocumentDescriptionAdmin)
admin.site.register(FamilyMembership, FamilyMembershipAdmin)
admin.site.register(RelatedWoman, RelatedWomanAdmin)
admin.site.register(RelatedOther, RelatedOtherAdmin)
