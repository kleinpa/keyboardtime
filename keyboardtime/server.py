import datetime
import decimal
import json
import os
import sys

import pkg_resources
import cherrypy
import dateutil.parser
import sqlalchemy
from sqlalchemy import func

from keyboardtime import software_info
from keyboardtime import db

def get_app_root():
  return os.path.abspath(os.path.dirname(__file__))

class Root(object):
  _cp_config = {
    'tools.staticdir.on' : True,
    'tools.staticdir.root' : pkg_resources.resource_filename('keyboardtime', 'web'),
    'tools.staticdir.dir' : '',
    'tools.staticdir.index' : 'index.html',
    'environment': 'embedded'
  }


  @cherrypy.expose
  def data_days(self):
    class ForegroundEncoder(json.JSONEncoder):
      def default(self, obj):
          if isinstance(obj, decimal.Decimal):
              return float(obj)
          if isinstance(obj, datetime.datetime):
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
  def data_detail(self, start=None, end=None):
    class ForegroundEncoder(json.JSONEncoder):
      def default(self, obj):
          if isinstance(obj, decimal.Decimal):
              return float(obj)
          if isinstance(obj, db.ForegroundApplication):
            return {
              'start': obj.start,
              'duration': obj.duration,
              'application': obj.application}
          if isinstance(obj, datetime.datetime):
            return obj.isoformat()+"Z"
          return json.JSONEncoder.default(self, obj)

    with db.session_scope() as s:
      to_local = lambda x: func.strftime('%Y-%m-%dT%H:%M:%S', x, 'localtime')
      date = func.strftime('%Y-%m-%d', db.ForegroundApplication.start, 'localtime')

      xs = s.query(db.ForegroundApplication.application)
      if start:
        start_dt = dateutil.parser.parse(start)
        xs = xs.filter(db.ForegroundApplication.start >= start_dt)
        print (start_dt.strftime("%A, %d. %B %Y %I:%M%p"))

      if end:
        end_dt = dateutil.parser.parse(end)
        xs = xs.filter(db.ForegroundApplication.start <= end_dt)

      activities = xs.add_column(db.ForegroundApplication.start)
      activities = activities.add_column(db.ForegroundApplication.duration)
      top = xs.group_by(db.ForegroundApplication.application)
      duration_sum = func.sum(db.ForegroundApplication.duration)
      top = top.add_column(duration_sum)
      top = top.order_by(duration_sum.desc())

      return json.dumps(
      {'activities': activities.all(),
       'top': top.all()}, cls=ForegroundEncoder)

  @cherrypy.expose
  def data_info(self):
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

  cherrypy.engine.signals.subscribe()


  cherrypy.engine.start()

if __name__ == '__main__':
  run()
  cherrypy.engine.block()
