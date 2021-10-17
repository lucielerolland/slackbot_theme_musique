import tornado.web
import tornado.ioloop
import json
import logging
import traceback
import os


class ThemePostingHandler(tornado.web.RequestHandler):
    def initialize(self, db_path):
        self.db_path = db_path

    def get(self):
        self.write('Bibibababu')

    def write_theme_to_db(self, query):
        csv_line = ';'.join([query['user'], query['message']])
        mode = 'a' if os.path.exists(self.db_path) else 'w+'
        with open(self.db_path, mode) as writer:
            writer.write(csv_line)

    def post(self):
        logging.info(f'Received request {self.request.body}')
        try:
            query = json.loads(self.request.body)
            self.write_theme_to_db(query)
            response = 'ok'
            logging.info(f'Processed message {query}')
        except Exception as e:
            response = traceback.format_exc()
            logging.error(traceback.format_exc())
        self.write(json.dumps({'response': response}))


def make_app(db_path):
    return tornado.web.Application([
        (r"/", ThemePostingHandler, {'db_path': db_path}),
    ])


if __name__ == "__main__":
    db_path = '/home/lucie/bot/themes.csv'
    app = make_app(db_path)
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
