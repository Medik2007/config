require('lualine').setup()
require('nvim-autopairs').setup()
require('mini.animate').setup()
require("toggleterm").setup()
require("mason").setup()
require("glow").setup()

require'colorizer'.setup({
    css = {
        css = true;
    }
})

require('nvim-ts-autotag').setup({
    filetypes = { "html" , "xml" , "htmldjango" },
})

require('nvim-treesitter.configs').setup {
    ensure_installed = { "c", "lua", "python", "javascript", "html", "css", "htmldjango", "cpp", "php" },
    highlight = {enable = true}
}

require'alpha'.setup(require'alpha.themes.dashboard'.config)

vim.cmd[[colorscheme tokyonight-night]]
--vim.cmd[[colorscheme dayfox]]
vim.cmd[[colorscheme duskfox]]
