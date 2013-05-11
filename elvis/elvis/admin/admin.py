from django.contrib import admin

from elvis.models.piece import Piece
from elvis.models.corpus import Corpus
from elvis.models.composer import Composer
from elvis.models.movement import Movement

class PieceAdmin(admin.ModelAdmin):
    pass


class CorpusAdmin(admin.ModelAdmin):
    pass


# Can display CSS here

class ComposerAdmin(admin.ModelAdmin):
	def upper_case_name(obj): return ("%s" % (obj.name)).upper()
	
	upper_case_name.short_description = 'name'

	list_display = ("name", "birth_date", "death_date")

	#list_display = (upper_case_name,)


class MovementAdmin(admin.ModelAdmin):
	pass

# Indicates that these objects have admin interface 

admin.site.register(Piece, PieceAdmin)
admin.site.register(Corpus, CorpusAdmin)
admin.site.register(Composer, ComposerAdmin)
admin.site.register(Movement, MovementAdmin)
