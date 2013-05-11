import os
import MySQLdb
from MySQLdb.cursors import DictCursor

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "elvis.settings")
from elvis.models.tag import Tag
from elvis.models.tag_hierarchy import TagHierarchy
from elvis.models.composer import Composer

COMPOSERS_QUERY = """SELECT td.tid AS old_id, td.name, dt.field_dates_value AS birth_date,
                      dt.field_dates_value2 AS death_date FROM taxonomy_term_data td
                     LEFT JOIN field_data_field_dates dt on td.tid = dt.entity_id
                     WHERE td.vid = 3"""

PIECE_QUERY = """SELECT rv.title, cp.field_composer_tid AS composer_id, rv.nid AS old_id,
                 rv.uid AS uploader FROM node n
                  LEFT JOIN node_revision rv ON (n.vid = rv.vid)
                  LEFT JOIN field_data_field_composer cp ON (rv.vid = cp.revision_id)
                  WHERE n.type=\"piece\""""

CORPUS_QUERY = """SELECT rv.title, rv.nid AS old_id, rv.uid AS uploader FROM node n
                  LEFT JOIN node_revision rv ON (n.vid = rv.vid)
                  WHERE n.type=\"corpus\""""

MOVEMENT_QUERY = """SELECT rv.title, rv.nid AS old_id, rv.uid AS uploader FROM node n
                  LEFT JOIN node_revision rv ON (n.vid = rv.vid)
                  WHERE n.type=\"movement\""""

TAG_QUERY = """SELECT td.name, td.description, td.tid AS old_id FROM taxonomy_term_data td"""

TAG_HIERARCHY_QUERY = """SELECT * FROM taxonomy_term_hierarchy"""


class DumpDrupal(object):
    def __init__(self):
        self.conn = MySQLdb.connect(host="localhost", user="root", cursorclass=DictCursor, db="ddmal_elvis")
        self.curs = self.conn.cursor()

        # curs.execute(PIECE_QUERY)
        # curs.execute(TAG_QUERY)
        # pieces = curs.fetchall()
        self.get_tags()
        self.get_composers()

    def get_composers(self):
        self.curs.execute(COMPOSERS_QUERY)
        composers = self.curs.fetchall()

        print "Deleting composer objects"
        Composer.objects.all().delete()

        print "Adding composers"
        for composer in composers:
            c = Composer(**composer)
            c.save()


    def get_tags(self):
        self.curs.execute(TAG_QUERY)
        tags = self.curs.fetchall()

        print "Deleting all tags"
        Tag.objects.all().delete()

        print "Adding tags"
        for tag in tags:
            t = Tag(**tag)
            t.save()

        print "Deleting tag hierarchy"
        TagHierarchy.objects.all().delete()

        print "Adding tag hierarchy"
        self.curs.execute(TAG_HIERARCHY_QUERY)
        tag_hierarchy = self.curs.fetchall()
        for t in tag_hierarchy:
            tag = Tag.objects.get(old_id=t.get('tid', None))
            if not t.get('parent') == 0:
                parent = Tag.objects.get(old_id=t.get('parent', None))
            else:
                parent = None
            t = TagHierarchy(tag=tag, parent=parent)
            t.save()


if __name__ == "__main__":
    x = DumpDrupal()
