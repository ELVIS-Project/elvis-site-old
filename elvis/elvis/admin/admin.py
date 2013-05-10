from django.contrib import admin

from elvis.models.piece import Piece
from elvis.models.corpus import Corpus


class PieceAdmin(admin.ModelAdmin):
    pass


class CorpusAdmin(admin.ModelAdmin):
    pass


admin.site.register(Piece, PieceAdmin)
admin.site.register(Corpus, CorpusAdmin)
