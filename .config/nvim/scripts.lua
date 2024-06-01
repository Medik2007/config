vim.api.nvim_exec([[
  autocmd WinEnter * if (winnr("$") == 1 && &filetype == "neo-tree") | q | endif
]], false)
