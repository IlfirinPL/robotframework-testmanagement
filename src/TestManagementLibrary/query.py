#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (c) 2015 Lingaro


import traceback

from robot.api import logger


class Operator(unicode):
    pass

Operator.EQUAL = Operator('=')
Operator.NOT_EQUAL = Operator('!=')
Operator.CONTAINS = Operator('contains')
Operator.NOT_CONTAINS = Operator('!contains')


class RallyQueryParameter(object):

    NAME = None
    DEFAULT_OPERATOR = Operator.EQUAL

    @classmethod
    def from_string(cls, value):
        #@TODO: so far only default operator is supported
        return cls(value)

    @classmethod
    def is_default_value(cls, value):
        return not bool(value)

    def __init__(self, value, operator=None):
        self._value = value
        if operator is None:
            operator = self.DEFAULT_OPERATOR
        self._operator = operator

    @property
    def name(self):
        if self.NAME is None:
            raise ValueError(u"subclass of RallyQueryParameter should provide NAME property")
        return self.NAME

    def construct(self):
        return u"{name} {operator} \"{value}\"".format(
            name=unicode(self.name),
            operator=unicode(self._operator),
            value=unicode(self._value)
        )

    def is_valid(self):
        return True


class ObjectIDParameter(RallyQueryParameter):
    NAME = u"ObjectID"
    DEFAULT_OPERATOR = Operator.EQUAL


class FormattedIDParameter(RallyQueryParameter):
    NAME = u'FormattedID'
    DEFAULT_OPERATOR = Operator.CONTAINS


class NotesParameter(RallyQueryParameter):
    NAME = u'Notes'
    DEFAULT_OPERATOR = Operator.CONTAINS


class ProjectParameter(RallyQueryParameter):
    NAME = u'Project'
    DEFAULT_OPERATOR = Operator.EQUAL


class DescriptionParameter(RallyQueryParameter):
    NAME = u'Description'
    DEFAULT_OPERATOR = Operator.CONTAINS


class NameParameter(RallyQueryParameter):
    NAME = u'Name'
    DEFAULT_OPERATOR = Operator.CONTAINS


class DisplayNameParameter(RallyQueryParameter):
    NAME = u'DisplayName'
    DEFAULT_OPERATOR = Operator.CONTAINS


class UserNameParameter(RallyQueryParameter):
    NAME = u'UserName'
    DEFAULT_OPERATOR = Operator.CONTAINS


class RallyQueryJoinMethod(unicode):

    PATTERN = u"({arg1}) {oper} ({arg2})"

    @classmethod
    def from_string(cls, value):
        if value == cls.AND:
            return cls.AND
        elif value == cls.OR:
            return cls.OR
        else:
            raise ValueError(u"Unsupported join method {0}".format(value))

    def join_params(self, params):
        result = u""
        if len(params) == 1:
            result = params[0].construct()
        elif len(params) > 1:
            result = self.PATTERN.format(
                arg1=params[0].construct(),
                oper=self,
                arg2=params[1].construct()
            )
            for param in params[2:]:
                result = self.PATTERN.format(
                    arg1=result,
                    oper=self,
                    arg2=param.construct()
                )
        return result

RallyQueryJoinMethod.AND = RallyQueryJoinMethod('AND')
RallyQueryJoinMethod.OR = RallyQueryJoinMethod('OR')


class RallyQuery(object):

    def __init__(self, join_method=None):
        self._params = []
        if join_method:
            join_method = RallyQueryJoinMethod.from_string(join_method)
        else:
            join_method = RallyQueryJoinMethod.AND
        self._join_method = join_method

    def add_parameter(self, parameter):
        if not parameter.is_valid():
            raise ValueError(u"Invalid parameter {0}".format(unicode(parameter)))
        if parameter in self._params:
            raise ValueError(u"Duplicated parameter value {0}".format(unicode(parameter)))
        self._params.append(parameter)

    def construct(self):
        return self._join_method.join_params(self._params)


class QueryManager(object):

    QUERY_PARAMETER_REGISTRY = dict(
        object_id=ObjectIDParameter,
        formatted_id=FormattedIDParameter,
        project=ProjectParameter,
        name=NameParameter,
        description=DescriptionParameter,
        notes=NotesParameter,
    )

    @classmethod
    def _build_query(cls, **kwargs):
        """
        Builder design pattern method witch construct the RallyQuery object base on method parameters.

        If parameter is evaluated to False, it will be omitted in the query.

        :return: query object with parameters.
        """
        query = RallyQuery(join_method=kwargs.pop(u'param_join_method', None))
        for name, value in kwargs.iteritems():
            if name in cls.QUERY_PARAMETER_REGISTRY:
                param_class = cls.QUERY_PARAMETER_REGISTRY.get(name)
                if not param_class.is_default_value(value):
                    param = param_class.from_string(value)
                    logger.info(u"{0} provided: {1}".format(param.name, unicode(value)))
                    query.add_parameter(param)
            else:
                logger.warn(u"Unregistered parameter class for key {0}".format(name))
        return query

    def _execute_rally_query(self, object_type, query, fetch=True, **kwargs):
        """
        Calls Rally Rest API with given query
        :param query: RallyQuery object
        :return:
        """
        connection = self._get_rally_connection()
        query_str = query.construct()
        logger.info(u"Constructed query: {0}".format(query_str))
        try:
            result = connection.get(object_type, fetch=fetch, query=query_str, **kwargs)
        except Exception as e:
            logger.warn(u"An error occurred during getting data")
            logger.warn(traceback.format_exc())
            raise e
        if result.errors:
            logger.warn(u"Some errors occurred when executed query: {0}".format(u"\n".join(result.errors)))
        return result

    def _get_object_by_id(self, object_type, id_param, **kwargs):
        """
        Fetch exactly one object of given type.
        :param object_type: object type
        :param id_param: an parameter that should identify exactly one object
        :param kwargs: extra params
        :return: request object from Rally
        """
        query = RallyQuery()
        query.add_parameter(id_param)
        result = list(self._execute_rally_query(object_type, query, **kwargs))
        if not result:
            logger.warn(u"No result found for {0}".format(id_param.construct()))
            raise ValueError(u"No result found")
        elif len(result) > 1:
            logger.warn(u"Found {0} but only one was expected, truncate extra data".format(len(result)))
        return result[0]
