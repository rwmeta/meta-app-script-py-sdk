# coding=utf-8
import base64

from metaappscriptsdk import MetaApp, pretty_json

META = MetaApp()
log = META.log

YOUR_FILE_CONTENT_BASE64 = base64.b64encode("Hello, from META!")

# Получаете инстанс сервиса и делаете запрос к нему
result = META.MediaService.persist_one(
    file_base64_content=YOUR_FILE_CONTENT_BASE64,
    filename="req.txt",
    extension="txt",
    mime="plain/text"
)
# Формат ответа стандартный для меты
first = result['rows'][0]
print(u"result['rows'][0]['url'] = %s" % first['url'])
print(u"first = %s" % first)
print(u"result = %s" % pretty_json(result))
