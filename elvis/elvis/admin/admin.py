from django.contrib import admin

from elvis.models.piece import Piece
from elvis.models.corpus import Corpus
from elvis.models.composer import Composer
from elvis.models.tag import Tag
from elvis.models.tag_hierarchy import TagHierarchy


class PieceAdmin(admin.ModelAdmin):
    pass


class CorpusAdmin(admin.ModelAdmin):
    pass


class ComposerAdmin(admin.ModelAdmin):
    list_display = ("name", "birth_date", "death_date")


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "old_id")


class TagHierarchyAdmin(admin.ModelAdmin):
    list_display = ("tag", "parent")


admin.site.register(TagHierarchy, TagHierarchyAdmin)
admin.site.register(Piece, PieceAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Corpus, CorpusAdmin)
admin.site.register(Composer, ComposerAdmin)
