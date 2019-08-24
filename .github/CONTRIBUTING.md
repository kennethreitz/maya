# Contributing

Thank you for helping maya to get a better piece of software.

## Support

If you have any questions regarding the usage of maya please use the Question Issue Template or ask on [StackOverflow](https://stackoverflow.com).

## Reporting Issues / Proposing Features

Before you submit an Issue or proposing a Feature check the existing Issues in order to avoid duplicates. <br>
Please make sure you provide enough information to work on your submitted Issue or proposed Feature:

* Which version of maya are you using?
* Which version of python are you using?
* On which platform are you running maya?

Make sure to use the GitHub Template when reporting an issue.

## Pull Requests

We are very happy to receive Pull Requests considering:

* Style Guide. Follow the rules of [PEP8](http://legacy.python.org/dev/peps/pep-0008/), but you may ignore *too-long-lines* and similar warnings. There is a *pylintrc* file for more information.
* Tests. If our change affects python code inside the source code directory, please make sure your code is covered by an automated test case.

### Testing

To test the maya source code against all supported python versions you should use *tox*:

```bash
cd ~/work/maya
pip install tox
tox
```

However, if you want to test your code on certain circumstances you can create a *virtualenv*:

```
cd ~/work/maya
virtualenv env
source env/bin/activate
pip install -e '.[dev]'
commands = coverage run --parallel -m pytest -s --failed-first
```
