"""

UUDEX

Copyright © 2021, Battelle Memorial Institute

1. Battelle Memorial Institute (hereinafter Battelle) hereby grants
permission to any person or entity lawfully obtaining a copy of this
software and associated documentation files (hereinafter “the Software”)
to redistribute and use the Software in source and binary forms, with or
without modification.  Such person or entity may use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software, and
may permit others to do so, subject to the following conditions:

   - Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimers.
   - Redistributions in binary form must reproduce the above copyright notice,
     this list of conditions and the following disclaimer in the documentation
     and/or other materials provided with the distribution.
   - Other than as used herein, neither the name Battelle Memorial Institute
     or Battelle may be used in any form whatsoever without the express
     written consent of Battelle.

2. THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL BATTELLE OR CONTRIBUTORS BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

import datetime
#
from flask_restful import abort
from flask_sqlalchemy import BaseQuery, Model, SQLAlchemy


class UUDEXQueryBase(BaseQuery):
    def __init__(self, *args, **kwargs):

        self.__uuid_col = None
        self.__filters = None

        if len(args) > 0 and hasattr(args[0], "columns"):
            cols = args[0].columns
            uuid_col = [x.key for x in cols if x.key.endswith('_uuid')]
            if len(uuid_col) > 0:
                self.__uuid_col = uuid_col[0]
            else:
                self.__uuid_col = None

            self.__filters = {self.__uuid_col: None}

        super(BaseQuery, self).__init__(*args, **kwargs)

    def get_uuid_or_404(self, uuid):
        if self.__uuid_col is not None:
            self.__filters[self.__uuid_col] = uuid
            rv = self.filter_by(**self.__filters).one_or_none()
            if rv is None:
                model_class_name = self._mapper_zero().class_.__name__
                abort(404, code=404, message=f"{model_class_name} {uuid} not found")
            return rv
        else:
            return None


class UUDEXModelBase(Model):

    def _set_columns(self, **kwargs):
        force = kwargs.get('_force')

        readonly = []
        if hasattr(self, 'readonly_fields'):
            readonly = self.readonly_fields
        if hasattr(self, 'hidden_fields'):
            readonly += self.hidden_fields

        readonly += [
            'create_datetime',
        ]

        change_log = []
        changes = None

        columns = self.__table__.columns.keys()

        for key in columns:
            if self.__table__.columns.get(key).primary_key:
                continue
            #allowed = True if allowed or force or (key not in readonly and key[-5:] != "_uuid" and key[-3:] != "_id") else False
            allowed = True if force or (key not in readonly and key[-5:] != "_uuid") else False
            exists = True if key in kwargs else False
            if allowed and exists:
                val = getattr(self, key)
                if kwargs[key] is not None and val != kwargs[key]:
                    #changes['change'] = {'attribute': key, 'old': val, 'new': kwargs[key]}
                    changes = {'attribute': key, 'old_value': val, 'new_value': kwargs[key]}
                    change_log.append(changes)
                    #changes = {}
                    setattr(self, key, kwargs[key])
        return change_log

    def set_columns(self, **kwargs):
        self._changes = self._set_columns(**kwargs)
        #if 'create_datetime' in self.__table__.columns:
        #    self.create_datetime = datetime.datetime.utcnow()
        #if 'modified_datetime' in self.__table__.columns:
        #    self.modified_datetime = datetime.datetime.utcnow()

        return self._changes

    @property
    def changes(self):
        return self._changes

    def reset_changes(self):
        self._changes = []


db = SQLAlchemy(model_class=UUDEXModelBase, query_class=UUDEXQueryBase)
