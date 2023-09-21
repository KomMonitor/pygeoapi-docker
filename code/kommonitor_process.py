# =================================================================
#
# Authors: Tom Kralidis <tomkralidis@gmail.com>
#
# Copyright (c) 2022 Tom Kralidis
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

import logging
import geopandas as gpd

from pygeoapi.process.base import BaseProcessor, ProcessorExecuteError


LOGGER = logging.getLogger(__name__)

#: Process metadata and description
PROCESS_METADATA = {
    'version': '0.2.0',
    'id': 'reproject-process',
    'title': {
        'en': 'Reproject Process'
    },
    'description': {
        'en': 'A process for reprojecting GeoJSON features into a target CRS.',
    },
    'jobControlOptions': ['sync-execute', 'async-execute'],
    'keywords': ['reproject', 'kommonitor'],
    'links': [{
        'type': 'text/html',
        'rel': 'about',
        'title': 'information',
        'href': 'https://example.org/process',
        'hreflang': 'en-US'
    }],
    'inputs': {
        'features': {
            'title': 'Features',
            'description': 'GeoJSON Features',
            'schema': {
                'type': 'string',
                'mediaType': 'application/geo+json'
            },
            'minOccurs': 1,
            'maxOccurs': 1,
            'metadata': None,  # TODO how to use?
            'keywords': ['features']
        },
        'crs': {
            'title': 'CRS',
            'description': 'Target CRS',
            'schema': {
                'type': 'integer'
            },
            'minOccurs': 0,
            'maxOccurs': 1,
            'metadata': None,
            'keywords': ['crs']
        }
    },
    'outputs': {
        'reprojected_features': {
            'title': 'Reprojected features',
            'description': 'A GeoJSON String with all features reprojected'
                           ' to the requested CRS.',
            'schema': {
                'type': 'object',
                'contentMediaType': 'application/json'
            }
        }
    },
    'example': {
        'inputs': {
            'features': "{\"type\":\"FeatureCollection\",\"features\":[{\"type\":\"Feature\",\"properties\":{},\"geometry\":{\"coordinates\":[7.22468,51.5158],\"type\":\"Point\"}}]}",
            'crs': 25832,
        }
    }
}


class ReprojectProcessor(BaseProcessor):
    """Reproject Processor"""

    def __init__(self, processor_def):
        """
        Initialize object

        :param processor_def: provider definition

        :returns: pygeoapi.process.kommonitor_process.ReprojectProcessor
        """

        super().__init__(processor_def, PROCESS_METADATA)

    def execute(self, data):

        mimetype = 'application/json'
        features = data.get('features')
        crs = data.get('crs')

        if features is None:
            raise ProcessorExecuteError('Cannot process without features')
        if crs is None:
            raise ProcessorExecuteError('Cannot process without CRS')

        gdf = gpd.read_file(features, driver='GeoJSON')
        gdf = gdf.to_crs(crs)

        value = gdf.to_json()

        outputs = {
            'id': 'reprojected_features',
            'value': value
        }

        return mimetype, outputs

    def __repr__(self):
        return f'<ReprojectProcessor> {self.name}'
