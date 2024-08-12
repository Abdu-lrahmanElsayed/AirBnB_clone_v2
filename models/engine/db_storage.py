#!/usr/bin/python3
"""engine DBStorage"""
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
import models
from models.base_model import BaseModel
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review
import os


class DBStorage:
    """engine DBStorage"""
    __engine = None
    __session = None

    def __init__(self):
        """init"""
        self.__engine = create_engine(
                'mysql+mysqldb://{}:{}@{}/{}'.format(
                    os.getenv('HBNB_MYSQL_USER'),
                    os.getenv('HBNB_MYSQL_PWD'),
                    os.getenv('HBNB_MYSQL_HOST', default='localhost'),
                    os.getenv('HBNB_MYSQL_DB')),
                pool_pre_ping=True
                )
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        dic = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            for row in query:
                k = '{}.{}'.format(type(row).__name__, row.id)
                dic[k] = row
        else:
            cls_list = [State, City, User, Place, Review, Amenity]
            for i in cls_list:
                query = self.__session.query(i)
                for row in query:
                    k = '{}.{}'.format(type(row).__name__, row.id)
                    dic[k] = row
        return (dic)

    def new(self, obj):
        """Adds new object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes from the current database session obj"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database
            create the current database session"""
        self.__session = Base.metadata.create_all(self.__engine)
        sec = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sec)
        self.__session = Session()

    def close(self):
        """close"""
        self.__session.close()
