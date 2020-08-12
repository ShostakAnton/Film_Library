from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from .models import Category, Genre, Movie, MovieShots, Actor, Rating, RatingStar, Reviews

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from modeltranslation.admin import TranslationAdmin


class MovieAdminForm(forms.ModelForm):
    description_ru = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())
    description_en = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())


class Meta:
    model = Movie
    fields = '__all__'


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    """Категории"""
    list_display = ("name", "url")
    list_display_links = ("name",)


class ReviewInline(admin.TabularInline):  # TabularInline - информация по горизонтали
    # class ReviewInline(admin.StackedInline):      StackedInline - информация по вертикали
    """Отзывы на странице фильма"""
    model = Reviews
    extra = 1  # количество дополнитеьных полей для добавления
    readonly_fields = ("name", "email")  # доступны только для чтения


class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')

    get_image.short_description = "Изображение"


@admin.register(Movie)
class MovieAdmin(TranslationAdmin):
    """Фильмы"""
    list_display = ("title", "category", "url", "draft")
    list_filter = ("category", "year")
    search_fields = ("title", "category__name")
    inlines = [MovieShotsInline, ReviewInline]  # добавление на админ-страницу другую модель
    save_on_top = True  # панель сохранения вверху
    save_as = True  # кнопка "сохранить как новый обьект"
    list_editable = ("draft",)  # для редактирования полей прамо со списка
    actions = ["publish", "unpublish"]      # добавление атрибутов в поле actions
    form = MovieAdminForm
    # fields = ("actors", "directors", "genres", "category")        # какие поля должны отображаться
    readonly_fields = ("get_image",)
    fieldsets = (  # для группировки полей
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": ("description", ("poster", "get_image"))
        }),
        (None, {
            "fields": (("year", "world_premiere", "country"),)
        }),
        ("Actors", {
            "classes": ("collapse",),  # в свернутом виде
            "fields": (("actors", "directors", "genres", "category"),)
        }),
        (None, {
            "fields": (("budget", "fees_in_usa", "fess_in_world"),)
        }),
        ("Options", {
            "fields": (("url", "draft"),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height="110"')

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)  # обновляем запись draft
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)  # обновляем запись draft
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Опубликовать"  # добавление нового столбца
    publish.allowed_permissions = ('change',)  # у пользователя должны быть права на изменение данного поля

    unpublish.short_description = "Снять с публикации"  # добавление нового столбца
    unpublish.allowed_permissions = ('change',)  # у пользователя должны быть права на изменение данного поля

    get_image.short_description = "Постер"


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы"""
    list_display = ("name", "email", "parent", "movie", "id")
    readonly_fields = ("name", "email")  # запретить изменять указаные поля (доступны только для чтения)


@admin.register(Genre)
class GenreAdmin(TranslationAdmin):
    """Жанры"""
    list_display = ("name", "url")


@admin.register(Actor)
class ActorAdmin(TranslationAdmin):
    """Актеры"""
    list_display = ("name", "age", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')  # mark_safe служит для вывода тега

    get_image.short_description = "Изображение"  # название столбца


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("movie", "ip", "star")


@admin.register(MovieShots)
class MovieShotsAdmin(TranslationAdmin):
    """Кадры из фильма"""
    list_display = ("title", "movie", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')  # mark_safe служит для вывода тега

    get_image.short_description = "Изображение"  # название столбца


admin.site.register(RatingStar)

admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"
