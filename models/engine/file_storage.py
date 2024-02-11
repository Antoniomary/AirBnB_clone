#!/usr/bin/python3
"""
    A module that defines the file_storage class
"""
import json


class FileStorage():
    """serializes an instance to a JSON file and
       deserializes a JSON file to an instances
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns the dictionary __object"""
        return self.__objects

    def new(self, obj):
        """sets in __object the obj with key <obj class name>.id"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file whose name
           is held in the class variable __file_path
        """
        with open(self.__file_path, 'w') as json_file:
            obj_to_dict = {}
            for key, value in self.__objects.items():
                obj_to_dict[key] = value.to_dict()
            json.dump(obj_to_dict, json_file)

    def reload(self):
        """deserializes the JSON file whose name is held
           in the class variable __file_path
        """
        try:
            classes, _ = self.classes_and_their_attr_types()
            with open(self.__file_path, 'r') as json_file:
                obj_dict = json.load(json_file)
                for key, value in obj_dict.items():
                    selected_class = classes[value["__class__"]]
                    self.__objects[key] = selected_class(**value)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            pass

    # def classes(self):
    @staticmethod
    def classes_and_their_attr_types():
        """returns all the classes and their attribute types
           that work with FileStorage
        """
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review
        from datetime import datetime

        classes = {
                "BaseModel": BaseModel,
                "User": User,
                "State": State,
                "City": City,
                "Amenity": Amenity,
                "Place": Place,
                "Review": Review,
            }

        class_attr_types = {
                "BaseModel": {
                        "id": str,
                        "created_at": datetime,
                        "updated_at": datetime,
                    },

                "User": {
                        "email": str,
                        "password": str,
                        "first_name": str,
                        "last_name": str,
                    },

                "State": {
                        "name": str,
                    },

                "City": {
                        "state_id": str,
                        "name": str,
                    },

                "Amenity": {
                        "name": str,
                    },

                "Place": {
                        "city_id": str,
                        "user_id": str,
                        "name": str,
                        "description": str,
                        "number_rooms": int,
                        "number_bathrooms": int,
                        "max_guest": int,
                        "price_by_night": int,
                        "latitude": float,
                        "longitude": float,
                        "amenity_ids": list,
                    },

                "Review": {
                        "place_id": str,
                        "user_id": str,
                        "text": str,
                    },
            }

        return classes, class_attr_types
