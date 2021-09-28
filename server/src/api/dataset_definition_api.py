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

from flask_restful import abort
#
import views
from api import base
from models import db, DatasetDefinition
from services import authorization_service
from views.dataset_definition_view import DatasetDefinitionView

# -----------------------------------------------------------------------------------------------------


class DatasetDefinitionAPI(base.UUDEXResource):

    # get
    #
    # endpoint: /dataset-definitions OR
    # endpoint: /dataset-definitions/<uuid:dataset_definition_uuid>
    #
    # Returns a collection of all Dataset Definitions in the system OR
    # Returns a single Dataset
    #
    # This endpoint is available to all users of the system
    #
    def get_dataset_definition(self, dataset_definition_uuid):
        if dataset_definition_uuid is None:
            datasets = DatasetDefinition.query.order_by(DatasetDefinition.dataset_definition_name).all()
            if len(datasets) == 0:
                abort(404, message=f"No datasets found")
        else:
            uuid = str(dataset_definition_uuid)
            datasets = DatasetDefinition.query.get_uuid_or_404(uuid)

        resp = DatasetDefinitionView.generate_resp(datasets)
        return views.generate_resp_envelope(resp), 200

    def get(self, dataset_definition_uuid=None):
        return self.get_dataset_definition(dataset_definition_uuid)


    # post
    #
    # endpoint: /dataset-definitions
    #
    # Create a single Dataset
    #
    def create_dataset_definition(self, ):
        authorization_service.uudex_admin_or_403()
        args = DatasetDefinitionView.parse_post_req()

        dataset = DatasetDefinition(**args)
        db.session.add(dataset)
        db.session.commit()

        resp = DatasetDefinitionView.generate_resp(dataset)
        return views.generate_resp_envelope(resp), 200

    def post(self, ):
        return self.create_dataset_definition()

    # patch
    #
    # endpoint: /dataset-definitions/<int:dataset_definition_uuid>
    #
    # Update a single Metadata Schema
    #
    def update_dataset_definition(self, dataset_definition_uuid):
        authorization_service.uudex_admin_or_403()

        uuid = str(dataset_definition_uuid)
        dataset = DatasetDefinition.query.get_uuid_or_404(uuid)

        args = DatasetDefinitionView.parse_patch_req()

        changes = dataset.set_columns(**args)
        if len(changes):
            db.session.commit()

        resp = DatasetDefinitionView.generate_resp(dataset)
        return views.generate_put_resp_envelope(resp, changes), 200


    def patch(self, dataset_definition_uuid):
        return self.update_dataset_definition(dataset_definition_uuid)

    # delete
    #
    # endpoint: /dataset-definitions/<int:dataset_definition_uuid>
    #
    # Delete a single Metadata Schema
    #
    def delete_dataset_definition(self, dataset_definition_uuid):
        authorization_service.uudex_admin_or_403()

        uuid = str(dataset_definition_uuid)
        dataset = DatasetDefinition.query.get_uuid_or_404(uuid)

        db.session.delete(dataset)
        db.session.commit()

    def delete(self, dataset_definition_uuid):
        self.delete_dataset_definition(dataset_definition_uuid)
        return '', 204
