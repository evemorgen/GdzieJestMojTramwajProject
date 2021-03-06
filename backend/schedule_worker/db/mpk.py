import os
import logging
import sqlite3


class MpkDb():
    def __init__(self):
        self.db_file = os.environ['TRAM_ROOT'] + '/data/baza.ready.zip'
        self.db_connection = sqlite3.connect(self.db_file)
        self.cursor = self.db_connection.cursor()

    def get_lines(self):
        logging.info('getting all lines numbers')
        self.cursor.execute('select name from lines;')
        return [x[0] for x in self.cursor.fetchall()]

    def get_line_points(self, line):
        query = """
        select VariantId, pointId
        from routes
        where VariantId in (
            select id
            from Variants
            where SheduleId = (
                select ID
                from Shedules
                where LineName = %s
                order by LastUpdate DESC
                limit 1
            ) and "Default" = 1
        );
        """ % line
        self.cursor.execute(query)
        points_dict = {}
        data = self.cursor.fetchall()
        for tupel in data:
            points_dict[tupel[0]] = []
        for tupel in data:
            points_dict[tupel[0]] += [tupel[1]]
        return points_dict

    def get_variants_for_line(self, linia):
        query = """
                select id
                from Variants
                where SheduleId = (
                    select ID
                    from Shedules
                    where LineName = %s
                    order by LastUpdate DESC
                    limit 1
                ) and "Default" = 1
                """
        self.cursor.execute(query % linia)
        warianty = [tupel[0] for tupel in self.cursor.fetchall()]
        return warianty

    def get_stops_for_variant(self, variant_id):
            query = """
                    select No, StopName
                    from routes
                    where VariantId = %s
                    """
            self.cursor.execute(query % variant_id)
            przystanki = [tupel[1] for tupel in self.cursor.fetchall()]
            return przystanki
