# -*- coding: utf-8 -*-
"""Module containing the DOV data type for groundwater samples (GrondwaterMonsters), including
subtypes."""
from pydov.types.fields import (
    XmlField,
    XsdType,
    WfsField,
)
from .abstract import (
    AbstractDovType,
    AbstractDovSubType,
)

_observatieDataCodes_xsd = 'https://www.dov.vlaanderen.be/xdov/schema/' \
                       'latest/xsd/kern/observatie/ObservatieDataCodes.xsd'


class Observatie(AbstractDovSubType):

    rootpath = './/filtermeting/watermonster/observatie'

    fields = [
        XmlField(name='parameter',
                 source_xpath='/parameter',
                 definition='Parameter',
                 datatype='string',
                 xsd_type=XsdType(
                     xsd_schema=_observatieDataCodes_xsd,
                     typename='ParameterEnumType')),
        XmlField(name='eenheid',
                 source_xpath='/eenheid',
                 definition='Eenheid',
                 datatype='string',
                 xsd_type=XsdType(
                     xsd_schema=_observatieDataCodes_xsd,
                     typename='MeeteenheidEnumType')),
        XmlField(name='waarde',
                 source_xpath='/waarde_numeriek',
                 definition='waarde (numeriek) van de parameter',
                 datatype='float'),
        XmlField(name='parametergroep',
                 source_xpath='/parametergroep',
                 definition='Parametergroep',
                 datatype='string'),
        XmlField(name='veld_labo',
                 source_xpath='/veld_labo',
                 definition='observatie in het LABO of op het VELD',
                 datatype='string'),
    ]


class GrondwaterMonster(AbstractDovType):
    """Class representing the DOV data type for Groundwater samples."""

    subtypes = [Observatie]

    fields = [
        WfsField(name='pkey_monster', source_field='grondwatermonsterfiche',
                 datatype='string'),
        WfsField(name='grondwatermonsternummer', source_field='grondwatermonsternummer',
                 datatype='string'),
        WfsField(name='pkey_filter', source_field='filterfiche',
                 datatype='string'),
        WfsField(name='pkey_grondwaterlocatie', source_field='grondwaterlocatiefiche',
                 datatype='string'),
        WfsField(name='gw_id', source_field='GW_ID', datatype='string'),
        WfsField(name='filternummer', source_field='filternr',
                 datatype='string'),
        WfsField(name='x', source_field='X_mL72', datatype='float'),
        WfsField(name='y', source_field='Y_mL72', datatype='float'),
        WfsField(name='mv_mtaw', source_field='Z_mTAW', datatype='float'),
        WfsField(name='gemeente', source_field='gemeente', datatype='string'),
        WfsField(name='datum_monstername', source_field='datum_monstername', datatype='date'),
    ]

    def __init__(self, pkey):
        """Initialisation.

        Parameters
        ----------
        pkey : str
            Permanent key of the GrondwaterMonster (groundwater sample), being a URI of the form
            `https://www.dov.vlaanderen.be/data/watermonster/<id>`.

        """
        super(GrondwaterMonster, self).__init__('filter', pkey)

    @classmethod
    def from_wfs_element(cls, feature, namespace):
        """Build `GrondwaterMonster` instance from a WFS feature element.

        Parameters
        ----------
        feature : etree.Element
            XML element representing a single record of the WFS layer.
        namespace : str
            Namespace associated with this WFS featuretype.

        Returns
        -------
        gwmonster : GrondwaterMonster
            An instance of this class populated with the data from the WFS
            element.

        """
        gwmonster = cls(
            feature.findtext('./{{{}}}grondwatermonsterfiche'.format(namespace)))

        for field in cls.get_fields(source=('wfs',)).values():
            gwmonster.data[field['name']] = cls._parse(
                func=feature.findtext,
                xpath=field['sourcefield'],
                namespace=namespace,
                returntype=field.get('type', None)
            )

        return gwmonster
