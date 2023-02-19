from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator
import re
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
# telephone nbm validator

class MetaTags(models.Model):
    meta_deck = models.JSONField('Meta desk', blank=True, null=True)
    meta_keys = models.JSONField('Meta keys', blank=True, null=True)



def telephone_validator(value):
    number_temp = r"\+998\d{9}"
    if bool(re.match(number_temp, value)) == False:
        raise ValidationError(
            ("Your telephone number is invalid"),
            params={'value': value}
        )


# Create your models here.
class StaticInformation(models.Model):
    title = models.JSONField('Заголовок сайта', blank=True, null=True)
    subtitle = models.JSONField('Подзаголовок сайта', blank=True, null=True)
    deskription = models.JSONField("Описание сайта", blank=True, null=True)
    about_us = models.JSONField("О нас", blank=True, null=True)
    adres = models.JSONField("Адрес", blank=True, null=True)
    logo_first = ThumbnailerImageField("Лого сайта", blank=True, null=True, upload_to='site_logo')
    logo_second = ThumbnailerImageField("Второе лого", blank=True, null=True, upload_to='site_logo')
    email = models.EmailField("Эмейл", blank=True, null=True)
    twitter = models.URLField("Ссылка на телеграм", blank=True, null=True, max_length=255)
    instagram = models.URLField("Ссылка на инстаграм", blank=True, null=True, max_length=255)
    facebook = models.URLField("Ссылка на фэйсбук", blank=True, null=True, max_length=255)
    linked_in = models.URLField("Ютуб", blank=True, null=True, max_length=255)
    nbm = models.CharField("Номер телефона", blank=True, null=True, max_length=255)
    map = models.TextField('Iframe карты', blank=True, null=True)
    work_time = models.JSONField('Время работы', blank=True, null=True)


    class Meta:
        verbose_name = 'static_inf'


    def __str__(self):
        return 'Static information'


# article categories
class ArticleCategories(models.Model):
    name = models.JSONField('Заголовок', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    image = ThumbnailerImageField(upload_to='article_group_image', blank=True, null=True)

    class Meta:
        verbose_name = 'ArticleCategory'

# blog 
class Articles(models.Model):
    image = ThumbnailerImageField(upload_to='article_images', blank=True, null=True)
    title = models.JSONField('Заголовок')
    subtitle = models.JSONField('Пост заголовок')
    body = models.JSONField("Статья")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    likes = models.IntegerField('Лайки', default=0)
    created_date = models.DateField()
    active = models.BooleanField(default=True, editable=True)
    category = models.ManyToManyField(ArticleCategories, blank=True, null=True, related_name='articles')
    meta = models.ForeignKey(MetaTags, on_delete=models.CASCADE, blank=True, null=True)


    def get_format_data(self):
        return str(self.created_date.year) + '-' + str(self.created_date.month) + '-' + str(self.created_date.day)

    def get_dot_date(self):
        m = str(self.created_date.month)
        if len(m) == 1:
            m = '0' + m

        d = str(self.created_date.day)
        if len(d) == 1:
            d = '0' + d

        return d + '.' + m + '.' + str(self.created_date.year)


    class Meta:
        verbose_name = 'articles'


@receiver(post_delete, sender=Articles)
def article_delete_image(sender, instance, *args, **kwargs):
    """ Clean Old Image file """
    try:
        instance.image.delete(save=False)
    except:
        pass



# article images
class ArticleImages(models.Model):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name='images')
    image = ThumbnailerImageField(upload_to='article_images')

    class Meta:
        verbose_name = 'art_images'



# languages
class Languages(models.Model):
    name = models.CharField('Названия', max_length=255, blank=True, null=True)
    code = models.CharField('Код языка', max_length=255, blank=True, null=True, unique=True)
    icon = ThumbnailerImageField(upload_to='lng_icon', blank=True, null=True)
    active = models.BooleanField(default=False)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'lang'





# translation groups
class TranlsationGroups(models.Model):
    title = models.CharField('Название', max_length=255, unique=True)
    sub_text = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'transl_group'


# translations
class Translations(models.Model):
    group = models.ForeignKey(TranlsationGroups, on_delete=models.CASCADE, related_name='translations')
    key = models.CharField(max_length=255)
    value = models.JSONField("Значение")


    def __str__(self):
        return f'{self.group.sub_text}.{self.key}'

    class Meta:
        verbose_name = 'transl'
        unique_together = ['key', 'group']



# inputs model
class AdminInputs(models.Model):
    inputs = models.JSONField('Input', blank=True, null=True)



# about us
class AboutUs(models.Model):
    title_one = models.JSONField('Title', blank=True, null=True)
    title_second = models.JSONField('Title', blank=True, null=True)
    text_first = models.JSONField("Text", blank=True, null=True)
    text_second = models.JSONField("Text", blank=True, null=True)
    video = models.FileField('Video', upload_to='about_us', blank=True, null=True)


# about us images
class AboutUsImages(models.Model):
    parent = models.ForeignKey(AboutUs, on_delete=models.CASCADE, related_name='images', blank=True, null=True)
    image = ThumbnailerImageField(upload_to='about_us_images', blank=True, null=True)


# parntners
class Partners(models.Model):
    title = models.JSONField('Title', blank=True, null=True)
    image = ThumbnailerImageField(upload_to='partner_images', blank=True, null=True)


# servises
class Services(models.Model):
    title = models.JSONField('Title', blank=True, null=True)
    sub_title = models.JSONField('Sub title', blank=True, null=True)
    deckription = models.JSONField('Deckription', blank=True, null=True)
    image = ThumbnailerImageField(upload_to='service_images', blank=True, null=True)
    order = models.PositiveIntegerField('Order', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    meta_field = models.ForeignKey(MetaTags, on_delete=models.CASCADE, blank=True, null=True)


@receiver(post_delete, sender=Services)
def post_save_image(sender, instance, *args, **kwargs):
    """ Clean Old Image file """
    try:
        instance.image.delete(save=False)
    except:
        pass


# reviews
class Reviews(models.Model):
    image = ThumbnailerImageField(upload_to='rev_image', blank=True, null=True)
    title = models.JSONField("Title", blank=True, null=True)
    text = models.JSONField('Text', blank=True, null=True)
    active = models.BooleanField('Active', default=True)
