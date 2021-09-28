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

from werkzeug.routing import ValidationError


def min_max_value(min_val, max_val):
    def validate(i):
        if not isinstance(i, int):
            raise ValidationError("Must be an integer")
        if min_val <= i <= max_val:
            return i
        raise ValidationError("Integer value must be >= {0} and  <= {1}".format(min_val, max_val))

    return validate


def min_value(min_val):
    def validate(i):
        if not isinstance(i, int):
            raise ValidationError("Must be an integer")
        if i >= min_val:
            return i
        raise ValidationError("Integer value must be >= {0}".format(min_val))

    return validate


def max_value(max_val):
    def validate(i):
        if not isinstance(i, int):
            raise ValidationError("Must be an integer")
        if i <= max_val:
            return i
        raise ValidationError("Integer value must be <= {0}".format(max_val))

    return validate


def min_length(min_val):
    def validate(s):
        if not isinstance(s, str):
            raise ValidationError("Must be a string")
        if len(s) >= min_val:
            return s
        raise ValidationError("String must be at least {0} characters long".format(min_val))

    return validate


def max_length(max_val):
    def validate(s):
        if not isinstance(s, str):
            raise ValidationError("Must be a string")
        if len(s) <= max_val:
            return s
        raise ValidationError("String must be less than {0} characters long".format(max_val + 1))

    return validate
