Learn Python
============

Watch as I learn Python! Or don't. Whatever.

## Python installation
As of the beginning of the year, there are two versions of Python available for Debian:

 - `python`, which is at version 2.7.3 (latest available at [python.org][1] is 2.7.9), and
 - `python3`, which is at version 3.2.3 (latest available at [python.org][1] is 3.4.2)

Since I wanted the latest and greatest, I built 3.4.2 from source [following these directions][2] (twice, actually, because my fingers typed `/user/` when my brain thought `/usr/`).

I also had to add the new python directory to the `PATH` environment variable in my `.bashrc` file, like so: `export PATH="$PATH:/usr/local/opt/python-3.4.2/bin"`.

  [1]: http://python.org
  [2]: http://www.extellisys.com/articles/python-on-debian-wheezy
