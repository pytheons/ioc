# Python Simple Dependency Injection Container

This project is a simple port of the Symfony DependencyInjection lib available at https://github.com/symfony/dependency-injection

Status: Work In Progress

## Usage

Create a file `services.yml` file, the file will contains different service definiton such as

.. code-block:: yaml

    parameters:
        foo.bar: argument 1

    services:
        fake:
            class: tests.ioc.service.Fake
            arguments: 
                - "%foo.bar%"
            kargs:
                param: here a parameter
            calls:
                 - [ set_ok, [ false ]]
                 - [ set_ok, [ true ], {arg2: "arg"} ]

        foo:
            class: tests.ioc.service.Foo
            arguments: ["@fake", "#@weak_reference"]
            kargs: {}

        weak_reference:
            class: tests.ioc.service.WeakReference


Then to use and access a service just do

.. code-block:: python

    import ioc

    container = ioc.build(['services.yml'])

    foo = container.get('foo')
