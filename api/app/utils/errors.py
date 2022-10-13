def error_404(description):
    return {
        'error': description or 'Não encontrado'
    }