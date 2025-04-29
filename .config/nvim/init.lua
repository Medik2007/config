vim.g.loaded_netrw = 1
vim.g.loaded_netrwPlugin = 1
vim.opt.termguicolors = true
vim.cmd('set number relativenumber')
vim.cmd('set autoindent')
vim.cmd('set expandtab')
vim.cmd('set expandtab')
vim.cmd('set tabstop=4')
vim.cmd('set shiftwidth=4')
vim.cmd('set smarttab')
vim.cmd('set softtabstop=4')
vim.cmd('set encoding=UTF-8')
vim.cmd('set langmap=ФИСВУАПРШОЛДЬТЩЗЙКЫЕГМЦЧНЯ;ABCDEFGHIJKLMNOPQRSTUVWXYZ,фисвуапршолдьтщзйкыегмцчня;abcdefghijklmnopqrstuvwxyz')
vim.cmd('au BufRead,BufNewFile *.html set filetype=html')
vim.cmd("xnoremap <silent> <c-c> :w !wl-copy<CR><CR>")

local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({
    "git",
    "clone",
    "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable",
    lazypath,
  })
end
vim.opt.rtp:prepend(lazypath)

require("lazy").setup({
    'nvim-telescope/telescope.nvim',
    'akinsho/toggleterm.nvim',
    "nvim-lua/plenary.nvim",
    "nvim-tree/nvim-web-devicons",
    "MunifTanjim/nui.nvim",
    "nvim-neo-tree/neo-tree.nvim",
    'goolord/alpha-nvim',

    'preservim/tagbar',

    "nvim-lualine/lualine.nvim",
    "echasnovski/mini.animate",
    "folke/tokyonight.nvim",
    "nvim-treesitter/nvim-treesitter",
	"windwp/nvim-autopairs",
	"windwp/nvim-ts-autotag",

    "neovim/nvim-lspconfig",

	'hrsh7th/cmp-nvim-lsp',
	'hrsh7th/cmp-buffer',
	'hrsh7th/cmp-path',
	'hrsh7th/cmp-cmdline',
	'hrsh7th/nvim-cmp',
	'hrsh7th/cmp-vsnip',
	'hrsh7th/vim-vsnip',
    'norcalli/nvim-colorizer.lua',

    "iamcco/markdown-preview.nvim",

    "williamboman/mason.nvim",
    'williamboman/mason-lspconfig.nvim',

    "JamshedVesuna/vim-markdown-preview",
    "ellisonleao/glow.nvim",

    'kdheepak/lazygit.nvim',

    'EdenEast/nightfox.nvim',
})


PATH = os.getenv("HOME") .. "/.config/nvim/"
dofile(PATH.."modules.lua")
dofile(PATH.."lsp.lua")
dofile(PATH.."scripts.lua")
dofile(PATH.."keymaps.lua")
