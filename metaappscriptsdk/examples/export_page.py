from metaappscriptsdk import MetaApp

META = MetaApp(meta_url="http://localhost:8080")
log = META.log

export = META.ExportService
res = export.export_page(58, 3203, ["res"], export_format="html")
print(u"res = %s" % str(res))
