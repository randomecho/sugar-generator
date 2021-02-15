# Sugar Records Generator

Generate a number of records in Sugar.


## Usage

Create a single record (defaults to Accounts module):

    $ python generator.py

Specify a certain module (case-sensitive):

    $ python generator.py -m Opportunities

Create multiple records:

    $ python generator.py -m Opportunities -n 3

Create with a prefix slug

    $ python generator.py -p "Test -"

Create records in Person-type module

    $ python generator.py -person


## License

Released under [BSD 3-Clause](./LICENSE).

