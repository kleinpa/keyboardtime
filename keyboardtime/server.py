import sys
import os
import cherrypy
import json

import decimal
import datetime

import sqlalchemy
from sqlalchemy import func

from keyboardtime import software_info
from keyboardtime import db

def get_app_root():
  p = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
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
  def data(self, start=None, end=None):
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
      xs = s.query(db.ForegroundApplication)
      if start:
        start_dt = datetime.datetime.utcfromtimestamp(int(start))
        xs = xs.filter(db.ForegroundApplication.start >= start_dt)

      if end:
        end_dt = datetime.datetime.utcfromtimestamp(int(end))
        xs = xs.filter(db.ForegroundApplication.start <= end_dt)

      return json.dumps(xs.all(), cls=ForegroundEncoder)

  @cherrypy.expose
  def days(self):
    class ForegroundEncoder(json.JSONEncoder):
      def default(self, obj):
          if isinstance(obj, decimal.Decimal):
              return float(obj)
          if isinstance(obj, datetime):
            return obj.isoformat()+"Z"
          return json.JSONEncoder.default(self, obj)

    with db.session_scope() as s:
      to_local = lambda x: func.strftime('%Y-%m-%dT%H:%M:%S', x, 'localtime')
      date = func.strftime('%Y-%m-%d', db.ForegroundApplication.start, 'localtime')

      xs = s.query(
        date,
        to_local(func.min(db.ForegroundApplication.start)).label('start'),
        to_local(func.max(db.ForegroundApplication.start)).label('end'),
        func.sum(db.ForegroundApplication.duration).label('duration'),
        )
      xs = xs.select_from(db.ForegroundApplication)
      xs = xs.group_by(date)
      xs = xs.order_by(date.desc())
      return json.dumps(xs.all(), cls=ForegroundEncoder)

  @cherrypy.expose
  def info(self):
    return json.dumps(software_info.info)

  # Serve index.html for all pages to make angular routing easier
  @cherrypy.expose
  def default(self,*args,**kwargs):
    return cherrypy.lib.static.serve_file(
    os.path.join(get_app_root(), 'web', 'index.html'))

def run(port = None):
  if hasattr(cherrypy.engine, "console_control_handler"):
    cherrypy.engine.console_control_handler.subscribe()

  cherrypy.tree.mount(Root(), '/',
  {'/': {'tools.gzip.on': True,
         'tools.staticdir.content_types':
           {'woff2': 'application/font-woff2'}}})
  cherrypy.server.socket_port = port or software_info.info['port']
  cherrypy.engine.start()

if __name__ == '__main__':
  run()
  cherrypy.engine.block()
