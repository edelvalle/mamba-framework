# -*- test-case-name: mamba.test.test_plugin -*-
# Copyright (c) 2012 Oscar Campos <oscar.campos@member.fsf.org>
# Ses LICENSE for more details

"""
Mamba Plugins System

This system is based on the really nice idea from Marty Alchin about plugins
systems using metaclasses that was exposed on his awesome book Pro Python.
"""


class ExtensionPoint(type):
    """
    Extenions mount point
    
    This class server 3 purposes:
        1) A way to declare a mount point for plugins or extensions point.
        2) A way to register a plugin in a particular mount point.
        3) A way to retrieve the plugins that have been registered.
        
        The system works by declaring classes that server as mount points.
        Since I subclass 'type' I can be used as a metaclass, for example:
        
        class ShareProvider:
            '''
            Mount point for plugins which refer to share services that can be 
            used.
            
            Plugins implementing this reference should provide the following
            attributes:
            
            =========== =======================================================
            name        Share service name
            url         The URL to connect with the service
            username    The username which connect to the service
            password    The user password
            API_key     The API Key to use with the service
            =========== =======================================================
            
            '''
            __metaclass__ = ExtensionPoint
        
        
        Then we can subclass those mount points in order to define plugins. 
        As the plugin will also inherits from the metaclass, they will be
        auto registered just for subclassing the provider. Example:
        
        class Twitter(ShareProvider):
            name = 'Twitter'
            url = 'http://api.twitter.com/'
            ...
        
        We can register any Share provider plugin just subclassing from the
        ShareProvider class and then use it to share our contents:
        
        For example:
        
        for share_service in ShareProvider.plugins:
            share_service().share(SharedObject)
    """
    
    
    def __init__(cls, name, bases, attrs):
        """        
        I will process the mount point itself and register plugins as well
            
        """
        
        if not hasattr(cls, 'plugins'):
            cls.plugins = []
        else:
            cls.plugins.append(cls)



__all__ = [
    'ExtensionPoint'
]