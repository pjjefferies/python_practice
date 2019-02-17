# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 00:28:51 2019

@author: PaulJ
"""

# from __future__ import print_function

"""
class Debugger(object):
    attribute_accesses = []
    method_calls = []
"""

class Meta(type):
    """
    def __call__(cls, *args, **kw):  # run first. calls __new__ and __init__
        print('args:', args, '\nkw:', kw)
        # print('dir(cls):', dir(cls))
        print('\ncls.__setattr__:', cls.__setattr__)
        Debugger.method_calls.append({'class': cls.name,
                                      'method': 'hello',
                                      'args': args,
                                      'kwargs': kw})
        return type.__call__(*args, **kw)
    """
    """
    def __init__(cls, name, bases, nmspec):
        print('Meta.__init__ starting')
        # super(Meta, cls).__init__(name, bases, nmspec)
        # cls.uses_metaclass = lambda self: "Yes!"
        # cls.__dict__['name'] = name
        type.__setattr__(cls, 'name', name)
        print('name:', name)
        print('bases:', bases)
        print('nmspec:', nmspec)
        print('Meta.__init__ end\n')
    """

    """
    def __setattr__(cls, *args, **kw):
        print('starting __setattr__')
        print('setattr: args:', args, ', kw:', kw)
        Debugger.method_calls.append({
            'args': args,
            'class': type.__getattribute__(cls, 'name'),
            'kwargs': kw,
            'method': 'a_future_method_name_sa'})
        print('ending __setattr__')
    """
    pass
    def __getattribute__(cls, *args, **kw):
        print('starting __getattribute__')
        """
        print('getattribute: cls:', cls,
              '\n              args:', args,
              '\n              kw:', kw)
        """
        # attr = type.__getattribute__(cls, name)
        # class_name_tmp = object.__getattribute__(cls, 'name')
        # class_name_tmp = 'this is really hard'
        # print('class_name_tmp:', class_name_tmp)
        """
        Debugger.method_calls.append({
            'class': class_name_tmp,
            # 'method': 'a_future_method_name_ga',  # __getattribute__
            'args': args,
            'kwargs': kw})
        """
        print('ending __getattribute__\n')
        return object.__getattribute__(cls, 'name')

    """
        cls.
    def __getattribute__(self, name):
        attr = type.__getattribute__(self, name)
        if hasattr(attr, '__call__'):
            def newfunc(*args, **kwargs):
                print('before calling %s' %attr.__name__)
                # result = attr(*args, **kwargs)
                Debugger.attribute_accesses.append({'action': 'get',
                                                    'class':  type,
                                                    'attribute': name,
                                                    'value': attr})
                print('done calling %s' %attr.__name__)
                return result
            return newfunc
        else:
            return attr
    """


class Foo(object):
    __metaclass__ = Meta
    print('Foo class creation started')

    def __init__(self, x):
        self.x = x

    def bar(self, v):
        return (self.x, v)
    print('Foo class creation ended\n')

print('ready to create "A"')
a = Foo(1)
print('"A" created')
a.bar(2)
print('a.bar(2) run')

# calls = Debugger.method_calls[:]
# print('got calls. Get attribs')
# attribs = Debugger.attribute_accesses[:]