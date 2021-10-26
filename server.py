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
            query = self.request.body.decode('utf-8')
            query_elements = query.split('&')
            query_dict = {   # sous-optimal, mais les boucles sont interdites en asyncio
                'user': query_elements[6].split('=')[1],
                'message': query_elements[8].split('=')[1],
                'response_url': query_elements[-2].split('=')[1],
                'trigger_id': query_elements[-1].split('=')[1],
                }
            self.write_theme_to_db(query_dict)
            response = {
                "response_type": "in_channel",
                "text": f"Bien noté, #{query_dict['user']} !"
                }

            logging.info(f'Processed message {query}')
        except Exception as e:
            response = {'response': traceback.format_exc()}
            logging.error(traceback.format_exc())
        self.set_header('Content-type', 'application/json')
        self.write(json.dumps(response))


def make_app(db_path):
    return tornado.web.Application([
        (r"/", ThemePostingHandler, {'db_path': db_path}),
    ])


if __name__ == "__main__":
    db_path = '/home/lucie/bot/themes.csv'
    app = make_app(db_path)
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
