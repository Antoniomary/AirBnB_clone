#!/usr/bin/python3
"""
    A module that defines a BaseModel class
"""
import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """defines all common attributes/methods for other classes"""
    def __init__(self, *args, **kwargs):
        """creates a new instance"""
        if kwargs:
            for k, v in kwargs.items():
                if k != "__class__":
                    if k in ["created_at", "updated_at"]:
                        v = datetime.fromisoformat(v)
                    setattr(self, k, v)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            storage.new(self)

    def __str__(self):
        """returns the format [<classname>] (<self.id>) <self._)dict__>"""
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """updates attribute updated_at with the current datetime"""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values of __dict__
           of the instance
        """
        my_dict = {
                "__class__": self.__class__.__name__,
        }
        for key in self.__dict__.keys():
            if key in ["created_at", "updated_at"]:
                my_dict[key] = datetime.isoformat(self.__dict__[key])
            else:
                my_dict[key] = self.__dict__[key]
        return my_dict
