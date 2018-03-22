=================
deoplete-biblatex
=================

`Deoplete-biblatex` offers completion of biblatex ids. By default it looks for
citations of this pattern:

:: 

   [AGreatCitation....
   
   [AGreatCitation,AnotherCitation....
   
   [author:AGreatCitation...
   
   [author,authornumb:AnotherCitation...

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

For information on the configuration see ``:help deoplete-biblatex.txt``
