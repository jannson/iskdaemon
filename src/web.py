import base64
import json
import logging
from os.path import join
from jinja2 import Environment, FileSystemLoader, FileSystemBytecodeCache
import tornado
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.options import define, options
from tornado.web import HTTPError
from tornado import gen

from isk_test import server as simserver, imgdb, simpledb
import config

cache = None
if config.TEMPLATE_CACHE_DIR:
    cache = FileSystemBytecodeCache(directory=config.TEMPLATE_CACHE_DIR)
env = Environment(loader=FileSystemLoader("template"),
                  bytecode_cache=cache, cache_size=100,
                  trim_blocks=True)


class BaseHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        raise HTTPError(404)

    def render_template(self, template_name, template_args=None):
        if not template_args:
            template_args = {}
        template = env.get_template(template_name)
        html = template.render(template_args)
        self.write(html)
        self.finish()

    def get_single_argument(self, name):
        l = self.get_arguments(name=name)
        if l and len(l) > 0:
            return l[0]
        return None


class IndexPageHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        img = self.get_single_argument("img")
        url = self.get_single_argument("url")
        filename = ""
        md5 = ""
        search_keyword = ""

        if img is not None:
            curr_img = simpledb.get_by_img(int(img))
            search_result = simpledb.sim_imgs(simserver, imgdb, int(img))
            filename = curr_img["path"]
            md5 = curr_img["md5"]
        elif url is not None:
            if url.startswith("http:"):
                http_client = AsyncHTTPClient()
                image_response = yield http_client.fetch(url)
                if image_response.code >= 400:
                    raise HTTPError(500)
                search_result = simpledb.sim_data(simserver, imgdb, image_response.body)
            else:
                search_keyword = url
                print search_keyword
                search_result = simpledb.search(url)
                url = ""
        else:  # no need to search, return random images
            search_result = simpledb.random(30)
        args = {
            "search_result": search_result,
            "search_file_name": filename,
            "md5": md5,
            "search_url": url,
            "search_keyword": search_keyword,
            "image_base_url": config.IMAGE_BASE_URL,
            "static_base_url": config.STATIC_BASE_URL
        }
        self.render_template("index.html", template_args=args)




settings = {
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
}
application = tornado.web.Application([
    (r"/", IndexPageHandler),
    (r'/image/(.*)', tornado.web.StaticFileHandler, {'path': config.IMAGE_FOLDER}),
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': "static"}),
], **settings)




define("port", default=8001, help="run on the given port", type=int)


if __name__ == "__main__":
    #options.logging = config.LOG_CONSOLE_LEVEL
    options.parse_command_line()

    logging.info("Start on port: " + str(options.port))

    from tornado.httpserver import HTTPServer
    server = HTTPServer(application, xheaders=True)
    loop = tornado.ioloop.IOLoop.instance()

    server.listen(port=options.port)
    loop.start()
