Release Notes for Mamba ${version}
==================================

..
   Any new feature or bugfix should be listed in this file, for trivial fixes
    or features a bulleted list item is enough but for more sphisticated
    additions a subsection for their own is required.

Those are the release notes for Mamba ${version} released on ${release_date}.

Features
--------

* Added Created (201 HTTP) Response to predefined responses
* Added Unknown (209 HTTP) Response to predefined responses (209 is unassigned)
* Added Unauthorized (401 HTTP) Response to predefined responses
* Added MovedPermanently (301 HTTP) Response to predefined responses
* Added SeeOther (303 HTTP) Response to predefined responses
* Added Forbidden (403 HTTP) Response to predefined responses
* Added decimal size and precission using size property for MySQL decimal fields definitions::

    some_field = Decimal(size=(10, 2))  # using a tuple
    some_field = Decimal(size=[10, 2])  # using a list
    some_field = Decimal(size=10.2)     # using a float
    some_field = Decimal(size='10,2')   # using a string
    some_field = Decimal(size=10)       # using an int (precission is set to 2)
* If user define `development` as `true` in the `application.json` config file, the twistd server will be started in **no** daemon mode, logging will be printed to standard output and no log file should be produced at all. If the user press Ctrl+C the mamba application will terminate immediately, this mode is quite useful to development stages
* We redirect all the regular twistd process logging messages to `syslog` if we don't define development mode as `true` in the application.json config file
* Added `package` subcommand to `mamba-admin` command line tool that allow us to pack, install and uninstall mamba based applications in order to reuse them (that doesn't replace setuptools and is not the way meant to package a full mamba application in order to distribute it, this is only meant to reuse code already present in other projects)
* Added shared controllers, models and views for mamba installed packages. We can now add a configuration file `installed_packages.json` with the following syntax so mamba can install and reuse scrips (JavaScript, CSS) controllers, models and views in automatic way (nota that views search paths are always added to Jinja2 templating search path even if `autoimport` is `false`)::


        {
            "packages": {
                "package_name": {
                    "autoimport": true,
                    "use_scripts": true
                }
            }
        }
* Added `restart` command to `mamba-admin` command line tool
* Added `checkers` package to `mamba.utils` for common checks on forms and applications
* Added auto LESS resources compiling for mambaerized styleseets
* Added `find` method that can be used with or without a class instance:

    customer = yield Customer.find(name=u'John')
    customer = yield Customer().find(name=u'John')
    customer = yield Customer.find(Customer.name == u'john')
* Added `all` method that can be used with or without a class instance and return all the rows from a given model:

    customers = yield Customer.all()
    customers = yield Customer().all()
* Added `async` magic named boolean argument to `Transactor.run` so we can now run a `@transact` decorated method synchronous just as:
        customer = Customer.find(name=u'Pam', async=False)
        customer = Customer().read(1, async=False)
* Added global class `__mamba_async__` property to `mamba.application.model` so we can just make all the methods from a given class synchronous by default
* Added `auto_commit` msgic boolean argument to `Transactor.run` so we can now run a `@transact` decorated method that is not commit in automatic way by the transact mechanism (autocommit is True by default).
* Added several unit tests
* Added support for FOREIGN KEYS in SQLite version >= 3.6.19
* Added UNIQUE and INDEX for single and compound SQLite, MySQL/MariaDB and PostgreSQL fields
* Added support to don't add some tables to the generated schema using ``__mamba_schema__ = False`` option
* Added ``--noschema`` option in ``mamba-admin sql`` command line options
* Added shell to ``mamba-admin sql`` command line tool
* Now controllers can be attached to other controllers controllers to form a path route tree
* Added TestableDatabase and prepare_model_for_test function to make easier the task of test mamba applications models
* Added fixtures class (extends Storm's Schema)
* Added modules and controllers sub pacages automatic pre-load (for ex: application/model/sub_package/model.py)
* Added dict, json and pickle method to serialize Models


Bug Fixes
---------

* We were not using properly ZStorm/transaction and Twisted Transactor integration in Storm, now is fixed and a new `copy` helper method has been added to :class:`mamba.application.model.Model` class to allow simple object copy on user code because we can't use a store that has been created in a thread into the :class:`twisted.python.threadpool.ThreadPool` using the `@transact` decorator. If you need to pass initialized Storm objects directly to a view for whatever reasson you shouldn't use the `@transact` decorator at all (so you shouldn't use asynchronous call to the database for that).
* Now unhandled errors in Deferreds on routing module are displayed nicely in the logs file
* Model read method now returns a copy of the Storm object that can be used in other threads if the optional parameter copy is True (it's False by default)
* Fixed a bug in create SQL mamba-admin command when used with live (-l) option
* Fixed a bug related with PyPy and it's lack of **set_debug** method in **gc** object
* Now mamba-admin start and stop subcommands can be used inside valid mamba application directories only
* Adding dependency to fabric package as docs will not build without it
* Added mandatory option parameter `development` to the application.json template.
* Fixed memory leak in the routing system cache
* Fixed bug that hides log_file being null in options
* Fixed bug in package pack when using alternative names
* Fixed bug in package pack when version string has more than two levels
* Fixed bug related with routed methods that does not return anything
* Now mamba does not print a bogus and unrelated error message when there is some problem with the JSON config files
* Fixes paths in scrips and stylesheets that were preventing those ones to be added into the HTML generated by the templating engine
* :class:`~mamba.utils.Converter` wasn't serializing properties that were other objects properly, now is fixed
* decimal.Decimal values are now corretly serialized on :class:`~mamba.utils.Converter`
* Fixed some model tests that weren't working
* When `mamba-admin sql configure` ran in a validmamba app directory that does not contains a `config` directory, it crashed, fixed
* Fixed bug in PostgreSQL schema generation for FOREIGN KEYS
* Fixed wrong response being displayed when installing mamba reusabiility package from file
* Fixed bug where updates made to an installed mamba package was not updated.
* Fixed bug where mamba packages in egg format were not being installed. Added two extra unit tests in test_mamaba_admin.py for installing from egg and tar.
* Fixed exception being raised when POST, PUT and PATCH requests were send with no body


Changes
-------

* Now we can add a custom Jinja2 templates loader to our controller templates in two different ways:

    * **Method One**: Just pass the named param `loader=<your customer loader class>` to the `Template.render` call and it will overwrite any previous loader configuration
    * **Method Two**: When you first instanciate your template object (commonly with `self.template = templating.Template()`) add just your custom loader class as a property of the new template instance::

        self.template.loader = CustomLoader

    Note that is a class and not an instance what you have to use in both methods. The class **must** expect a list of strings (paths) as first and unique argument.
* The mamba-admin application subcommand generates now a ``logs`` directory and logs files are created inside it
* The mamba-admin application subcommand generates now a ``lib`` directory into the ``application`` directory in oreder to place code that doesn't fit the MVC pattern and 3rd party libraries
* The ``@route`` decorator now accepts lists and tuples defining more than one HTTP method where to register the given action
* The :class:`~mamba.enterprise.common.NativeEnum` type has been reimplemented as a ``set``. Implementation provided by Patrick O'Loughlin @paddyoloughlin on GitHub
* Added new find method to model object to find ojects into the database
* Storm.locals imports moved to ``mamba.entreprise`` package
* Now is possible to create subpakages for modules and controllers using 'subpackage.module_name' as the name of the controller or model, for ex: mamba-admin controller community.users
* If we return a Model object from a controller method, the routing system try to convert it into JSON instead of silently fail

Documentation
-------------

* Added contributors documentation
* Added developers documentation

Deprecations
------------

None

Removals
--------

* Removed unused cleanups in controller tests

Uncompatible Changes
--------------------

None

Details
-------

If you need a more detailed description of the changes made in this release you
can use git itself using::

   git log ${current_version}..${version}
