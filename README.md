#shelp
##the Somewhat Helpful Extendable Linguistic Person

###What is shelp?

shelp is a lightweight IRC bot with a simple module system. No dependencies are required to run shelp. All that is needed is Python3.

###How do I add modules?

In the shelp module system, modules are called 'shelpers'.  A shelper is a class that implements the `Shelper` module.  In addition to implementing the `Shelper` class, a shelper also

 * Has a trigger, which is a regex string set on the `REGEX` member
 * Has `run` defined which returns an empty list or a list of strings on all code paths. The only argument to `run` is `m` which is an IRC message containing the trigger.

Here is an example of a shelper that responds to 'Hello!'.

     from lib.shelper import Shelper

     class Hello(Shelper):
         REGEX = r'^Hello!$'

         def run(self, m):
             return ['Hi! You just said '+m]

Note at this time that a shelper cannot import any external packages or modules other than `Shelper`.

###What is on the future feature list?

shelp will eventually be able to

* Identify who said a message with the trigger
* Nickserv support