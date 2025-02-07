local cmp = require'cmp'

cmp.setup({
	snippet = {
		expand = function(args)
		vim.fn["vsnip#anonymous"](args.body)
		end,
	},
	window = {},
	mapping = cmp.mapping.preset.insert({
		['<c-b>'] = cmp.mapping.scroll_docs(-4),
		['<c-n>'] = cmp.mapping.scroll_docs(4),
		['<c-Space>'] = cmp.mapping.complete(),
		['<c-e>'] = cmp.mapping.abort(),
		['<tab>'] = cmp.mapping.confirm({ select = true }),
	}),
	sources = cmp.config.sources({{ name = 'nvim_lsp' },{ name = 'vsnip' }}, {{ name = 'buffer' }}),
})

cmp.setup.cmdline({ '/', '?' }, {
	mapping = cmp.mapping.preset.cmdline(),
	sources = {{ name = 'buffer' }}
})

cmp.setup.cmdline(':', {
	mapping = cmp.mapping.preset.cmdline(),
	sources = cmp.config.sources({{ name = 'path' }}, {{ name = 'cmdline' }})
})

local lspconfig = require('lspconfig')
local lsp_capabilities = require('cmp_nvim_lsp').default_capabilities()


require('mason').setup({})
require('mason-lspconfig').setup({
    ensure_installed = {
        'html',
        'cssls',
        'bashls',
        'jsonls',
        'clangd',
        'pyright',
        'openscad_lsp',
        'lua_ls',
        'eslint',
    },
    handlers = {
        function(server)
            local setup = {capabilities = lsp_capabilities}
            if server == "lua_ls" then
                setup.settings = {Lua = {diagnostics = {globals = {'vim'}}}}
            end
            if server == "html" then
                setup.settings = {html = {validate = { scripts = false }}}
            end
            lspconfig[server].setup(setup)
        end
    }
})
