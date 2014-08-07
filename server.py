import sys
import os
import cherrypy
import db
import json

import decimal
import datetime
import software_info

def get_app_root():
  p = os.path.abspath(os.path.dirname(__file__))
  if hasattr(sys,"frozen") and sys.frozen in ("windows_exe", "console_exe"):
    p=os.path.abspath(os.path.dirname(os.path.abspath(sys.executable)))
  return p

class Root(object):
  _cp_config = {
    'tools.staticdir.on' : True,
    'tools.staticdir.root' : os.path.join(get_app_root(), 'web'),
    'tools.staticdir.dir' : '',
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
            return obj.isoformat()+"Z"

              #<sqlalchemy.orm.query.Query object at 0x04821DD0
          # Let the base class default method raise the TypeError
          return json.JSONEncoder.default(self, obj)

    with db.session_scope() as s:
      xs = s.query(db.ForegroundApplication).all()
      return json.dumps(xs, cls=ForegroundEncoder)

  @cherrypy.expose
  def info(self):
    return json.dumps(software_info.info)

def run():
  if hasattr(cherrypy.engine, "console_control_handler"):
    cherrypy.engine.console_control_handler.subscribe()

  cherrypy.tree.mount(Root(), '/',
  {'/': {'tools.gzip.on': True}})
  cherrypy.server.socket_port = software_info.info['port']
  cherrypy.engine.start()

if __name__ == '__main__':

  run()
  cherrypy.engine.block()
