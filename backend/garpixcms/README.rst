
GarpixCMS
=========

Start new project with GarpixCMS
--------------------------------

.. code-block:: bash

   pip install cookiecutter

   cookiecutter https://github.com/garpixcms/garpixcms-empty-template

   # Enter name for your website...

   cd website

   # See README.md of project

   cat README.md

Garpix user
=========

Starting from version 4.0.0 of cms `garpix_auth` is deprecated and replaces by `garpix_user`.
If you used `garpix_auth` in your project with an older cms version, follow the steps below to update correctly.

1. Install new version of module `pip install garpixcms==4.0.0`.
2. Following the instructions for installing `garpix_user` (https://github.com/garpixcms/garpix_user#quickstart) set up the project (note that routes and basic settings are already included in the garpixcms module in `garpixcms/settings.py` and ` garpixcms/urls.py` respectively).
3. After applying the migrations run command `python3 manage.py update_user_module`.
4. Set .env variable `ENABLE_GARPIX_AUTH` to False or just delete it.

Changelog
=========

See `CHANGELOG.md <CHANGELOG.md>`_.

Contributing
============

See `CONTRIBUTING.md <CONTRIBUTING.md>`_.

License
=======

`MIT <LICENSE>`_
