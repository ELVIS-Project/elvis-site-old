import os
import datetime
import MySQLdb
from MySQLdb.cursors import DictCursor

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "elvis.settings")
from elvis.models.tag import Tag
from elvis.models.tag_hierarchy import TagHierarchy
from elvis.models.composer import Composer
from django.contrib.auth.models import User
from elvis.models.corpus import Corpus

ELVIS_USERS = """SELECT DISTINCT u.uid, u.name, u.mail, u.created, u.access, u.login FROM users u
                LEFT JOIN users_roles ur ON u.uid = ur.uid
                LEFT JOIN role r ON ur.rid = r.rid
                WHERE ur.rid IN (5, 6, 4)"""

COMPOSERS_QUERY = """SELECT td.tid AS old_id, td.name, dt.field_dates_value AS birth_date,
                      dt.field_dates_value2 AS death_date FROM taxonomy_term_data td
                     LEFT JOIN field_data_field_dates dt on td.tid = dt.entity_id
                     WHERE td.vid = 3"""

PIECE_QUERY = """SELECT rv.title, cp.field_composer_tid AS composer_id, rv.nid AS old_id,
                 rv.uid AS uploader FROM node n
                  LEFT JOIN node_revision rv ON (n.vid = rv.vid)
                  LEFT JOIN field_data_field_composer cp ON (rv.vid = cp.revision_id)
                  WHERE n.type=\"piece\""""

CORPUS_QUERY = """SELECT rv.title, rv.nid AS old_id, rv.uid AS creator, cc.field_corpus_comment_value AS comment FROM node n
                  LEFT JOIN node_revision rv ON (n.vid = rv.vid)
                  LEFT JOIN field_revision_field_corpus_comment cc ON (cc.revision_id = n.vid)
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
        # self.get_users()
        self.get_corpus()

    def __get_ddmal_users(self):
        conn = MySQLdb.connect(host="localhost", user="root", cursorclass=DictCursor, db="ddmal_drupal")
        curs = conn.cursor()

        curs.execute(ELVIS_USERS)
        return curs.fetchall()

    def get_corpus(self):
        users = self.__get_ddmal_users()
        print users
        self.curs.execute(CORPUS_QUERY)
        corpus = self.curs.fetchall()

        Corpus.objects.all().delete()

        for corp in corpus:
            for user in users:
                if corp.get('creator') == user.get('uid'):
                    u = User.objects.get(username=user.get('name'))
                    break
            corp['creator'] = u
            x = Corpus(**corp)
            x.save()

    def get_users(self):
        conn = MySQLdb.connect(host="localhost", user="root", cursorclass=DictCursor, db="ddmal_drupal")
        curs = conn.cursor()

        curs.execute(ELVIS_USERS)
        users = curs.fetchall()
        for user in users:
            print "Creating {0}".format(user.get('name'))
            u = {
                'is_active': True,
                'username': user.get('name'),
                'last_login': datetime.datetime.fromtimestamp(user.get('login')),
                'date_joined': datetime.datetime.fromtimestamp(user.get('created'))
            }
            x = User(**u)
            x.save()


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
