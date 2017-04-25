import pymysql


class DBUtil(object):
    def __init__(self):
        self.connection = None

    def create_index(self, img_id, web_id, img_url, page_url, tags):
        self.get_connection()

        try:
            with self.connection.cursor() as cursor:
                img_insert_stmt = "INSERT INTO `images` (`img_id`, `url`, `page_url`) VALUES(%s, %s, %s)"
                img_tags_rel_stmt = "INSERT INTO `imgtags`(`img_id`, `tag_id`) VALUES" + \
                                    ",".join("(%s, %s)" for tag in tags)

                cursor.execute(img_insert_stmt, (img_id, img_url, page_url))

                # Construct the insert query for tagging
                num_tags = len(tags)
                tag_list = [0] * (num_tags * 2)
                for i in xrange(num_tags):
                    tag_list[2 * i] = img_id
                    tag_list[2 * i + 1] = tags[i]
                cursor.execute(img_tags_rel_stmt, tag_list)

                self.connection.commit()

        finally:
            self.connection.close()

    def get_connection(self):
        self.connection = pymysql.connect(host='localhost',
                                          user='root',
                                          password='root',
                                          db='capstone',
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)
