# coding=utf-8
from metaappscriptsdk import MetaApp, pretty_json

META = MetaApp()
log = META.log

db_adplatform = META.db("adplatform")
u = db_adplatform.one("""
    SELECT id, name, info
    FROM users
    WHERE id = -1
    LIMIT 1
""")
# Выдаст None
print(u"u = %s" % u)

db_adplatform = META.db("adplatform")
dr = db_adplatform.query("""
    SELECT id, name, info
    FROM users
    WHERE name ILIKE 'Андре%'
    ORDER BY name
    LIMIT 1
""")
print(u"dr = %s" % pretty_json(dr))

for r in dr['rows']:
    print("\n")
    print(u"r['id'] = %s" % r['id'])
    print(u"r['name'] = %s" % r['name'])
    print(u"r['info'] = %s" % pretty_json(r['info']))

db_adhands_ui = META.db("adhands_ui")
dr = db_adhands_ui.query("""
    SELECT id, name
    FROM user
    WHERE name LIKE :uname
    AND id IN ( :ids )
    ORDER BY name
    LIMIT 3
""", {
    "uname": "Андре%",
    "ids": [8734, 3840]
})

for r in dr['rows']:
    print("\n")
    print(u"r['id'] = %s" % r['id'])
    print(u"r['name'] = %s" % r['name'])

db_adhands_ui = META.db("adhands_ui")
user = db_adhands_ui.one("""
    SELECT id, name
    FROM user
    WHERE id=:id
""", {"id": 4501})
print(u"user = %s" % pretty_json(user))

db_meta_samples = META.db("meta_samples")
dr = db_meta_samples.update("""
    UPDATE counters SET inc = inc + 1 WHERE name = :name
""", {"name": "md_source_update"})
print(u"dr = %s" % pretty_json(dr))
