=================
deoplete-biblatex
=================

`Deoplete-biblatex` offers completion of biblatex ids. By default it looks for
citations of this pattern:

:: 

   [AGreatCitation....

   [@AGreatCitation....

   [AGreatCitation,AnotherCitation....

   [@AGreatCitation,@AnotherCitation....

   [author:AGreatCitation...

   [author,authornumb:AnotherCitation...
   
Required
========

- `Neovim`_
- `Deoplete`_
- `Bibtexparser`_ for python

.. _deoplete: https://github.com/Shougo/deoplete.nvim
.. _bibtexparser: https://github.com/sciunto-org/python-bibtexparser

Installation
============

To install `deoplete-biblatex`, use your favorite `Neovim`_
plugin manager.

.. _Neovim: https://neovim.io

`vim-plug`_
--------------------------------------------------

:: 

   Plug 'Shougo/deoplete.nvim', { 'do': ':UpdateRemotePlugins' }
   Plug 'lionawurscht/deoplete-biblatex'
   
.. _vim-plug: https://github.com/junegunn/vim-plug

Documentation
=============

For information on the configuration see ``:help deoplete-biblatex``
