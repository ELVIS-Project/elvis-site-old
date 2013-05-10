import MySQLdb
from MySQLdb.cursors import DictCursor

COMPOSERS_QUERY = """SELECT td.tid AS old_id, td.name, dt.field_dates_value AS birth_date, dt.field_dates_value2 AS death_date FROM taxonomy_term_data td
                     LEFT JOIN field_data_field_dates dt on td.tid = dt.entity_id
                     WHERE td.vid = 3"""

PIECE_QUERY = """SELECT rv.title, cp.field_composer_tid AS composer_id, rv.nid AS old_id,
                 rv.uid AS uploader, td.name AS tag_name FROM node n
                  LEFT JOIN node_revision rv ON (n.vid = rv.vid)
                  LEFT JOIN field_data_field_composer cp ON (rv.vid = cp.revision_id)
                  LEFT JOIN field_data_field_tags tg ON (rv.vid = cp.revision_id)
                  LEFT JOIN taxonomy_term_data td ON (td.tid = tg.field_tags_tid)
                  WHERE n.type=\"piece\""""

CORPUS_QUERY = """SELECT rv.title, rv.nid AS old_id, rv.uid AS uploader FROM node n
                  LEFT JOIN node_revision rv ON (n.vid = rv.vid)
                  WHERE n.type=\"corpus\""""

MOVEMENT_QUERY = """SELECT rv.title, rv.nid AS old_id, rv.uid AS uploader FROM node n
                  LEFT JOIN node_revision rv ON (n.vid = rv.vid)
                  WHERE n.type=\"movement\""""


class DumpDrupal(object):
    def __init__(self):
        conn = MySQLdb.connect(host="localhost", user="root", cursorclass=DictCursor, db="ddmal_elvis")
        curs = conn.cursor()

        curs.execute(PIECE_QUERY)
        pieces = curs.fetchall()
        print pieces


if __name__ == "__main__":
    x = DumpDrupal()
