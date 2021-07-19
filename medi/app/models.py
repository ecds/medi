from django.db import models
from django_date_extensions.fields import ApproximateDateField
from django.db.models import Q
from django.utils.html import mark_safe

class Woman(models.Model):
    MARITAL_STATUS_CHOICES = (
        ('Single', 'Single'),
        ('Single / Daughter of', 'Single / Daughter of'),
        ('Married', 'Married'),
        ('Widowed', 'Widowed'),
        ('Abandoned Spouse', 'Abandoned Spouse'),
        ('Concubinary Partner', 'Concubinary Partner')
    )

    CONC_OR_PRO_CHOICES = (
        ('Concubine', 'Concubine'),
        ('Prostitute', 'Prostitute')
    )

    AGE_CHOICES = (
        ('Child', 'Child'),
        ('Adolescent', 'Adolescent'),
        ('Nubile / fadrina', 'Nubile / fadrina'),
        ('Childbearing', 'Childbearing'),
        ('Middle Aged', 'Middle Aged'),
        ('Elderly', 'Elderly'),
        ('Unknown', 'Unknown')
    )

    name = models.CharField(max_length=255)
    name_variations = models.CharField(max_length=255, blank=True, null=True, help_text='Variations of name separated by semi-colons')
    marital_status = models.CharField(max_length=255, blank=True, null=True, choices=MARITAL_STATUS_CHOICES)
    identifier = models.ForeignKey('Identifier', blank=True, null=True, on_delete=models.CASCADE)
    conc_or_pro = models.CharField(max_length=255, blank=True, null=True, choices=CONC_OR_PRO_CHOICES, verbose_name="Concubine or Prostitute")
    age_literal = models.CharField(max_length=255, blank=True, null=True, verbose_name='Age as written')
    age_category = models.CharField(max_length=255, blank=True, null=True, verbose_name='Age category', choices=AGE_CHOICES)
    activity = models.CharField(max_length=255, blank=True, null=True, verbose_name='Type of activity', help_text="e.g. 'buying property'")
    origin = models.ForeignKey('Place', blank=True, null=True, related_name='origin', on_delete=models.CASCADE, verbose_name='Place of origin')
    location_of_transaction = models.ForeignKey('Place', blank=True, null=True, related_name='location_of_transaction', on_delete=models.CASCADE, verbose_name='Location of transaction/act')
    family_members = models.ManyToManyField('FamilyMember', related_name='family_members', through="FamilyMembership")
    others = models.ManyToManyField('Other', related_name='others', through="RelatedOther")
    related_women = models.ManyToManyField('self', through="RelatedWoman")
    occupation = models.CharField(max_length=255, blank=True, null=True)
    enslavement_status = models.ForeignKey('EnslavementStatus', blank=True, null=True, on_delete=models.CASCADE)
    location_sold = models.ForeignKey('Place', blank=True, null=True, related_name='location_sold', on_delete=models.CASCADE)
    sale_freq = models.BooleanField(max_length=255, blank=True, null=True, verbose_name='Sold more than once?')
    sale_details = models.TextField(blank=True, null=True)
    enslavement_details = models.TextField(blank=True, null=True)
    enslavement_occupation = models.CharField(max_length=255, blank=True, null=True, verbose_name='Occupation as enslaved person')
    date_as_written = models.CharField(max_length=255, blank=True, null=True)
    date_cal = ApproximateDateField(blank=True, null=True, verbose_name="Calendar date", help_text="Accepts approximate dates like '1350' or 'March 1402'")
    date_range = models.CharField(max_length=255, blank=True, null=True, help_text="Enter a period of time, e.g. 'early 14th century'")
    document_type = models.ForeignKey('DocumentType', blank=True, null=True, verbose_name='Type of document', on_delete=models.CASCADE)
    description = models.ForeignKey('DocumentDescription', blank=True, null=True, verbose_name="Description of document", on_delete=models.CASCADE)
    transcription = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    archive = models.CharField(max_length=255, blank=True, null=True)
    shelfmark = models.CharField(max_length=255, blank=True, null=True)
    data_enterer = models.CharField(max_length=255, blank=True, null=True)
    document_image = models.ImageField(upload_to='images/', blank=True)

    @property
    def children(self):
        return Child.objects.filter(Q(woman__id=self.pk))

    @property
    def related_women_qs(self):
        return RelatedWoman.objects.filter(Q(woman__id=self.pk))

    def __str__(self):
        return "%s - %s" % (self.id, self.name)

    class Meta:
        verbose_name_plural = "women"

class RelatedWoman(models.Model):
    woman = models.ForeignKey('Woman', on_delete=models.CASCADE, related_name='woman')
    related_woman = models.ForeignKey('Woman', on_delete=models.CASCADE, related_name='related_woman')
    relationship = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Related Women'


class RelatedOther(models.Model):
    woman = models.ForeignKey('Woman', on_delete=models.CASCADE)
    other = models.ForeignKey('Other', on_delete=models.CASCADE)
    role = models.ForeignKey('Role', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Related Others'

class Identifier(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class EnslavementStatus(models.Model):
    status = models.CharField(max_length=255)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name_plural = "Enslavement Statuses"


class DocumentType(models.Model):
    document_type = models.CharField(max_length=255)

    def __str__(self):
        return self.document_type

class DocumentDescription(models.Model):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description


class FamilyMembership(models.Model):
    woman = models.ForeignKey('Woman', on_delete=models.CASCADE)
    family_member = models.ForeignKey('FamilyMember', on_delete=models.CASCADE)
    relationship = models.CharField(max_length=255, blank=True, null=True)


class FamilyMember(models.Model):
    name = models.CharField(max_length=255)
    age_literal = models.CharField(max_length=255, blank=True, null=True, verbose_name='Age as written')
    age_category = models.CharField(max_length=255, blank=True, null=True, verbose_name='Age category')

    @property
    def children(self):
        return Child.objects.filter(Q(father__id=self.pk))

    def __str__(self):
        return "%s - %s" % (self.id, self.name)

    class Meta:
        verbose_name_plural = "Family Members"


class Other(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return "%s - %s" % (self.id, self.name)


class Role(models.Model):
    role = models.CharField(max_length=255)

    def __str__(self):
        return self.role


class Child(models.Model):
    woman = models.ForeignKey('Woman', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    age_literal = models.CharField(max_length=255, blank=True, null=True, verbose_name='Age as written')
    age_category = models.ForeignKey('ChildAge', blank=True, null=True, verbose_name='Age category', on_delete=models.CASCADE)
    father = models.ForeignKey('FamilyMember', blank=True, null=True, on_delete=models.CASCADE)
    legitimacy = models.ForeignKey('ChildLegitimacy', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Children"

class ChildAge(models.Model):
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.category

class ChildLegitimacy(models.Model):
    status = models.CharField(max_length=255)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name_plural = "Child Legitimacy Statuses"


class Place(models.Model):
    name = models.CharField(max_length=255)
    lon = models.DecimalField(max_digits=15, decimal_places=12, blank=True, null=True, verbose_name='longitude')
    lat = models.DecimalField(max_digits=15, decimal_places=12, blank=True, null=True, verbose_name='latitude')

    def __str__(self):
        return self.name
