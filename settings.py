# Scrapy settings for kick project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'kick'

SPIDER_MODULES = ['kick.spiders']
NEWSPIDER_MODULE = 'kick.spiders'

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'

DOWNLOADER_MIDDLEWARES = {
    # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'kick.smartproxy_auth.ProxyMiddleware': 100,
    'kick.middlewares.KickSpiderMiddleware': 543,
    # 'kick.middlewares.SimpleProxyMiddleware': 540,

}
SMARTPROXY_USER = 'ldlucien' ## Smartproxy Username (Sub-user)
SMARTPROXY_PASSWORD = '12345678' ## Password for your user
SMARTPROXY_ENDPOINT = 'gate.dc.smartproxy.com' ## Endpoint you'd like to use
SMARTPROXY_PORT = '20000' ## Port of the endpoint you are using.
ITEM_PIPELINES = {
   # 'tutorial.pipelines.QQNewsPipeline': 300,
   # 'kick.pipelines.KickMongoPipeline':400
    'kick.pipelines.KickStoryPipeline': 400
   #  'kick.pipelines.KickUpdatesCommentsPipeline': 400

    # ,
    # 'kick.pipelines.KickFAQPipeline': 400

}
MONGO_URI = 'mongodb://localhost:27017'
MONGO_DB = "kick"
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'kick (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True
# PROXY_URL = 'https://dps.kdlapi.com/api/getdps/?orderid=949911939411124&num=10&pt=1&format=json&sep=1'
PROXY_URL = "https://proxy6.net/api/ad42a35cb3-e8fe6b14d1-6aca5e500f/getproxy"
# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 6
# import logging
#
# LOG_ENABLED=True
#
# # 日志使用的编码
# LOG_ENCODING='utf-8'
# #
# # 日志文件(文件名)
# LOG_FILE="kick"
#
# 日志格式
# LOG_FORMAT='%(asctime)s [%(name)s] %(levelname)s: %(message)s'
#
# # 日志时间格式
# LOG_DATEFORMAT='%Y-%m-%d %H:%M:%S'
#
# # 日志级别 CRITICAL, ERROR, WARNING, INFO, DEBUG
# LOG_LEVEL='ERROR'
#
# # 如果等于True，所有的标准输出（包括错误）都会重定向到日志，例如：print('hello')
# LOG_STDOUT=False
#
# # 如果等于True，日志仅仅包含根路径，False显示日志输出组件
# LOG_SHORT_NAMES=False
# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'kick.middlewares.KickSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'kick.middlewares.KickDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'kick.pipelines.KickPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
