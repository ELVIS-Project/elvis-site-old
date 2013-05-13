import os
import datetime
import MySQLdb
from django.core.files import File
from MySQLdb.cursors import DictCursor

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "elvis.settings")
from elvis.models.tag import Tag
from elvis.models.tag_hierarchy import TagHierarchy
from elvis.models.composer import Composer
from django.contrib.auth.models import User
from elvis.models.corpus import Corpus
from elvis.models.piece import Piece
from elvis.models.attachment import Attachment
from elvis.models.movement import Movement

ELVIS_USERS = """SELECT DISTINCT u.uid, u.name, u.mail, u.created, u.access, u.login FROM users u
                LEFT JOIN users_roles ur ON u.uid = ur.uid
                LEFT JOIN role r ON ur.rid = r.rid
                WHERE ur.rid IN (5, 6, 4)"""

COMPOSERS_QUERY = """SELECT td.tid AS old_id, td.name, dt.field_dates_value AS birth_date,
                      dt.field_dates_value2 AS death_date FROM taxonomy_term_data td
                     LEFT JOIN field_data_field_dates dt on td.tid = dt.entity_id
                     WHERE td.vid = 3"""

PIECE_QUERY = """SELECT rv.title, cp.field_composer_tid AS composer_id, rv.nid AS old_id,
                 rv.uid AS uploader, fd.field_date_value AS date_of_composition,
                 fv.field_voices_value AS number_of_voices, fc.field_comment_value AS comment,
                 n.created AS created, n.changed AS updated, b.bid AS book_id FROM node n
                  LEFT JOIN node_revision rv ON (n.vid = rv.vid)
                  LEFT JOIN field_data_field_composer cp ON (rv.vid = cp.revision_id)
                  LEFT JOIN field_data_field_date fd ON (fd.revision_id = rv.vid)
                  LEFT JOIN field_data_field_voices fv ON (fv.revision_id = rv.vid)
                  LEFT JOIN field_data_field_comment fc ON (fc.revision_id = rv.vid)
                  LEFT JOIN book b ON (n.nid = b.nid)
                  WHERE n.type=\"piece\""""

CORPUS_QUERY = """SELECT rv.title, rv.nid AS old_id, rv.uid AS creator, cc.field_corpus_comment_value AS comment FROM node n
                  LEFT JOIN node_revision rv ON (n.vid = rv.vid)
                  LEFT JOIN field_revision_field_corpus_comment cc ON (cc.revision_id = n.vid)
                  WHERE n.type=\"corpus\""""

MOVEMENT_QUERY = """SELECT rv.title, cp.field_composer_tid AS composer_id, n.nid AS old_id,
                 rv.uid AS uploader, fd.field_date_value AS date_of_composition,
                 fv.field_voices_value AS number_of_voices, fc.field_comment_value AS comment FROM node n
                  LEFT JOIN node_revision rv ON (n.vid = rv.vid)
                  LEFT JOIN field_data_field_composer cp ON (rv.vid = cp.revision_id)
                  LEFT JOIN field_data_field_date fd ON (fd.revision_id = rv.vid)
                  LEFT JOIN field_data_field_voices fv ON (fv.revision_id = rv.vid)
                  LEFT JOIN field_data_field_comment fc ON (fc.revision_id = rv.vid)
                  WHERE n.type=\"movement\""""

TAG_QUERY = """SELECT td.name, td.description, td.tid AS old_id FROM taxonomy_term_data td"""

TAG_HIERARCHY_QUERY = """SELECT * FROM taxonomy_term_hierarchy"""

ATTACHMENT_QUERY = """"""


class DumpDrupal(object):
    def __init__(self):
        # curs.execute(PIECE_QUERY)
        # curs.execute(TAG_QUERY)
        # pieces = curs.fetchall()
        self.get_tags()
        self.get_composers()
        # self.get_users()
        self.get_corpus()
        self.get_pieces()

    def __connect(self):
        self.conn = MySQLdb.connect(host="localhost", user="root", cursorclass=DictCursor, db="ddmal_elvis")
        self.curs = self.conn.cursor()

    def __disconnect(self):
        self.curs.close()
        self.conn.close()

    def __get_ddmal_users(self):
        conn = MySQLdb.connect(host="localhost", user="root", cursorclass=DictCursor, db="ddmal_drupal")
        curs = conn.cursor()

        curs.execute(ELVIS_USERS)
        u = curs.fetchall()
        curs.close()
        conn.close()
        return u

    def get_corpus(self):
        users = self.__get_ddmal_users()
        self.__connect()

        self.curs.execute(CORPUS_QUERY)
        corpus = self.curs.fetchall()
        print "Deleting corpora"
        Corpus.objects.all().delete()

        print "Adding corpora"
        for corp in corpus:
            for user in users:
                if corp.get('creator') == user.get('uid'):
                    u = User.objects.get(username=user.get('name'))
                    break
            corp['creator'] = u
            x = Corpus(**corp)
            x.save()

        self.__disconnect()


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
                'date_joined': datetime.datetime.fromtimestamp(user.get('created')),
                'email': user.get('mail')
            }
            x = User(**u)
            x.save()

        curs.close()
        conn.close()

    def get_composers(self):
        self.__connect()
        self.curs.execute(COMPOSERS_QUERY)
        composers = self.curs.fetchall()

        print "Deleting composer objects"
        Composer.objects.all().delete()

        print "Adding composers"
        for composer in composers:
            c = Composer(**composer)
            c.save()
        self.__disconnect()

    def get_tags(self):
        self.__connect()
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

        self.__disconnect()

    def get_attachments(self):
        self.curs.execute(ATTACHMENT_QUERY)

    def get_pieces(self):
        users = self.__get_ddmal_users()

        self.__connect()
        self.curs.execute(PIECE_QUERY)
        pieces = self.curs.fetchall()

        print "Deleting Pieces"
        Piece.objects.all().delete()

        print "Adding Pieces"
        for piece in pieces:
            composer_obj = Composer.objects.get(old_id=piece['composer_id'])
            for user in users:
                if piece.get('uploader') == user.get('uid'):
                    user_obj = User.objects.get(username=user.get('name'))
                    break

            corpus_obj = Corpus.objects.filter(old_id=piece['book_id'])
            if not corpus_obj.exists():
                corpus_obj = None
            else:
                corpus_obj = corpus_obj[0]

            p = {
                'uploader': user_obj,
                'corpus': corpus_obj,
                'composer': composer_obj,
                'old_id': piece.get('old_id', None),
                'title': piece.get('title', None),
                'date_of_composition': piece.get('date_of_composition', None),
                'number_of_voices': piece.get('number_of_voices', None),
                'comment': piece.get('comment', None),
                'created': datetime.datetime.fromtimestamp(piece.get('created')),
                'updated': datetime.datetime.fromtimestamp(piece.get('updated'))
            }
            x = Piece(**p)
            x.save()
        self.__disconnect()

        print "Tagging pieces"
        PIECE_TAG_QUERY = """SELECT ti.nid, ti.tid FROM taxonomy_index ti
                             WHERE ti.nid = %s"""

        pieces = Piece.objects.all()

        for piece in pieces:
            self.__connect()
            self.curs.execute(PIECE_TAG_QUERY, piece.old_id)
            tags = self.curs.fetchall()
            for tag in tags:
                tag_obj = Tag.objects.filter(old_id=tag.get('tid'))
                if not tag_obj.exists():
                    continue
                piece.tags.add(tag_obj[0])
                piece.save()

            self.__disconnect()

        PIECE_ATTACHMENT_QUERY = """SELECT ff.field_files_description AS description, fm.timestamp AS created,
                                    fm.uid AS uploader, fm.filename AS filename, fm.uri AS uri FROM field_data_field_files ff
                                    LEFT JOIN file_managed fm ON ff.field_files_fid = fm.fid
                                    WHERE ff.entity_id = %s"""
        print "Attaching files"
        pieces = Piece.objects.all()
        Attachment.objects.all().delete()
        old_file_path = ""  # path to the old drupal files.
        self.__connect()
        for piece in pieces:
            self.curs.execute(PIECE_ATTACHMENT_QUERY, piece.old_id)
            attachments = self.curs.fetchall()
            for attachment in attachments:
                for user in users:
                    if attachment.get('uploader') == user.get('uid'):
                        user_obj = User.objects.get(username=user.get('name'))
                        break

                a = Attachment()
                a.save()  # ensure we've got a PK before we try and attach a file.

                # filename = attachment.get('filename')[9:]  # lop the 'public://' off.
                filename = "test_file.mei"  # for testing.

                filepath = os.path.join(old_file_path, filename)
                f = open(filepath, 'rb')

                attached_file = os.path.join(a.attachment_path, filename)
                print "attached file: {0}".format(attached_file)
                s = {
                    'uploader': user_obj,
                    'description': attachment.get('description', None),
                    'created': datetime.datetime.fromtimestamp(attachment.get('created')),
                    'old_id': attachment.get('old_id', None)
                }
                a.__dict__.update(**s)
                a.save()

                a.attachment.save(filename, File(f))
                a.save()
                f.close()
                piece.attachments.add(a)

        self.__disconnect()



if __name__ == "__main__":
    x = DumpDrupal()
