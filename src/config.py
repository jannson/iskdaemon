# -*- coding: UTF-8 -*-
import logging

#IMAGE_FOLDER = "/home/janson/projects/elastic/tmp/mirflickr"
IMAGE_FOLDER = "/home/janson/download/baidu-yun"
ES_SERVER_ENDPOINT = "http://127.0.0.1:9200"
#IMAGE_BASE_URL = "/image"
IMAGE_BASE_URL = "http://127.0.0.1:4869"
STATIC_BASE_URL = "/static"
INDEX_NAME = "testb"
TYPE_NAME = "testb"
#INDEX_FEATURES = ["CEDD", "JCD", "COLOR_LAYOUT", "OPPONENT_HISTOGRAM", "SCALABLE_COLOR", "JOINT_HISTOGRAM", "FCTH", "EDGE_HISTOGRAM", "PHOG"]
#INDEX_FEATURES = ["CEDD", "JCD", "COLOR_LAYOUT", "OPPONENT_HISTOGRAM", "JOINT_HISTOGRAM", "FCTH", "EDGE_HISTOGRAM", "PHOG"]
#INDEX_FEATURES = ["CEDD", "JCD", "FCTH"]
INDEX_FEATURES = [u"test1", u"test2"]
SEARCH_HASH_LIMIT = 1000
RESULT_SIZE = 24
INDEX_LOG_INTERVAL = 10
IGNORE_EXIST = True
IMAGE_EXTENSIONS = ["jpg", "png", 'jpeg']
LOGGING_LEVEL = logging.DEBUG
TEMPLATE_CACHE_DIR = None

IS_RELEASE=True