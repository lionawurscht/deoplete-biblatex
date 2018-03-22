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

To install `deoplete-biblatex`, use your favorite `Neovim<https://neovim.io_>`_
plugin manager.

`vim-plug<https://github.com/junegunn/vim-plug_>_`_
---------------------------------------------------

:: 

   Plug 'Shougo/deoplete.nvim', { 'do': ':UpdateRemotePlugins' }
   Plug 'lionawurscht/deoplete-biblatex'

Documentation
=============

For information on the configuration see `:help deoplete-biblatex.txt`
