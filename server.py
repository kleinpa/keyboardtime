import os
import cherrypy
import db
import json

import decimal
import datetime

class Root(object):
  _cp_config = {'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__)),
  'tools.staticdir.on' : True,
  'tools.staticdir.dir' : 'web',
  'tools.staticdir.index' : 'index.html',
  }

  @cherrypy.expose
  def data(self):
    class ForegroundEncoder(json.JSONEncoder):
      def default(self, obj):
          if isinstance(obj, decimal.Decimal):
              return float(obj)
          if isinstance(obj, db.ForegroundApplication):
              return {
                'start': obj.start,
                'duration': obj.duration,
                'application': obj.application,
                'activeness': obj.activeness,
              }
          if isinstance(obj, datetime.datetime):
            return obj.isoformat()

              #<sqlalchemy.orm.query.Query object at 0x04821DD0
          # Let the base class default method raise the TypeError
          return json.JSONEncoder.default(self, obj)

    with db.session_scope() as s:
      xs = s.query(db.ForegroundApplication).all()
      return json.dumps(xs, cls=ForegroundEncoder)

def run():
  cherrypy.tree.mount(Root(), '/',
  {'/': {'tools.gzip.on': True}})
  cherrypy.server.socket_port = 63874
  cherrypy.engine.start()


if __name__ == '__main__':
  cherrypy.engine.console_control_handler.subscribe()
  run()
  cherrypy.engine.block()
