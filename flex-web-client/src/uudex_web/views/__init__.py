from uudex_web.views.home import home_view
from uudex_web.views.sender import sender_view
from pydantic import BaseModel
from uudex_web.data import get_participants, get_subjects
from uudex_web.data.certificates import get_certificates
from uudex_web.views.subscriber import subscriber_view
from functools import partial

get_message_list = None
get_message = None

class _UUDEXView(BaseModel):
    route: str
    instance: object


class _UUDEXViews(BaseModel):
    home: _UUDEXView = _UUDEXView(route="/", instance=partial(home_view))
    sender: _UUDEXView = _UUDEXView(route="/sender", instance=partial(sender_view, get_subjects=get_subjects, get_certificates=get_certificates))
    subscriber: _UUDEXView = _UUDEXView(route="/subscriber", instance=partial(subscriber_view, get_certificates=get_certificates, get_message_list=get_message_list, get_message=get_message))

    def __getitem__(self, item):
        return getattr(self, item)

    def __iter__(self):
        for page in self.__dict__.values():
            yield page


UUDEXViews = _UUDEXViews()
