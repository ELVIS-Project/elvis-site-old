from django.contrib import admin

from elvis.models.piece import Piece
from elvis.models.corpus import Corpus
from elvis.models.composer import Composer


class PieceAdmin(admin.ModelAdmin):
    pass


class CorpusAdmin(admin.ModelAdmin):
    pass


class ComposerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Piece, PieceAdmin)
admin.site.register(Corpus, CorpusAdmin)
admin.site.register(Composer, ComposerAdmin)
