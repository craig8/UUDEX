# coding: utf-8

"""
    UUDEXApi

    uudex api  # noqa: E501

    OpenAPI spec version: 1.0
    Contact: jeff.welsh@pnnl.gov
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six


class MessagePublishRespMessages(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'message_index': 'int',
        'message_md5_hash': 'str'
    }

    attribute_map = {
        'message_index': 'message_index',
        'message_md5_hash': 'message_md5_hash'
    }

    def __init__(self, message_index=None, message_md5_hash=None):  # noqa: E501
        """MessagePublishRespMessages - a model defined in Swagger"""  # noqa: E501
        self._message_index = None
        self._message_md5_hash = None
        self.discriminator = None
        if message_index is not None:
            self.message_index = message_index
        if message_md5_hash is not None:
            self.message_md5_hash = message_md5_hash

    @property
    def message_index(self):
        """Gets the message_index of this MessagePublishRespMessages.  # noqa: E501


        :return: The message_index of this MessagePublishRespMessages.  # noqa: E501
        :rtype: int
        """
        return self._message_index

    @message_index.setter
    def message_index(self, message_index):
        """Sets the message_index of this MessagePublishRespMessages.


        :param message_index: The message_index of this MessagePublishRespMessages.  # noqa: E501
        :type: int
        """

        self._message_index = message_index

    @property
    def message_md5_hash(self):
        """Gets the message_md5_hash of this MessagePublishRespMessages.  # noqa: E501


        :return: The message_md5_hash of this MessagePublishRespMessages.  # noqa: E501
        :rtype: str
        """
        return self._message_md5_hash

    @message_md5_hash.setter
    def message_md5_hash(self, message_md5_hash):
        """Sets the message_md5_hash of this MessagePublishRespMessages.


        :param message_md5_hash: The message_md5_hash of this MessagePublishRespMessages.  # noqa: E501
        :type: str
        """

        self._message_md5_hash = message_md5_hash

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(MessagePublishRespMessages, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, MessagePublishRespMessages):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
